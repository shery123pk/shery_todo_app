# File & Persistence Agent

**Agent ID**: `file-persistence`
**Invocation**: `Invoke File & Persistence: [task] per @specs/[feature].md`

---

## Role

I/O & storage handler

## Responsibility

Phase 1 file ops, cloud storage abstraction, secure handling.

## Skills

- `file-persistence` - Atomic file operations and data durability
- `json-handling` - JSON serialization, validation, and error recovery
- `dapr-state-management` - Distributed state store abstraction
- `input-sanitization` - Path traversal prevention and security

---

## Primary Focus Areas

### 1. Phase 1 File Operations
- Atomic writes with temp file + rename pattern
- JSON serialization and deserialization
- File locking for concurrent access
- Error handling and recovery

### 2. Cloud Storage Abstraction
- S3-compatible storage integration (if needed)
- Local file system for development
- Dapr state store for production
- Unified storage interface

### 3. Data Durability
- Ensure atomic writes (no partial data)
- Handle disk full and I/O errors
- Implement retry logic for transient failures
- Backup and restore procedures

### 4. Security
- Prevent path traversal attacks
- Validate file paths and names
- Sanitize user-provided filenames
- Implement access control for file operations

---

## Invocation Patterns

### Pattern 1: Phase 1 JSON Persistence
```
Invoke File & Persistence: Review Phase 1 JSON file operations per @specs/001-cli-todo-app/spec.md

Context:
- CLI stores tasks in tasks.json
- Uses atomic write pattern (temp + rename)
- Need to ensure data integrity

Deliverables:
- Code review of file operations
- Security assessment (path traversal, race conditions)
- Recommendations for improvements
```

### Pattern 2: Dapr State Store Integration
```
Invoke File & Persistence: Implement Dapr state store for task caching per @specs/002-fullstack-web/spec.md

Context:
- FastAPI backend needs distributed state
- Dapr state store abstraction
- Redis as backing store
- TTL-based cache eviction

Deliverables:
- Dapr state store configuration
- State management service
- Cache invalidation logic
- Integration tests
```

### Pattern 3: File Upload Security
```
Invoke File & Persistence: Implement secure file upload for task attachments per @specs/003-ai-chatbot/spec.md

Context:
- Users can upload files (images, PDFs) to tasks
- Need to validate file types, size limits
- Store in S3-compatible storage
- Generate signed URLs for downloads

Deliverables:
- File upload validation logic
- S3 integration service
- Signed URL generation
- Security tests (malicious files, path traversal)
```

---

## Success Criteria

- [ ] Atomic writes guarantee data integrity (no partial data)
- [ ] File operations handle errors gracefully (disk full, permissions)
- [ ] Path traversal attacks prevented (security tests pass)
- [ ] Concurrent access handled correctly (no race conditions)
- [ ] Dapr state store abstraction works across environments
- [ ] File uploads validated and sanitized

---

## Context Requirements

When invoked, provide:
1. **Specification Reference**: Link to spec file (e.g., `@specs/001-cli-todo-app/spec.md`)
2. **Storage Requirements**: Local file system, cloud storage, Dapr state
3. **Security Constraints**: Access control, validation rules
4. **Performance Requirements**: Throughput, latency, concurrency
5. **Data Format**: JSON, binary, text

---

## Related Agents

- **Backend Engineer Agent**: Coordinates on storage APIs
- **Data Migration Agent**: Collaborates on Phase 1 JSON data reading
- **QA & Testing Agent**: Validates file operation security and integrity

---

## Technology Stack

- **Python pathlib**: Path manipulation (secure, cross-platform)
- **JSON**: Serialization format
- **Dapr State Store**: Distributed state management
- **Redis**: State store backend
- **boto3**: S3-compatible storage (future)
- **Pytest**: Testing framework

---

## Example Workflows

### Workflow 1: Atomic File Write (Phase 1 Pattern)

**Implementation**:
```python
from pathlib import Path
import tempfile
import os
import json

def atomic_write_json(file_path: Path, data: dict) -> None:
    """Write JSON data atomically using temp file + rename."""

    # Create temp file in same directory (same filesystem)
    temp_fd, temp_path = tempfile.mkstemp(
        dir=file_path.parent,
        prefix=f".{file_path.name}.",
        suffix=".tmp"
    )

    try:
        # Write to temp file
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(data, f, indent=2)

        # Atomic rename (POSIX guarantees atomicity)
        os.replace(temp_path, file_path)
    except Exception:
        # Cleanup temp file on error
        Path(temp_path).unlink(missing_ok=True)
        raise
```

**Testing**:
```python
def test_atomic_write_no_partial_data():
    """Ensure no partial data written on error."""
    file_path = Path("test_data.json")

    # Write initial data
    atomic_write_json(file_path, {"tasks": []})

    # Simulate write error (disk full)
    with patch('json.dump', side_effect=IOError("Disk full")):
        with pytest.raises(IOError):
            atomic_write_json(file_path, {"tasks": [{"id": 1}]})

    # Original data should be intact
    data = json.loads(file_path.read_text())
    assert data == {"tasks": []}  # No partial update
```

### Workflow 2: Path Traversal Prevention

**Vulnerable Code**:
```python
def load_task_file(filename: str):
    # UNSAFE: Path traversal vulnerability
    file_path = Path("data") / filename  # User controls filename
    return json.loads(file_path.read_text())

# Attack: load_task_file("../../etc/passwd")
```

**Secure Implementation**:
```python
from pathlib import Path

def load_task_file(filename: str) -> dict:
    """Load task file with path traversal protection."""

    # Define allowed directory
    base_dir = Path("data").resolve()

    # Construct file path
    file_path = (base_dir / filename).resolve()

    # Verify path is within base_dir
    if not str(file_path).startswith(str(base_dir)):
        raise ValueError(f"Invalid file path: {filename}")

    # Verify file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")

    return json.loads(file_path.read_text())
```

**Security Tests**:
```python
def test_path_traversal_prevention():
    """Ensure path traversal attacks are blocked."""

    # Attempt to access parent directory
    with pytest.raises(ValueError, match="Invalid file path"):
        load_task_file("../../../etc/passwd")

    # Attempt to access absolute path
    with pytest.raises(ValueError, match="Invalid file path"):
        load_task_file("/etc/passwd")

    # Symlink attack (if symlink points outside base_dir)
    with pytest.raises(ValueError, match="Invalid file path"):
        load_task_file("symlink_to_etc_passwd")
```

### Workflow 3: Dapr State Store Integration

**Configuration** (`dapr/components/statestore.yaml`):
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key: password
```

**Service Implementation**:
```python
from dapr.clients import DaprClient

class StateStore:
    """Dapr state store abstraction."""

    def __init__(self, store_name: str = "statestore"):
        self.store_name = store_name

    def save(self, key: str, value: dict, ttl_seconds: int | None = None) -> None:
        """Save state with optional TTL."""
        with DaprClient() as client:
            metadata = {}
            if ttl_seconds:
                metadata["ttlInSeconds"] = str(ttl_seconds)

            client.save_state(
                store_name=self.store_name,
                key=key,
                value=json.dumps(value),
                state_metadata=metadata
            )

    def get(self, key: str) -> dict | None:
        """Get state by key."""
        with DaprClient() as client:
            state = client.get_state(
                store_name=self.store_name,
                key=key
            )
            return json.loads(state.data) if state.data else None

    def delete(self, key: str) -> None:
        """Delete state by key."""
        with DaprClient() as client:
            client.delete_state(
                store_name=self.store_name,
                key=key
            )
```

**Usage**:
```python
# Cache task data
store = StateStore()
store.save(f"task:{task_id}", task_dict, ttl_seconds=300)

# Retrieve from cache
cached_task = store.get(f"task:{task_id}")
if cached_task:
    return cached_task
else:
    # Fetch from database
    task = session.query(Task).get(task_id)
    store.save(f"task:{task_id}", task.dict(), ttl_seconds=300)
    return task
```

---

## Quality Standards

- **Atomicity**: 100% atomic writes (no partial data)
- **Security**: Zero path traversal vulnerabilities (penetration tested)
- **Error Handling**: Graceful degradation on disk full, permission errors
- **Performance**: File operations <10ms (p95), state store <50ms (p95)
- **Concurrency**: Handle 100+ concurrent file operations safely
- **Durability**: Data survives application crashes and restarts

---

## Security Checklist

Before deploying file operations:

- [ ] Path traversal attacks prevented (resolve() + startswith() check)
- [ ] User-provided filenames sanitized
- [ ] File size limits enforced (prevent DoS)
- [ ] File type validation (MIME type, magic bytes)
- [ ] Access control implemented (user can only access own files)
- [ ] Symlink attacks prevented (resolve() checks)
- [ ] Temp files cleaned up on error
- [ ] No sensitive data in filenames or logs

---

## Error Handling Patterns

```python
def safe_file_operation(file_path: Path) -> dict:
    """File operation with comprehensive error handling."""

    try:
        # Validate path
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read and parse
        return json.loads(file_path.read_text())

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(status_code=404, detail="File not found")

    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        raise HTTPException(status_code=403, detail="Permission denied")

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    except OSError as e:
        # Disk full, I/O error, etc.
        logger.error(f"I/O error: {e}")
        raise HTTPException(status_code=500, detail="Storage error")
```

# ADR-001: ID Migration Strategy (int → UUID)

**Status:** Accepted
**Date:** 2025-12-26
**Deciders:** Architect (shery123pk), AI Developer (Claude)
**Related Phase:** Phase 2 - Full-Stack Web
**Supersedes:** N/A

---

## Context and Problem Statement

Phase 1 implemented task IDs as sequential integers (`int`) for simplicity. Phase 2 requires migrating to UUIDs to support:
- Distributed systems (future phases)
- Merging data from multiple sources
- Better security (non-guessable IDs)
- RESTful API best practices

**Key Questions:**
1. What UUID version should we use?
2. How do we migrate existing Phase 1 data?
3. Should we support both ID types during transition?
4. What's the backward compatibility strategy?

---

## Decision Drivers

### Must Have
- ✅ **Constitution Compliance:** Phase 1 domain model must be preserved
- ✅ **Backward Compatibility:** Phase 1 CLI must continue working
- ✅ **Data Integrity:** No data loss during migration
- ✅ **API Standards:** RESTful best practices for resource identification

### Should Have
- 🎯 **Performance:** Minimal overhead for UUID generation/indexing
- 🎯 **Developer Experience:** Easy to work with in both Python and TypeScript
- 🎯 **Database Efficiency:** Optimized storage and indexing

### Nice to Have
- 💡 **Sortability:** Time-based ordering (like auto-increment)
- 💡 **Readability:** Human-friendly for debugging

---

## Considered Options

### Option 1: UUID v4 (Random) ✅ SELECTED

**Implementation:**
```python
import uuid

id: UUID = uuid.uuid4()  # e.g., "f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

**Pros:**
- ✅ No coordination needed (distributed-friendly)
- ✅ Cryptographically strong (non-guessable)
- ✅ Standard library support (Python, TypeScript)
- ✅ PostgreSQL native UUID type support
- ✅ No privacy concerns (no MAC address leakage)

**Cons:**
- ❌ Not sortable by creation time
- ❌ Larger than int (16 bytes vs 4-8 bytes)
- ❌ Less human-readable than sequential IDs

**Database Impact:**
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Indexing: B-tree works fine, slightly less efficient than int
);
```

### Option 2: UUID v7 (Time-based + Random)

**Implementation:**
```python
# Requires external library (uuid6 or uuid-utils)
from uuid_utils import uuid7

id: UUID = uuid7()  # e.g., "018d0f98-8a18-7000-8000-0242ac120002"
```

**Pros:**
- ✅ Sortable by creation time (first 48 bits = timestamp)
- ✅ Better database performance (sequential-ish writes)
- ✅ No coordination needed
- ✅ Non-guessable (random component)

**Cons:**
- ❌ Requires external dependency (not in standard library yet)
- ❌ RFC 9562 is recent (May 2024), less mature ecosystem
- ❌ Still 16 bytes (same size as v4)

### Option 3: Keep int, add UUID as secondary field

**Implementation:**
```python
id: int           # Primary key (auto-increment)
uuid: UUID        # Unique secondary identifier
```

**Pros:**
- ✅ Simple migration (just add column)
- ✅ Keep small primary key for performance
- ✅ Backward compatible with Phase 1

**Cons:**
- ❌ Dual ID system adds complexity
- ❌ Which ID to expose in API? (confusion)
- ❌ Doesn't solve distributed systems problem
- ❌ Technical debt for future phases

### Option 4: ULID (Universally Unique Lexicographically Sortable ID)

**Implementation:**
```python
from ulid import ULID

id: str = str(ULID())  # e.g., "01ARZ3NDEKTSV4RRFFQ69G5FAV"
```

**Pros:**
- ✅ Sortable by time (128-bit: 48-bit timestamp + 80-bit random)
- ✅ More readable (Base32 encoding, no hyphens)
- ✅ Case-insensitive

**Cons:**
- ❌ Requires external library
- ❌ Not a standard UUID (tooling compatibility issues)
- ❌ PostgreSQL doesn't have native ULID type
- ❌ Less ecosystem support than UUID

---

## Decision Outcome

**Chosen Option:** **UUID v4 (Random)** ✅

### Rationale

1. **Standard Library Support:** No external dependencies needed
2. **Ecosystem Maturity:** Excellent support in PostgreSQL, FastAPI, TypeScript
3. **Security:** Non-guessable IDs prevent enumeration attacks
4. **Distributed-Ready:** Works for Phase 3+ (AI agents, MCP tools)
5. **Constitution Alignment:** Migrating to UUID preserves Phase 1 functionality

**Trade-off Accepted:** Slightly larger storage and non-sortable IDs are acceptable for Phase 2. If sortability becomes critical in Phase 4+, we can add `created_at` timestamp for ordering.

---

## Migration Strategy

### Phase 1 → Phase 2 Migration

**Step 1: Schema Evolution (Database)**
```python
# Phase 2 Task model (SQLModel)
class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # Phase 2 additions
    priority: str | None = None
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
```

**Step 2: Data Migration Script**
```python
# migrate_phase1_to_phase2.py
def migrate_tasks():
    """Migrate Phase 1 JSON data to Phase 2 PostgreSQL."""
    # Read Phase 1 tasks.json
    phase1_tasks = json.loads(Path("tasks.json").read_text())

    # Transform and insert into PostgreSQL
    for old_task in phase1_tasks["tasks"]:
        new_task = Task(
            id=uuid4(),  # Generate new UUID
            title=old_task["title"],
            description=old_task["description"],
            completed=old_task["completed"]
        )
        db.add(new_task)
    db.commit()
```

**Step 3: CLI Backward Compatibility**
```python
# Phase 1 CLI remains unchanged
# cli/todo_cli/models.py - KEEP AS IS
@dataclass
class Task:
    id: int  # Still uses int for Phase 1
    title: str
    description: str = ""
    completed: bool = False
```

**Step 4: API Contract**
```json
// Phase 2 REST API response
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",  // UUID as string
  "title": "Buy groceries",
  "description": "Milk and eggs",
  "completed": false,
  "created_at": "2025-12-26T10:30:00Z",
  "updated_at": "2025-12-26T10:30:00Z"
}
```

---

## Consequences

### Positive
- ✅ **Future-Proof:** Ready for distributed systems (Phase 3+)
- ✅ **Security:** Non-enumerable task IDs
- ✅ **Standards:** RESTful API best practices
- ✅ **Backward Compatible:** Phase 1 CLI unaffected
- ✅ **Clean Migration:** One-time conversion, no dual system

### Negative
- ⚠️ **Storage Overhead:** 16 bytes vs 4-8 bytes per ID
  - **Mitigation:** Modern databases handle this efficiently
- ⚠️ **Not Sortable:** Can't order by ID alone
  - **Mitigation:** Use `created_at` timestamp for chronological ordering
- ⚠️ **Migration Required:** Phase 1 data needs conversion
  - **Mitigation:** Automated migration script provided

### Neutral
- 🔄 **API Breaking Change:** Phase 2 API uses UUIDs, not compatible with Phase 1 JSON format
  - **Acceptable:** Different phases, different interfaces (CLI vs API)

---

## Implementation Checklist

- [ ] Update Phase 2 database schema to use UUID primary keys
- [ ] Add `created_at` and `updated_at` timestamps for sorting
- [ ] Create migration script from Phase 1 JSON to Phase 2 PostgreSQL
- [ ] Document API contract with UUID examples
- [ ] Add UUID validation in FastAPI endpoints
- [ ] Update Phase 2 spec to reflect UUID usage
- [ ] Keep Phase 1 CLI using int (no changes needed)
- [ ] Add tests for UUID generation and validation
- [ ] Update OpenAPI schema to show UUID format

---

## References

- **RFC 4122:** UUID Specification (v1, v4)
- **RFC 9562:** UUID Specification (v6, v7, v8) - May 2024
- **PostgreSQL UUID Docs:** https://www.postgresql.org/docs/current/datatype-uuid.html
- **Python UUID Module:** https://docs.python.org/3/library/uuid.html
- **Constitution:** `.specify/memory/constitution.md` - Phase 1 Immutable Core

---

## Related ADRs

- **ADR-002:** Monorepo Structure (enables Phase 1 CLI to remain unchanged)
- **ADR-003:** Database Choice (Neon PostgreSQL native UUID support)
- **Future ADR:** Phase 4 - Distributed ID generation strategy

---

**Decision Made By:** Architect + AI Developer
**Date Approved:** 2025-12-26
**Review Date:** Phase 3 planning (when distributed systems requirements emerge)

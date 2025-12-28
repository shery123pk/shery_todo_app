"""
Test file storage service.

Tests for file upload, validation, and storage abstraction.
"""

import pytest
import os
from pathlib import Path
from uuid import uuid4


@pytest.fixture
def cleanup_uploads():
    """Cleanup test uploads after tests."""
    uploaded_files = []
    yield uploaded_files
    # Cleanup
    for file_path in uploaded_files:
        if os.path.exists(file_path):
            os.remove(file_path)


def test_file_storage_service_exists():
    """Test that file storage service module exists."""
    from app.services import file_storage
    assert file_storage is not None


def test_validate_file_type():
    """Test file type validation."""
    from app.services.file_storage import validate_file_type

    # Valid image types
    assert validate_file_type("photo.jpg") == True
    assert validate_file_type("photo.png") == True
    assert validate_file_type("photo.gif") == True

    # Valid document types
    assert validate_file_type("document.pdf") == True
    assert validate_file_type("document.txt") == True

    # Invalid types
    assert validate_file_type("script.exe") == False
    assert validate_file_type("virus.bat") == False
    assert validate_file_type("malware.sh") == False


def test_validate_file_size():
    """Test file size validation."""
    from app.services.file_storage import validate_file_size
    from app.config import settings

    max_size = settings.max_file_size_mb * 1024 * 1024

    # Valid sizes
    assert validate_file_size(1024) == True  # 1KB
    assert validate_file_size(max_size - 1) == True

    # Invalid sizes
    assert validate_file_size(max_size + 1) == False
    assert validate_file_size(max_size * 2) == False


def test_generate_safe_filename():
    """Test safe filename generation."""
    from app.services.file_storage import generate_safe_filename

    # Should preserve extension
    safe_name = generate_safe_filename("my file.jpg")
    assert safe_name.endswith(".jpg")
    assert " " not in safe_name  # Spaces removed

    # Should handle special characters
    safe_name = generate_safe_filename("file@#$%.pdf")
    assert safe_name.endswith(".pdf")
    assert "@" not in safe_name
    assert "#" not in safe_name


def test_get_upload_path():
    """Test upload path generation."""
    from app.services.file_storage import get_upload_path

    org_id = uuid4()
    project_id = uuid4()
    task_id = uuid4()
    filename = "test.jpg"

    path = get_upload_path(org_id, project_id, task_id, filename)

    # Should be a Path object
    assert isinstance(path, Path)

    # Should contain IDs in path
    assert str(org_id) in str(path)
    assert str(project_id) in str(path)
    assert str(task_id) in str(path)
    assert filename in str(path)


@pytest.mark.asyncio
async def test_save_file(cleanup_uploads):
    """Test saving a file to storage."""
    from app.services.file_storage import save_file
    from io import BytesIO

    # Create fake file content
    file_content = b"This is a test file content"
    file = BytesIO(file_content)

    org_id = uuid4()
    project_id = uuid4()
    task_id = uuid4()
    filename = "test.txt"

    # Save file
    file_path = await save_file(file, org_id, project_id, task_id, filename)
    cleanup_uploads.append(str(file_path))

    # Verify file was saved
    assert os.path.exists(file_path)

    # Verify content
    with open(file_path, "rb") as f:
        saved_content = f.read()
    assert saved_content == file_content


@pytest.mark.asyncio
async def test_delete_file(cleanup_uploads):
    """Test deleting a file from storage."""
    from app.services.file_storage import save_file, delete_file
    from io import BytesIO

    # Create and save a file
    file_content = b"Test content to delete"
    file = BytesIO(file_content)

    org_id = uuid4()
    project_id = uuid4()
    task_id = uuid4()
    filename = "to_delete.txt"

    file_path = await save_file(file, org_id, project_id, task_id, filename)
    assert os.path.exists(file_path)

    # Delete file
    await delete_file(file_path)

    # Verify file was deleted
    assert not os.path.exists(file_path)


def test_allowed_file_extensions():
    """Test that allowed extensions list exists."""
    from app.services.file_storage import ALLOWED_EXTENSIONS

    assert isinstance(ALLOWED_EXTENSIONS, (list, tuple, set))
    assert "jpg" in ALLOWED_EXTENSIONS or ".jpg" in ALLOWED_EXTENSIONS
    assert "pdf" in ALLOWED_EXTENSIONS or ".pdf" in ALLOWED_EXTENSIONS

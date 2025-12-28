"""
File Storage Service

Handles file uploads, validation, and storage for task attachments.
Author: Sharmeen Asif
"""

import os
import aiofiles
from pathlib import Path
from uuid import UUID
from typing import BinaryIO
from app.config import settings


# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {
    # Images
    "jpg", "jpeg", "png", "gif", "webp",
    # Documents
    "pdf", "doc", "docx", "txt", "md",
    # Archives
    "zip",
    # Code
    "json", "csv", "xml",
}


def validate_file_type(filename: str) -> bool:
    """
    Validate that a file type is allowed for upload.

    Args:
        filename: Name of the file to validate

    Returns:
        True if file type is allowed, False otherwise

    Example:
        >>> validate_file_type("photo.jpg")
        True
        >>> validate_file_type("virus.exe")
        False
    """
    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def validate_file_size(size_bytes: int) -> bool:
    """
    Validate that a file size is within allowed limits.

    Args:
        size_bytes: File size in bytes

    Returns:
        True if size is valid, False otherwise

    Example:
        >>> validate_file_size(1024)  # 1KB
        True
        >>> validate_file_size(100 * 1024 * 1024)  # 100MB
        False
    """
    max_size = settings.max_file_size_mb * 1024 * 1024
    return 0 < size_bytes <= max_size


def generate_safe_filename(filename: str) -> str:
    """
    Generate a safe filename by removing special characters.

    Args:
        filename: Original filename

    Returns:
        Safe filename with only alphanumeric characters, dots, and hyphens

    Example:
        >>> generate_safe_filename("my file@#$.jpg")
        'my-file.jpg'
    """
    # Get extension
    if "." in filename:
        name, ext = filename.rsplit(".", 1)
    else:
        name, ext = filename, ""

    # Remove/replace special characters
    safe_name = "".join(
        c if c.isalnum() or c in "-_" else "-"
        for c in name
    )

    # Remove consecutive hyphens and trim
    safe_name = "-".join(filter(None, safe_name.split("-")))

    # Reconstruct filename
    if ext:
        return f"{safe_name}.{ext.lower()}"
    return safe_name


def get_upload_path(
    org_id: UUID,
    project_id: UUID,
    task_id: UUID,
    filename: str,
) -> Path:
    """
    Generate the full upload path for a file.

    Creates directory structure: uploads/org_{org_id}/project_{project_id}/task_{task_id}/

    Args:
        org_id: Organization UUID
        project_id: Project UUID
        task_id: Task UUID
        filename: Name of the file

    Returns:
        Path object for the file location

    Example:
        >>> get_upload_path(org_id, project_id, task_id, "file.jpg")
        Path('uploads/org_xxx/project_yyy/task_zzz/file.jpg')
    """
    # Base upload directory from settings
    base_dir = Path(settings.upload_dir)

    # Create hierarchical directory structure
    upload_dir = base_dir / f"org_{org_id}" / f"project_{project_id}" / f"task_{task_id}"

    # Full file path
    return upload_dir / filename


async def save_file(
    file: BinaryIO,
    org_id: UUID,
    project_id: UUID,
    task_id: UUID,
    filename: str,
) -> Path:
    """
    Save an uploaded file to storage.

    Creates necessary directories and saves file asynchronously.

    Args:
        file: File-like object with read() method
        org_id: Organization UUID
        project_id: Project UUID
        task_id: Task UUID
        filename: Name to save the file as

    Returns:
        Path where file was saved

    Example:
        >>> file_path = await save_file(uploaded_file, org_id, project_id, task_id, "photo.jpg")
    """
    # Generate safe filename
    safe_filename = generate_safe_filename(filename)

    # Get upload path
    file_path = get_upload_path(org_id, project_id, task_id, safe_filename)

    # Create directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Save file asynchronously
    async with aiofiles.open(file_path, "wb") as f:
        # Read content from uploaded file
        content = file.read() if hasattr(file, 'read') else file
        await f.write(content)

    return file_path


async def delete_file(file_path: Path | str) -> bool:
    """
    Delete a file from storage.

    Args:
        file_path: Path to the file to delete

    Returns:
        True if file was deleted, False if file didn't exist

    Example:
        >>> await delete_file("/uploads/org_xxx/.../file.jpg")
        True
    """
    file_path = Path(file_path) if isinstance(file_path, str) else file_path

    if file_path.exists():
        file_path.unlink()
        return True
    return False


async def get_file_info(file_path: Path | str) -> dict:
    """
    Get information about a stored file.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary with file info (size, name, extension)

    Example:
        >>> info = await get_file_info("/uploads/.../file.jpg")
        >>> info
        {'size': 1024, 'name': 'file.jpg', 'extension': 'jpg'}
    """
    file_path = Path(file_path) if isinstance(file_path, str) else file_path

    if not file_path.exists():
        return None

    stat = file_path.stat()
    return {
        "size": stat.st_size,
        "name": file_path.name,
        "extension": file_path.suffix.lstrip("."),
        "path": str(file_path),
    }

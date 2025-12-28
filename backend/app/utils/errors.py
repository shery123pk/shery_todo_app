"""
Error Handling Utilities

Custom exceptions and error formatting for consistent API responses.
Author: Sharmeen Asif
"""

from datetime import datetime, UTC
from typing import Any, Optional
from fastapi import HTTPException, status
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import IntegrityError


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(AppException):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422)


class NotFoundError(AppException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedError(AppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppException):
    """Raised when user lacks permission for an action."""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class ConflictError(AppException):
    """Raised when a resource conflict occurs (e.g., duplicate)."""

    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


def format_error_response(
    message: str,
    status_code: int,
    errors: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Format an error into a standard response structure.

    Args:
        message: Human-readable error message
        status_code: HTTP status code
        errors: Optional detailed errors (e.g., field-level validation errors)

    Returns:
        Dictionary with error details including timestamp

    Example:
        >>> format_error_response("Invalid email", 422, {"email": "Not a valid email"})
        {
            "message": "Invalid email",
            "status_code": 422,
            "errors": {"email": "Not a valid email"},
            "timestamp": "2025-12-27T10:30:00Z"
        }
    """
    return {
        "message": message,
        "status_code": status_code,
        "errors": errors,
        "timestamp": datetime.now(UTC).isoformat(),
    }


def format_validation_errors(exc: PydanticValidationError) -> dict[str, str]:
    """
    Format Pydantic validation errors into field-level error messages.

    Args:
        exc: Pydantic ValidationError exception

    Returns:
        Dictionary mapping field names to error messages

    Example:
        >>> errors = format_validation_errors(validation_error)
        >>> errors
        {"email": "Invalid email format", "age": "Must be a positive integer"}
    """
    errors = {}
    for error in exc.errors():
        # Get field path (e.g., ['email'] or ['address', 'city'])
        field_path = error["loc"]
        # Join nested fields with dots (e.g., 'address.city')
        field_name = ".".join(str(loc) for loc in field_path if loc != "body")

        # Get error message
        error_msg = error["msg"]

        errors[field_name] = error_msg

    return errors


def handle_database_error(exc: IntegrityError) -> dict[str, Any]:
    """
    Handle database integrity errors and format appropriate responses.

    Args:
        exc: SQLAlchemy IntegrityError exception

    Returns:
        Formatted error response dictionary

    Example:
        >>> handle_database_error(integrity_error)
        {
            "message": "Email already exists",
            "status_code": 409,
            "errors": None,
            "timestamp": "..."
        }
    """
    error_msg = str(exc.orig).lower() if exc.orig else str(exc).lower()

    # Detect unique constraint violations
    if "unique constraint" in error_msg or "duplicate key" in error_msg:
        # Try to extract field name from error message
        field = "Resource"
        if "email" in error_msg:
            field = "Email"
        elif "username" in error_msg:
            field = "Username"

        return format_error_response(
            message=f"{field} already exists",
            status_code=status.HTTP_409_CONFLICT,
        )

    # Detect foreign key constraint violations
    if "foreign key constraint" in error_msg or "violates foreign key" in error_msg:
        return format_error_response(
            message="Referenced resource does not exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Generic database error
    return format_error_response(
        message="Database operation failed",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def error_to_http_exception(error: AppException) -> HTTPException:
    """
    Convert a custom application exception to FastAPI HTTPException.

    Args:
        error: Custom AppException or subclass

    Returns:
        FastAPI HTTPException with formatted detail

    Example:
        >>> exc = error_to_http_exception(ValidationError("Invalid input"))
        >>> raise exc
    """
    detail = format_error_response(
        message=error.message,
        status_code=error.status_code,
    )

    return HTTPException(
        status_code=error.status_code,
        detail=detail,
    )

"""
Test error handling utilities.

Tests for custom exceptions and error response formatting.
"""

import pytest
from fastapi import HTTPException, status


def test_errors_module_exists():
    """Test that errors module exists."""
    from app.utils import errors
    assert errors is not None


def test_validation_error_exception():
    """Test ValidationError custom exception."""
    from app.utils.errors import ValidationError

    error = ValidationError("Invalid email format")
    assert str(error) == "Invalid email format"
    assert error.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_not_found_error_exception():
    """Test NotFoundError custom exception."""
    from app.utils.errors import NotFoundError

    error = NotFoundError("User not found")
    assert str(error) == "User not found"
    assert error.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_error_exception():
    """Test UnauthorizedError custom exception."""
    from app.utils.errors import UnauthorizedError

    error = UnauthorizedError("Invalid credentials")
    assert str(error) == "Invalid credentials"
    assert error.status_code == status.HTTP_401_UNAUTHORIZED


def test_forbidden_error_exception():
    """Test ForbiddenError custom exception."""
    from app.utils.errors import ForbiddenError

    error = ForbiddenError("Access denied")
    assert str(error) == "Access denied"
    assert error.status_code == status.HTTP_403_FORBIDDEN


def test_conflict_error_exception():
    """Test ConflictError custom exception."""
    from app.utils.errors import ConflictError

    error = ConflictError("Email already exists")
    assert str(error) == "Email already exists"
    assert error.status_code == status.HTTP_409_CONFLICT


def test_format_error_response():
    """Test formatting error response to standard structure."""
    from app.utils.errors import format_error_response

    response = format_error_response(
        message="Validation failed",
        status_code=422,
        errors={"email": "Invalid format"}
    )

    assert response["message"] == "Validation failed"
    assert response["status_code"] == 422
    assert response["errors"] == {"email": "Invalid format"}
    assert "timestamp" in response


def test_format_error_response_minimal():
    """Test formatting error response with minimal parameters."""
    from app.utils.errors import format_error_response

    response = format_error_response(
        message="Something went wrong",
        status_code=500
    )

    assert response["message"] == "Something went wrong"
    assert response["status_code"] == 500
    assert response["errors"] is None
    assert "timestamp" in response


def test_format_validation_errors():
    """Test formatting Pydantic validation errors."""
    from app.utils.errors import format_validation_errors
    from pydantic import BaseModel, ValidationError, field_validator

    class TestModel(BaseModel):
        email: str
        age: int

        @field_validator('email')
        @classmethod
        def validate_email(cls, v):
            if '@' not in v:
                raise ValueError('Invalid email format')
            return v

    try:
        TestModel(email="invalid", age="not_a_number")
    except ValidationError as e:
        formatted = format_validation_errors(e)

        assert isinstance(formatted, dict)
        # Should have errors for both fields
        assert len(formatted) >= 1


def test_handle_database_error():
    """Test handling database-specific errors."""
    from app.utils.errors import handle_database_error
    from sqlalchemy.exc import IntegrityError

    # Mock IntegrityError for unique constraint violation
    try:
        raise IntegrityError(
            "INSERT INTO users...",
            {},
            Exception("duplicate key value violates unique constraint")
        )
    except IntegrityError as e:
        result = handle_database_error(e)

        assert result["status_code"] == 409
        assert "already exists" in result["message"].lower() or "duplicate" in result["message"].lower()


def test_handle_database_error_foreign_key():
    """Test handling database foreign key errors."""
    from app.utils.errors import handle_database_error
    from sqlalchemy.exc import IntegrityError

    # Mock IntegrityError for foreign key constraint
    try:
        raise IntegrityError(
            "INSERT INTO tasks...",
            {},
            Exception("violates foreign key constraint")
        )
    except IntegrityError as e:
        result = handle_database_error(e)

        assert result["status_code"] == 400
        assert "reference" in result["message"].lower() or "foreign key" in result["message"].lower()


def test_error_to_http_exception():
    """Test converting custom error to HTTPException."""
    from app.utils.errors import ValidationError, error_to_http_exception

    error = ValidationError("Invalid input")
    http_exc = error_to_http_exception(error)

    assert isinstance(http_exc, HTTPException)
    assert http_exc.status_code == 422
    assert "Invalid input" in str(http_exc.detail)

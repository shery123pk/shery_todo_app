"""
Test email service.

Tests for sending verification emails, password reset emails, etc.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


def test_email_service_exists():
    """Test that email service module exists."""
    from app.services import email
    assert email is not None


def test_create_verification_email():
    """Test creating email verification message."""
    from app.services.email import create_verification_email

    email_to = "user@example.com"
    token = "abc123token"

    subject, html_content = create_verification_email(email_to, token)

    assert subject is not None
    assert "verify" in subject.lower() or "verification" in subject.lower()
    assert html_content is not None
    assert token in html_content
    assert email_to in html_content or "user" in html_content.lower()


def test_create_password_reset_email():
    """Test creating password reset email."""
    from app.services.email import create_password_reset_email

    email_to = "user@example.com"
    token = "reset123token"

    subject, html_content = create_password_reset_email(email_to, token)

    assert subject is not None
    assert "reset" in subject.lower() or "password" in subject.lower()
    assert html_content is not None
    assert token in html_content


def test_create_welcome_email():
    """Test creating welcome email."""
    from app.services.email import create_welcome_email

    email_to = "newuser@example.com"
    user_name = "John Doe"

    subject, html_content = create_welcome_email(email_to, user_name)

    assert subject is not None
    assert "welcome" in subject.lower()
    assert html_content is not None
    assert user_name in html_content


@pytest.mark.asyncio
@patch('app.services.email.aiosmtplib.SMTP')
async def test_send_email_success(mock_smtp_class):
    """Test successful email sending."""
    from app.services.email import send_email

    # Mock SMTP connection
    mock_smtp = AsyncMock()
    mock_smtp.__aenter__ = AsyncMock(return_value=mock_smtp)
    mock_smtp.__aexit__ = AsyncMock(return_value=None)
    mock_smtp.send_message = AsyncMock()
    mock_smtp_class.return_value = mock_smtp

    # Send email
    result = await send_email(
        email_to="test@example.com",
        subject="Test Subject",
        html_content="<p>Test Content</p>"
    )

    assert result == True
    mock_smtp.send_message.assert_called_once()


@pytest.mark.asyncio
@patch('app.services.email.aiosmtplib.SMTP')
async def test_send_email_failure(mock_smtp_class):
    """Test email sending failure handling."""
    from app.services.email import send_email

    # Mock SMTP connection to raise exception
    mock_smtp = AsyncMock()
    mock_smtp.__aenter__ = AsyncMock(side_effect=Exception("SMTP Error"))
    mock_smtp_class.return_value = mock_smtp

    # Send email should handle error gracefully
    result = await send_email(
        email_to="test@example.com",
        subject="Test Subject",
        html_content="<p>Test Content</p>"
    )

    assert result == False


@pytest.mark.asyncio
@patch('app.services.email.send_email')
async def test_send_verification_email(mock_send):
    """Test sending verification email end-to-end."""
    from app.services.email import send_verification_email

    mock_send.return_value = True

    result = await send_verification_email("user@example.com", "token123")

    assert result == True
    mock_send.assert_called_once()
    call_args = mock_send.call_args
    assert call_args[1]['email_to'] == "user@example.com"
    assert "token123" in call_args[1]['html_content']


@pytest.mark.asyncio
@patch('app.services.email.send_email')
async def test_send_password_reset_email(mock_send):
    """Test sending password reset email end-to-end."""
    from app.services.email import send_password_reset_email

    mock_send.return_value = True

    result = await send_password_reset_email("user@example.com", "reset456")

    assert result == True
    mock_send.assert_called_once()
    call_args = mock_send.call_args
    assert call_args[1]['email_to'] == "user@example.com"
    assert "reset456" in call_args[1]['html_content']


def test_email_config_loaded():
    """Test that email configuration is loaded from settings."""
    from app.config import settings

    assert settings.smtp_host is not None
    assert settings.smtp_port is not None
    assert settings.from_email is not None

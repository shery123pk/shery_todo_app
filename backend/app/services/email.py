"""
Email Service

Handles sending transactional emails (verification, password reset, welcome).
Uses aiosmtplib for async SMTP operations.
Author: Sharmeen Asif
"""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


def create_verification_email(email_to: str, token: str) -> tuple[str, str]:
    """
    Create email verification message content.

    Args:
        email_to: Recipient email address
        token: Verification token

    Returns:
        Tuple of (subject, html_content)

    Example:
        >>> subject, html = create_verification_email("user@example.com", "token123")
    """
    subject = "Verify Your Email - Project Management System"

    # Construct verification URL
    verification_url = f"{settings.frontend_url}/auth/verify-email?token={token}"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Verify Your Email Address</h2>
            <p>Thank you for signing up! Please verify your email address by clicking the button below:</p>
            <div style="margin: 30px 0;">
                <a href="{verification_url}"
                   style="background-color: #4F46E5; color: white; padding: 12px 24px;
                          text-decoration: none; border-radius: 6px; display: inline-block;">
                    Verify Email
                </a>
            </div>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #666;">{verification_url}</p>
            <p style="margin-top: 30px; color: #666; font-size: 14px;">
                This link will expire in 24 hours. If you didn't create an account, you can safely ignore this email.
            </p>
            <p style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; color: #999; font-size: 12px;">
                Project Management System
            </p>
        </div>
    </body>
    </html>
    """

    return subject, html_content


def create_password_reset_email(email_to: str, token: str) -> tuple[str, str]:
    """
    Create password reset email content.

    Args:
        email_to: Recipient email address
        token: Password reset token

    Returns:
        Tuple of (subject, html_content)

    Example:
        >>> subject, html = create_password_reset_email("user@example.com", "reset123")
    """
    subject = "Reset Your Password - Project Management System"

    # Construct reset URL
    reset_url = f"{settings.frontend_url}/auth/reset-password?token={token}"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Reset Your Password</h2>
            <p>We received a request to reset your password. Click the button below to create a new password:</p>
            <div style="margin: 30px 0;">
                <a href="{reset_url}"
                   style="background-color: #DC2626; color: white; padding: 12px 24px;
                          text-decoration: none; border-radius: 6px; display: inline-block;">
                    Reset Password
                </a>
            </div>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #666;">{reset_url}</p>
            <p style="margin-top: 30px; color: #666; font-size: 14px;">
                This link will expire in 1 hour. If you didn't request a password reset, you can safely ignore this email.
            </p>
            <p style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; color: #999; font-size: 12px;">
                Project Management System
            </p>
        </div>
    </body>
    </html>
    """

    return subject, html_content


def create_welcome_email(email_to: str, user_name: str) -> tuple[str, str]:
    """
    Create welcome email content for new users.

    Args:
        email_to: Recipient email address
        user_name: User's full name

    Returns:
        Tuple of (subject, html_content)

    Example:
        >>> subject, html = create_welcome_email("user@example.com", "John Doe")
    """
    subject = "Welcome to Project Management System!"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Welcome, {user_name}!</h2>
            <p>Your account has been successfully created. You're now ready to start managing your projects.</p>
            <h3>Getting Started</h3>
            <ul>
                <li>Create your first organization</li>
                <li>Invite team members</li>
                <li>Create projects and boards</li>
                <li>Start tracking tasks</li>
            </ul>
            <div style="margin: 30px 0;">
                <a href="{settings.frontend_url}/dashboard"
                   style="background-color: #10B981; color: white; padding: 12px 24px;
                          text-decoration: none; border-radius: 6px; display: inline-block;">
                    Go to Dashboard
                </a>
            </div>
            <p style="margin-top: 30px; color: #666; font-size: 14px;">
                Need help? Check out our documentation or contact support.
            </p>
            <p style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; color: #999; font-size: 12px;">
                Project Management System
            </p>
        </div>
    </body>
    </html>
    """

    return subject, html_content


async def send_email(
    email_to: str,
    subject: str,
    html_content: str,
) -> bool:
    """
    Send an email using SMTP (async).

    Args:
        email_to: Recipient email address
        subject: Email subject line
        html_content: HTML content of the email

    Returns:
        True if email sent successfully, False otherwise

    Example:
        >>> await send_email("user@example.com", "Test", "<p>Hello</p>")
        True
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.from_email
        message["To"] = email_to

        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        # Send email using async SMTP
        async with aiosmtplib.SMTP(
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            use_tls=False,  # Use STARTTLS instead
        ) as smtp:
            # Start TLS if not using port 465
            if settings.smtp_port != 465:
                await smtp.starttls()

            # Login if credentials provided
            if settings.smtp_username and settings.smtp_password:
                await smtp.login(settings.smtp_username, settings.smtp_password)

            # Send message
            await smtp.send_message(message)

        return True

    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"Failed to send email to {email_to}: {str(e)}")
        return False


async def send_verification_email(email_to: str, token: str) -> bool:
    """
    Send email verification email.

    Args:
        email_to: Recipient email address
        token: Verification token

    Returns:
        True if sent successfully, False otherwise

    Example:
        >>> await send_verification_email("user@example.com", "token123")
        True
    """
    subject, html_content = create_verification_email(email_to, token)
    return await send_email(email_to, subject, html_content)


async def send_password_reset_email(email_to: str, token: str) -> bool:
    """
    Send password reset email.

    Args:
        email_to: Recipient email address
        token: Password reset token

    Returns:
        True if sent successfully, False otherwise

    Example:
        >>> await send_password_reset_email("user@example.com", "reset123")
        True
    """
    subject, html_content = create_password_reset_email(email_to, token)
    return await send_email(email_to, subject, html_content)


async def send_welcome_email(email_to: str, user_name: str) -> bool:
    """
    Send welcome email to new user.

    Args:
        email_to: Recipient email address
        user_name: User's full name

    Returns:
        True if sent successfully, False otherwise

    Example:
        >>> await send_welcome_email("user@example.com", "John Doe")
        True
    """
    subject, html_content = create_welcome_email(email_to, user_name)
    return await send_email(email_to, subject, html_content)

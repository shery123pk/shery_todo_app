"""
Email Notification Service for Task Reminders
Sends task reminder emails using SMTP
Author: Sharmeen Asif
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Load .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USERNAME)

# Check if email is configured
email_configured = bool(SMTP_USERNAME and SMTP_PASSWORD)

if email_configured:
    print(f"[SUCCESS] Email notifications enabled (SMTP: {SMTP_HOST})")
else:
    print("[INFO] Email notifications disabled. Set SMTP credentials in .env to enable.")


async def send_task_reminder_email(user_email: str, task_title: str, due_date: datetime):
    """
    Send a task reminder email.

    Args:
        user_email: User's email address
        task_title: Title of the task
        due_date: When the task is due

    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not email_configured:
        print("[WARNING] Email not configured. Cannot send reminder.")
        return False

    if not user_email:
        print("[WARNING] No user email provided")
        return False

    try:
        # Format due date
        due_str = due_date.strftime("%B %d, %Y at %I:%M %p")

        # Create email
        message = MIMEMultipart("alternative")
        message["Subject"] = f"🔔 Task Reminder: {task_title}"
        message["From"] = FROM_EMAIL
        message["To"] = user_email

        # Plain text version
        text_content = f"""
Task Reminder
=============

You have a task due soon:

📌 {task_title}
⏰ Due: {due_str}

Don't forget to complete this task!

---
TaskFlow - Your AI Task Assistant
"""

        # HTML version
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }}
        .content {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .icon {{
            font-size: 48px;
        }}
        .task-title {{
            font-size: 20px;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
        }}
        .due-date {{
            background: #f7fafc;
            padding: 15px;
            border-left: 4px solid #667eea;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <div class="header">
                <div class="icon">🔔</div>
                <h1 style="color: #667eea; margin: 10px 0;">Task Reminder</h1>
            </div>

            <p>You have a task due soon:</p>

            <div class="task-title">
                📌 {task_title}
            </div>

            <div class="due-date">
                <strong>⏰ Due:</strong> {due_str}
            </div>

            <p>Don't forget to complete this task!</p>

            <div class="footer">
                <p>TaskFlow - Your AI Task Assistant</p>
                <p>This is an automated reminder email.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

        # Attach both versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)

        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)

        print(f"[SUCCESS] Reminder email sent to {user_email} for task: {task_title}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send reminder email: {e}")
        return False


async def send_task_created_email(user_email: str, task_title: str, due_date: datetime = None):
    """
    Send confirmation email when a task with reminder is created.

    Args:
        user_email: User's email address
        task_title: Title of the task
        due_date: When the task is due (optional)

    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not email_configured or not user_email:
        return False

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"✅ Task Created: {task_title}"
        message["From"] = FROM_EMAIL
        message["To"] = user_email

        due_str = due_date.strftime("%B %d, %Y at %I:%M %p") if due_date else "Not set"

        text_content = f"""
Task Created Successfully
========================

Your task has been created:

📌 {task_title}
⏰ Reminder: {due_str}

You'll receive a reminder email 30 minutes before it's due.

---
TaskFlow - Your AI Task Assistant
"""

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .content {{ background: white; padding: 30px; border-radius: 8px; }}
        .success {{ color: #48bb78; font-size: 48px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <div class="success">✅</div>
            <h2 style="text-align: center; color: #667eea;">Task Created!</h2>
            <p>Your task has been created successfully:</p>
            <h3>📌 {task_title}</h3>
            <p><strong>⏰ Reminder:</strong> {due_str}</p>
            <p>You'll receive a reminder email 30 minutes before it's due.</p>
        </div>
    </div>
</body>
</html>
"""

        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)

        print(f"[SUCCESS] Task creation email sent to {user_email}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send task creation email: {e}")
        return False

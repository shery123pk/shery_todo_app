"""
WhatsApp Notification Service using Twilio
Sends task reminders to WhatsApp
Author: Sharmeen Asif
"""

import os
from twilio.rest import Client
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")  # Twilio Sandbox number
USER_WHATSAPP_NUMBER = os.getenv("USER_WHATSAPP_NUMBER")  # Your WhatsApp number

# Initialize Twilio client
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    try:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print("[SUCCESS] Twilio WhatsApp client initialized")
    except Exception as e:
        print(f"[WARNING] Failed to initialize Twilio: {e}")
else:
    print("[INFO] Twilio credentials not found. WhatsApp notifications disabled.")


async def send_whatsapp_reminder(task_title: str, task_id: str, due_date: str, user_phone: str = None):
    """
    Send a WhatsApp reminder for a task.

    Args:
        task_title: Title of the task
        task_id: ID of the task
        due_date: Due date/time of the task
        user_phone: User's WhatsApp number (optional, uses env var if not provided)

    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not twilio_client:
        print("[WARNING] Twilio client not initialized. Cannot send WhatsApp message.")
        return False

    phone_number = user_phone or USER_WHATSAPP_NUMBER

    if not phone_number:
        print("[WARNING] No WhatsApp phone number configured")
        return False

    # Ensure phone number has whatsapp: prefix
    if not phone_number.startswith("whatsapp:"):
        phone_number = f"whatsapp:{phone_number}"

    message_body = f"""🔔 *Task Reminder*

📌 *{task_title}*

⏰ Due: {due_date}

Don't forget to complete this task!

---
TaskFlow AI Assistant"""

    try:
        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_FROM,
            to=phone_number
        )

        print(f"[SUCCESS] WhatsApp reminder sent for task {task_id}: {message.sid}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send WhatsApp reminder: {e}")
        return False


async def send_task_created_notification(task_title: str, due_date: str = None, user_phone: str = None):
    """Send notification when a task is created with a due date."""
    if not twilio_client or not (user_phone or USER_WHATSAPP_NUMBER):
        return False

    phone_number = user_phone or USER_WHATSAPP_NUMBER
    if not phone_number.startswith("whatsapp:"):
        phone_number = f"whatsapp:{phone_number}"

    message_body = f"""✅ *Task Created*

📌 *{task_title}*
"""

    if due_date:
        message_body += f"\n⏰ Reminder set for: {due_date}"

    message_body += "\n\n---\nTaskFlow AI Assistant"

    try:
        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_FROM,
            to=phone_number
        )
        print(f"[SUCCESS] Task creation notification sent: {message.sid}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send task notification: {e}")
        return False

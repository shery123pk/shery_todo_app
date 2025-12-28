"""
Background Task Reminder Checker
Periodically checks for due tasks and sends WhatsApp reminders
Author: Sharmeen Asif
"""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.task import Task
from app.models.user import User
from app.services.email_notifications import send_task_reminder_email
from app.database import async_session_maker


async def check_and_send_reminders():
    """
    Check for tasks that are due soon and haven't had reminders sent.
    Sends WhatsApp reminders for tasks due within the next 30 minutes.
    """
    print("[REMINDER] Checking for due tasks...")

    async with async_session_maker() as db:
        try:
            # Get current time and 30 minutes from now
            now = datetime.utcnow()
            reminder_window = now + timedelta(minutes=30)

            # Find tasks that:
            # 1. Have a due_date
            # 2. Due date is between now and 30 minutes from now
            # 3. Haven't had a reminder sent yet
            # 4. Are not completed
            query = select(Task).where(
                and_(
                    Task.due_date.isnot(None),
                    Task.due_date <= reminder_window,
                    Task.due_date >= now,
                    Task.reminder_sent == False,
                    Task.completed == False
                )
            )

            result = await db.execute(query)
            tasks_to_remind = result.scalars().all()

            print(f"[REMINDER] Found {len(tasks_to_remind)} tasks needing reminders")

            for task in tasks_to_remind:
                # Get user email
                user_result = await db.execute(select(User).where(User.id == task.user_id))
                user = user_result.scalar_one_or_none()

                if user and user.email:
                    # Send email reminder
                    success = await send_task_reminder_email(
                        user_email=user.email,
                        task_title=task.title,
                        due_date=task.due_date
                    )

                    if success:
                        # Mark reminder as sent
                        task.reminder_sent = True
                        await db.commit()
                        print(f"[REMINDER] Sent email reminder for task: {task.title}")

        except Exception as e:
            print(f"[REMINDER ERROR] {e}")
            await db.rollback()


async def start_reminder_service():
    """
    Start the background reminder service that checks every 10 minutes.
    """
    print("[REMINDER SERVICE] Starting...")

    while True:
        try:
            await check_and_send_reminders()
        except Exception as e:
            print(f"[REMINDER SERVICE ERROR] {e}")

        # Wait 10 minutes before next check
        await asyncio.sleep(600)  # 600 seconds = 10 minutes

"""
Chatbot API Routes with Function Calling
Phase III: AI-Powered Natural Language Task Management
Author: Sharmeen Asif
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import httpx
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from dateutil import parser as date_parser

from ..dependencies import get_current_user, get_async_session
from ..models.user import User
from ..models.task import Task as TaskModel
from ..schemas.task import TaskCreate, TaskUpdate

# Load .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])

# Initialize OpenAI client if API key is available
openai_client = None
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    try:
        openai_client = OpenAI(api_key=openai_api_key)
        print("[SUCCESS] OpenAI client initialized for chatbot with function calling")
    except Exception as e:
        print(f"[WARNING] Failed to initialize OpenAI: {e}")
else:
    print("[INFO] OPENAI_API_KEY not found in environment")


class ChatMessage(BaseModel):
    """Chat message model"""
    message: str


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    error: Optional[str] = None
    tasks: Optional[List[dict]] = None


# Define function schemas for OpenAI
TASK_FUNCTIONS = [
    {
        "name": "get_tasks",
        "description": "Get all tasks for the user. Use this when user asks to show, list, view, or see their tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "completed": {
                    "type": "boolean",
                    "description": "Filter by completion status. True for completed tasks, false for incomplete tasks. Omit to get all tasks."
                }
            },
            "required": []
        }
    },
    {
        "name": "create_task",
        "description": "Create a new task. Use this when user asks to add, create, make, or set a task.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The task title or description"
                },
                "description": {
                    "type": "string",
                    "description": "Additional details about the task"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Task priority level"
                },
                "category": {
                    "type": "string",
                    "description": "Task category (e.g., work, personal, shopping)"
                },
                "due_date": {
                    "type": "string",
                    "description": "Due date in ISO format (e.g., '2025-12-30T15:00:00'). Parse from natural language like 'tomorrow 3pm', 'next Monday 9am', 'in 2 hours'."
                },
                "is_recurring": {
                    "type": "boolean",
                    "description": "Whether this task repeats automatically (e.g., 'weekly meeting', 'daily standup')"
                },
                "recurrence_pattern": {
                    "type": "string",
                    "enum": ["daily", "weekly", "monthly"],
                    "description": "How often the task repeats: daily, weekly, or monthly"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "update_task",
        "description": "Update an existing task. Use this when user asks to mark complete, update, change, or modify a task.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The ID of the task to update"
                },
                "completed": {
                    "type": "boolean",
                    "description": "Mark task as completed or incomplete"
                },
                "title": {
                    "type": "string",
                    "description": "New task title"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "New priority level"
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task. Use this when user asks to delete, remove, or get rid of a task.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The ID of the task to delete"
                }
            },
            "required": ["task_id"]
        }
    }
]


# Task operation functions
async def get_tasks_function(db: AsyncSession, user_id: str, completed: Optional[bool] = None):
    """Get tasks from database"""
    query = select(TaskModel).where(TaskModel.user_id == user_id)

    if completed is not None:
        query = query.where(TaskModel.completed == completed)

    result = await db.execute(query)
    tasks = result.scalars().all()

    task_list = []
    for task in tasks:
        task_list.append({
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "category": task.category,
            "created_at": task.created_at.isoformat() if task.created_at else None
        })

    return task_list


async def create_task_function(db: AsyncSession, user_id: str, **kwargs):
    """Create a new task"""
    # Parse due_date if provided
    due_date = None
    if kwargs.get("due_date"):
        try:
            due_date = date_parser.parse(kwargs.get("due_date"))
        except:
            # If parsing fails, set it to None
            due_date = None

    task = TaskModel(
        user_id=user_id,
        title=kwargs.get("title"),
        description=kwargs.get("description"),
        priority=kwargs.get("priority", "medium"),
        category=kwargs.get("category"),
        due_date=due_date,
        is_recurring=kwargs.get("is_recurring", False),
        recurrence_pattern=kwargs.get("recurrence_pattern"),
        completed=False
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "priority": task.priority,
        "category": task.category,
        "due_date": task.due_date.isoformat() if task.due_date else None
    }


async def update_task_function(db: AsyncSession, user_id: str, task_id: str, **kwargs):
    """Update an existing task"""
    result = await db.execute(
        select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise ValueError(f"Task with ID {task_id} not found")

    # Check if completing a recurring task
    is_completing_recurring = (
        kwargs.get("completed") is True and
        task.is_recurring and
        task.recurrence_pattern and
        task.due_date
    )

    if "completed" in kwargs:
        task.completed = kwargs["completed"]
    if "title" in kwargs:
        task.title = kwargs["title"]
    if "description" in kwargs:
        task.description = kwargs["description"]
    if "priority" in kwargs:
        task.priority = kwargs["priority"]
    if "category" in kwargs:
        task.category = kwargs["category"]

    # If completing a recurring task, create next occurrence
    if is_completing_recurring:
        from dateutil.relativedelta import relativedelta
        from datetime import datetime

        # Calculate next due date
        next_due_date = task.due_date
        if task.recurrence_pattern == "daily":
            next_due_date = task.due_date + relativedelta(days=1)
        elif task.recurrence_pattern == "weekly":
            next_due_date = task.due_date + relativedelta(weeks=1)
        elif task.recurrence_pattern == "monthly":
            next_due_date = task.due_date + relativedelta(months=1)

        # Create next occurrence
        next_task = TaskModel(
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=False,
            priority=task.priority,
            category=task.category,
            due_date=next_due_date,
            is_recurring=True,
            recurrence_pattern=task.recurrence_pattern,
            parent_task_id=task.id,
            reminder_sent=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(next_task)

    await db.commit()
    await db.refresh(task)

    return {
        "id": str(task.id),
        "title": task.title,
        "completed": task.completed,
        "priority": task.priority
    }


async def delete_task_function(db: AsyncSession, user_id: str, task_id: str):
    """Delete a task"""
    result = await db.execute(
        select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise ValueError(f"Task with ID {task_id} not found")

    await db.delete(task)
    await db.commit()

    return {"success": True, "message": f"Task '{task.title}' deleted successfully"}


@router.post("/chat", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Natural language task management chatbot with function calling.

    Examples:
    - "Show me all my tasks"
    - "Add buy groceries to my list"
    - "Mark the first task as complete"
    - "Delete the shopping task"
    """
    try:
        if not openai_client:
            return ChatResponse(
                response="AI chatbot is not configured. Please set OPENAI_API_KEY in your backend/.env file.",
                error="No AI service configured"
            )

        # First, get current tasks to help AI understand context
        current_tasks = await get_tasks_function(db, str(current_user.id))

        # Build context about current tasks with mapping
        task_context = ""
        task_number_map = {}  # Map position number to task ID
        if current_tasks:
            task_context = "\n\nCurrent tasks (use the full task_id shown):\n"
            for i, task in enumerate(current_tasks[:20], 1):
                status = "✅" if task["completed"] else "⬜"
                task_context += f"{i}. {status} {task['title']} | task_id: {task['id']}\n"
                task_number_map[i] = task['id']
        else:
            task_context = "\n\nThe user currently has no tasks."

        # Detect language from user message
        def detect_language(text: str) -> str:
            """Simple language detection for Urdu vs English"""
            # Check for Urdu unicode range (U+0600 to U+06FF)
            urdu_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
            if urdu_chars > len(text) * 0.3:  # If 30%+ of chars are Urdu
                return "urdu"
            return "english"

        user_language = detect_language(message.message)

        # Build system prompt based on language
        if user_language == "urdu":
            system_prompt = f"""آپ ایک مددگار AI ٹاسک مینجمنٹ اسسٹنٹ ہیں جو یوزر کے ٹاسک ڈیٹا بیس تک رسائی رکھتے ہیں۔

آپ یہ کام کر سکتے ہیں:
- ٹاسک دیکھیں (get_tasks)
- نئے ٹاسک بنائیں (create_task)
- ٹاسک اپ ڈیٹ کریں (update_task)
- ٹاسک ڈیلیٹ کریں (delete_task)

اہم: جب یوزر "ٹاسک 1"، "پہلا ٹاسک"، "ٹاسک 2 ڈیلیٹ کریں" وغیرہ کہے:
1. نیچے دی گئی نمبر والی فہرست دیکھیں
2. جس ٹاسک نمبر کا ذکر کیا گیا ہے اسے تلاش کریں
3. مکمل task_id استعمال کریں (task_id: کے بعد لمبی UUID سٹرنگ)
4. وہی مکمل ID update_task یا delete_task میں دیں

مثال: اگر یوزر "ٹاسک 1 ڈیلیٹ کریں" کہے اور ٹاسک 1 میں "task_id: 123e4567-e89b-12d3-a456-426614174000" دکھائی دے،
تو مکمل ID استعمال کریں: delete_task(task_id="123e4567-e89b-12d3-a456-426614174000")

ٹاسک مکمل کرنے کے لیے، task_id اور completed: true کے ساتھ update_task استعمال کریں۔
ہمیشہ دوستانہ رہیں اور تصدیق کریں کہ آپ نے کیا کیا۔ اسے دلچسپ بنانے کے لیے emojis استعمال کریں!

یوزر کے موجودہ ٹاسک:
{task_context}

یوزر کو اردو میں جواب دیں۔"""
        else:
            system_prompt = f"""You are a helpful AI task management assistant with access to the user's task database.

You can perform these operations:
- View tasks (get_tasks)
- Create new tasks (create_task)
- Update tasks (update_task)
- Delete tasks (delete_task)

IMPORTANT: When user says "task 1", "first task", "delete task 2", etc:
1. Look at the numbered list below
2. Find the task number they mentioned
3. Use the FULL task_id shown (the long UUID string after "task_id:")
4. Pass that exact task_id to update_task or delete_task

Example: If user says "delete task 1" and task 1 shows "task_id: 123e4567-e89b-12d3-a456-426614174000",
use that FULL ID: delete_task(task_id="123e4567-e89b-12d3-a456-426614174000")

When marking tasks complete, use update_task with the task_id and completed: true.
Always be friendly and confirm what you did. Use emojis to make it engaging!
{task_context}

Respond to the user in English."""

        # Call OpenAI with function calling
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message.message
            }
        ]

        # Initial API call with function calling
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=[{"type": "function", "function": func} for func in TASK_FUNCTIONS],
            tool_choice="auto",
            temperature=0.7,
        )

        assistant_message = response.choices[0].message

        # Check if AI wants to call a function
        if assistant_message.tool_calls:
            # Execute the function calls
            function_results = []

            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"[CHATBOT] Calling function: {function_name} with args: {function_args}")

                try:
                    # Execute the appropriate function
                    if function_name == "get_tasks":
                        result = await get_tasks_function(db, str(current_user.id), **function_args)
                    elif function_name == "create_task":
                        result = await create_task_function(db, str(current_user.id), **function_args)
                    elif function_name == "update_task":
                        result = await update_task_function(db, str(current_user.id), **function_args)
                    elif function_name == "delete_task":
                        result = await delete_task_function(db, str(current_user.id), **function_args)
                    else:
                        result = {"error": f"Unknown function: {function_name}"}

                    function_results.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(result)
                    })

                except Exception as e:
                    print(f"[CHATBOT] Function error: {e}")
                    function_results.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps({"error": str(e)})
                    })

            # Add function results to messages
            messages.append(assistant_message.model_dump())
            for result in function_results:
                messages.append({
                    "role": "tool",
                    "tool_call_id": result["tool_call_id"],
                    "content": result["output"]
                })

            # Get final response from AI
            final_response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
            )

            final_message = final_response.choices[0].message.content

            return ChatResponse(
                response=final_message,
                tasks=current_tasks if function_name == "get_tasks" else None
            )

        else:
            # No function call, just return the response
            return ChatResponse(response=assistant_message.content or "I'm here to help!")

    except Exception as e:
        print(f"[CHATBOT] Error: {e}")
        import traceback
        traceback.print_exc()
        return ChatResponse(
            response=f"Sorry, I encountered an error: {str(e)}",
            error=str(e)
        )


@router.get("/status")
async def chatbot_status():
    """Check if chatbot service is available"""
    if openai_client:
        return {
            "available": True,
            "message": "AI Chatbot is ready with function calling (GPT-4)",
            "provider": "openai",
            "features": ["get_tasks", "create_task", "update_task", "delete_task"]
        }

    return {
        "available": False,
        "message": "Chatbot not configured",
        "instructions": "Set OPENAI_API_KEY in backend/.env to enable AI chatbot"
    }

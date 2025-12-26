"""
Chatbot API Routes
Phase III: AI-Powered Chatbot Integration
Author: Sharmeen Asif
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import os

from ..dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])


class ChatMessage(BaseModel):
    """Chat message model"""
    message: str


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    error: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """
    Send a message to the AI chatbot.

    The chatbot can perform task operations using natural language:
    - "Show me all my tasks"
    - "Add buy groceries to my list"
    - "Mark task 3 as complete"
    - "Delete the shopping task"
    """
    try:
        # For now, return a mock response
        # In production, this would integrate with the chatbot service

        # Check if chatbot service is available
        chatbot_url = os.getenv("CHATBOT_API_URL")

        if not chatbot_url:
            # Return helpful mock responses for common queries
            user_message = message.message.lower()

            if "hello" in user_message or "hi" in user_message:
                return ChatResponse(
                    response="Hello! I'm your AI task assistant. I can help you manage your todos using natural language. Try asking me to 'show all tasks' or 'add a new task'."
                )
            elif "help" in user_message:
                return ChatResponse(
                    response="I can help you with:\n- Listing tasks: 'show me all tasks'\n- Creating tasks: 'add buy milk to my list'\n- Updating tasks: 'mark task 1 as complete'\n- Deleting tasks: 'delete the shopping task'\n- Searching: 'find tasks about groceries'"
                )
            elif "task" in user_message and "show" in user_message:
                return ChatResponse(
                    response="I can see you want to view your tasks. Please use the main Tasks page for now, or integrate the full chatbot service with ANTHROPIC_API_KEY."
                )
            else:
                return ChatResponse(
                    response=f"I understand you said: '{message.message}'. The full chatbot service requires ANTHROPIC_API_KEY to be configured. For now, please use the Tasks page to manage your todos."
                )

        # If chatbot service is available, forward the request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{chatbot_url}/chat",
                json={
                    "message": message.message,
                    "user_id": str(current_user.id)
                }
            )

            if response.status_code == 200:
                data = response.json()
                return ChatResponse(response=data.get("response", "No response"))
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Chatbot service error"
                )

    except httpx.RequestError as e:
        # Chatbot service not available
        return ChatResponse(
            response="The AI chatbot service is currently offline. Please use the main Tasks page to manage your todos.",
            error=str(e)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def chatbot_status():
    """Check if chatbot service is available"""
    chatbot_url = os.getenv("CHATBOT_API_URL")

    if not chatbot_url:
        return {
            "available": False,
            "message": "Chatbot service URL not configured (CHATBOT_API_URL)",
            "instructions": "Set ANTHROPIC_API_KEY and deploy the chatbot service to enable AI assistance"
        }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{chatbot_url}/health")

            if response.status_code == 200:
                return {
                    "available": True,
                    "message": "Chatbot service is online"
                }
            else:
                return {
                    "available": False,
                    "message": f"Chatbot service returned status {response.status_code}"
                }
    except httpx.RequestError:
        return {
            "available": False,
            "message": "Chatbot service is not reachable"
        }

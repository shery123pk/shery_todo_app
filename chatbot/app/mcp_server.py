"""
MCP Server for Todo Operations
Provides tools for AI chatbot to manage todos via Model Context Protocol
Author: Sharmeen Asif
"""

import httpx
from typing import Any, Optional
import os
from mcp.server import Server
from mcp.types import Tool, TextContent


# Backend API configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")


class TodoMCPServer:
    """MCP Server providing todo management tools for AI agents"""

    def __init__(self, session_token: Optional[str] = None):
        """
        Initialize MCP server with optional authentication.

        Args:
            session_token: JWT session token for authenticated requests
        """
        self.session_token = session_token
        self.server = Server("todo-mcp-server")
        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools for todo management"""
            return [
                Tool(
                    name="list_tasks",
                    description="Get all tasks for the current user. Can filter by completion status.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "completed": {
                                "type": "boolean",
                                "description": "Filter by completion status (true/false/null for all)"
                            }
                        }
                    }
                ),
                Tool(
                    name="create_task",
                    description="Create a new task with title and optional details",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Task title (required)"
                            },
                            "description": {
                                "type": "string",
                                "description": "Task description (optional)"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Task priority (optional)"
                            },
                            "category": {
                                "type": "string",
                                "description": "Task category (optional)"
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Task tags (optional)"
                            }
                        },
                        "required": ["title"]
                    }
                ),
                Tool(
                    name="update_task",
                    description="Update an existing task by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "UUID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title (optional)"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description (optional)"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Completion status (optional)"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New priority (optional)"
                            }
                        },
                        "required": ["task_id"]
                    }
                ),
                Tool(
                    name="delete_task",
                    description="Delete a task by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "UUID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                ),
                Tool(
                    name="search_tasks",
                    description="Search tasks by keyword in title or description",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search keyword"
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Execute tool calls"""

            if name == "list_tasks":
                return await self._list_tasks(arguments.get("completed"))
            elif name == "create_task":
                return await self._create_task(arguments)
            elif name == "update_task":
                return await self._update_task(arguments)
            elif name == "delete_task":
                return await self._delete_task(arguments["task_id"])
            elif name == "search_tasks":
                return await self._search_tasks(arguments["query"])
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def _list_tasks(self, completed: Optional[bool] = None) -> list[TextContent]:
        """List all tasks"""
        async with httpx.AsyncClient() as client:
            params = {}
            if completed is not None:
                params["completed"] = str(completed).lower()

            response = await client.get(
                f"{API_URL}/api/tasks",
                params=params,
                cookies={"session_token": self.session_token} if self.session_token else {}
            )

            if response.status_code == 200:
                data = response.json()
                tasks = data["tasks"]

                if not tasks:
                    return [TextContent(
                        type="text",
                        text="No tasks found."
                    )]

                result = f"Found {len(tasks)} tasks:\n\n"
                for task in tasks:
                    status = "✓" if task["completed"] else "☐"
                    result += f"{status} {task['title']}\n"
                    if task.get("description"):
                        result += f"   Description: {task['description']}\n"
                    if task.get("priority"):
                        result += f"   Priority: {task['priority']}\n"
                    if task.get("tags"):
                        result += f"   Tags: {', '.join(task['tags'])}\n"
                    result += f"   ID: {task['id']}\n\n"

                return [TextContent(type="text", text=result)]
            else:
                return [TextContent(
                    type="text",
                    text=f"Error fetching tasks: {response.status_code}"
                )]

    async def _create_task(self, data: dict[str, Any]) -> list[TextContent]:
        """Create a new task"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/api/tasks",
                json=data,
                cookies={"session_token": self.session_token} if self.session_token else {}
            )

            if response.status_code == 201:
                task = response.json()
                return [TextContent(
                    type="text",
                    text=f"✓ Created task: {task['title']}\nID: {task['id']}"
                )]
            else:
                error_detail = response.json().get("detail", "Unknown error")
                return [TextContent(
                    type="text",
                    text=f"Error creating task: {error_detail}"
                )]

    async def _update_task(self, data: dict[str, Any]) -> list[TextContent]:
        """Update an existing task"""
        task_id = data.pop("task_id")

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{API_URL}/api/tasks/{task_id}",
                json=data,
                cookies={"session_token": self.session_token} if self.session_token else {}
            )

            if response.status_code == 200:
                task = response.json()
                return [TextContent(
                    type="text",
                    text=f"✓ Updated task: {task['title']}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Error updating task: {response.status_code}"
                )]

    async def _delete_task(self, task_id: str) -> list[TextContent]:
        """Delete a task"""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{API_URL}/api/tasks/{task_id}",
                cookies={"session_token": self.session_token} if self.session_token else {}
            )

            if response.status_code == 204:
                return [TextContent(
                    type="text",
                    text=f"✓ Deleted task: {task_id}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Error deleting task: {response.status_code}"
                )]

    async def _search_tasks(self, query: str) -> list[TextContent]:
        """Search tasks by keyword"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_URL}/api/tasks",
                cookies={"session_token": self.session_token} if self.session_token else {}
            )

            if response.status_code == 200:
                data = response.json()
                tasks = data["tasks"]

                # Filter tasks by query
                query_lower = query.lower()
                matching_tasks = [
                    task for task in tasks
                    if query_lower in task["title"].lower()
                    or (task.get("description") and query_lower in task["description"].lower())
                ]

                if not matching_tasks:
                    return [TextContent(
                        type="text",
                        text=f"No tasks found matching '{query}'"
                    )]

                result = f"Found {len(matching_tasks)} tasks matching '{query}':\n\n"
                for task in matching_tasks:
                    status = "✓" if task["completed"] else "☐"
                    result += f"{status} {task['title']}\n"
                    result += f"   ID: {task['id']}\n\n"

                return [TextContent(type="text", text=result)]
            else:
                return [TextContent(
                    type="text",
                    text=f"Error searching tasks: {response.status_code}"
                )]

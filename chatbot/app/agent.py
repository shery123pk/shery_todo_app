"""
AI Todo Agent using Anthropic Claude
Provides natural language interface for todo management
Author: Sharmeen Asif
"""

import os
from typing import Optional
from anthropic import Anthropic
from app.mcp_server import TodoMCPServer


class TodoAgent:
    """AI agent for natural language todo management"""

    def __init__(self, session_token: Optional[str] = None):
        """
        Initialize AI todo agent.

        Args:
            session_token: JWT session token for authenticated API requests
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = Anthropic(api_key=api_key)
        self.mcp_server = TodoMCPServer(session_token=session_token)
        self.conversation_history: list[dict] = []

        # System prompt for the AI agent
        self.system_prompt = """You are a helpful AI assistant for managing todo tasks.

You have access to the following tools:
- list_tasks: View all tasks (can filter by completed status)
- create_task: Create a new task with title, description, priority, category, and tags
- update_task: Update an existing task by ID
- delete_task: Delete a task by ID
- search_tasks: Search tasks by keyword

When users ask to manage their todos, use these tools to help them.

Examples:
- "Show my tasks" → use list_tasks
- "Add buy groceries to my list" → use create_task with title "buy groceries"
- "Mark task X as done" → use update_task with completed=true
- "Delete the grocery task" → search for it, then delete_task
- "What tasks do I have about work?" → use search_tasks with query "work"

Always be friendly and helpful. Confirm actions before executing them.
Provide clear summaries of what you've done."""

    async def chat(self, user_message: str) -> str:
        """
        Process a user message and return AI response.

        Args:
            user_message: User's natural language input

        Returns:
            AI agent's response
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Get available tools
        tools = await self.mcp_server.server.list_tools()()

        # Convert MCP tools to Anthropic tool format
        anthropic_tools = []
        for tool in tools:
            anthropic_tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            })

        # Call Claude with tools
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=self.system_prompt,
            messages=self.conversation_history,
            tools=anthropic_tools
        )

        # Process tool calls
        while response.stop_reason == "tool_use":
            # Extract tool calls from response
            tool_results = []

            for content_block in response.content:
                if content_block.type == "tool_use":
                    tool_name = content_block.name
                    tool_input = content_block.input

                    # Execute tool via MCP server
                    result = await self.mcp_server.server.call_tool()(
                        name=tool_name,
                        arguments=tool_input
                    )

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": result[0].text
                    })

            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })

            # Add tool results to history
            self.conversation_history.append({
                "role": "user",
                "content": tool_results
            })

            # Continue conversation with tool results
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=self.system_prompt,
                messages=self.conversation_history,
                tools=anthropic_tools
            )

        # Extract final text response
        final_response = ""
        for content_block in response.content:
            if hasattr(content_block, "text"):
                final_response += content_block.text

        # Add final response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_response
        })

        return final_response

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []

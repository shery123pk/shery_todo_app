"""
AI Agent with OpenAI GPT-4
Phase III: AI-Powered Todo Chatbot
Author: Sharmeen Asif
"""

import json
import os
from typing import Any, Optional
from openai import OpenAI
from .mcp_server import TodoMCPServer


class TodoAgent:
    """AI agent for managing todos using natural language with OpenAI"""

    def __init__(self, session_token: str):
        """
        Initialize the AI agent.

        Args:
            session_token: User's session token for API authentication
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.mcp_server = TodoMCPServer(session_token)
        self.conversation_history: list[dict[str, Any]] = []

        self.system_prompt = """You are a helpful AI assistant for managing todo tasks.
You have access to tools that can interact with a todo API.

When users ask you to manage their tasks, use the available tools to:
- List tasks (with optional filtering by completion status)
- Create new tasks
- Update existing tasks
- Delete tasks
- Search for tasks by keywords

Be conversational and helpful. When you perform an action, confirm what you did.
Always use the tools to get real data - don't make up task information.

Examples:
User: "Show me all my tasks"
You: Use list_tasks tool, then present the results clearly

User: "Add buy groceries to my list"
You: Use create_task with title "buy groceries", then confirm creation

User: "Mark task 1 as complete"
You: Use update_task to set completed=true, then confirm

Be natural and friendly in your responses!"""

    async def chat(self, user_message: str) -> str:
        """
        Process a user message and return AI response.

        Args:
            user_message: The user's input message

        Returns:
            The AI's response as a string
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Get available tools from MCP server
        tools = await self.mcp_server.server.list_tools()()

        # Convert MCP tools to OpenAI function format
        openai_tools = []
        for tool in tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            })

        # Call OpenAI with tools
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history
            ],
            tools=openai_tools if openai_tools else None,
            tool_choice="auto" if openai_tools else None
        )

        # Process response
        assistant_message = response.choices[0].message

        # Handle tool calls
        if assistant_message.tool_calls:
            # Add assistant message to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })

            # Execute tool calls
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Call the MCP tool
                result = await self.mcp_server.server.call_tool()(
                    name=function_name,
                    arguments=function_args
                )

                # Extract text content from result
                result_text = ""
                if result and len(result.content) > 0:
                    result_text = result.content[0].text

                # Add tool result to history
                self.conversation_history.append({
                    "role": "tool",
                    "content": result_text,
                    "tool_call_id": tool_call.id
                })

            # Get final response after tool execution
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.conversation_history
                ]
            )

            final_message = final_response.choices[0].message.content or ""
            self.conversation_history.append({
                "role": "assistant",
                "content": final_message
            })

            return final_message
        else:
            # No tool calls, just return the response
            response_text = assistant_message.content or ""
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })

            return response_text

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []

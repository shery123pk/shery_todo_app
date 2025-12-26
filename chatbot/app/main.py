"""
AI Todo Chatbot - Main CLI Interface
Phase III: Natural language todo management
Author: Sharmeen Asif
"""

import asyncio
import os
import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from dotenv import load_dotenv
from app.agent import TodoAgent
import httpx


console = Console()


async def authenticate() -> Optional[str]:
    """
    Authenticate user and get session token.

    Returns:
        Session token or None if authentication fails
    """
    console.print("\n[bold cyan]Todo AI Chatbot - Authentication[/bold cyan]\n")

    email = console.input("[yellow]Email:[/yellow] ")
    password = console.input("[yellow]Password:[/yellow] ", password=True)

    api_url = os.getenv("API_URL", "http://localhost:8000")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{api_url}/api/auth/signin",
                json={"email": email, "password": password, "remember_me": False}
            )

            if response.status_code == 200:
                # Extract session token from cookie
                session_token = response.cookies.get("session_token")
                console.print("\n[green]✓ Authentication successful![/green]\n")
                return session_token
            else:
                error = response.json().get("detail", "Authentication failed")
                console.print(f"\n[red]✗ {error}[/red]\n")
                return None

    except Exception as e:
        console.print(f"\n[red]✗ Error: {str(e)}[/red]\n")
        return None


async def chat_loop(agent: TodoAgent):
    """
    Main chat loop for conversing with the AI agent.

    Args:
        agent: Initialized TodoAgent instance
    """
    console.print(Panel.fit(
        "[bold green]Todo AI Chatbot[/bold green]\n\n"
        "I can help you manage your todo tasks using natural language.\n\n"
        "Try saying:\n"
        "• 'Show my tasks'\n"
        "• 'Add buy groceries to my list'\n"
        "• 'Mark the first task as done'\n"
        "• 'Search for tasks about work'\n"
        "• 'Delete the grocery task'\n\n"
        "Type 'exit' or 'quit' to leave, 'reset' to clear conversation history.",
        title="Welcome"
    ))

    while True:
        try:
            # Get user input
            user_input = console.input("\n[bold blue]You:[/bold blue] ")

            # Handle special commands
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("\n[yellow]Goodbye! Happy tasking! 👋[/yellow]\n")
                break

            if user_input.lower() == "reset":
                agent.reset_conversation()
                console.print("\n[green]✓ Conversation history cleared[/green]\n")
                continue

            if not user_input.strip():
                continue

            # Show thinking indicator
            with console.status("[yellow]AI is thinking...[/yellow]"):
                response = await agent.chat(user_input)

            # Display AI response
            console.print(f"\n[bold green]AI Assistant:[/bold green]")
            console.print(Markdown(response))

        except KeyboardInterrupt:
            console.print("\n\n[yellow]Chat interrupted. Type 'exit' to quit.[/yellow]")
            continue
        except Exception as e:
            console.print(f"\n[red]✗ Error: {str(e)}[/red]\n")
            console.print("[yellow]Please try again or type 'exit' to quit.[/yellow]")


async def main():
    """Main entry point for the chatbot"""
    # Load environment variables
    load_dotenv()

    # Check for required environment variables
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print(
            "\n[red]Error: ANTHROPIC_API_KEY environment variable not set[/red]\n"
            "Please set your Anthropic API key:\n"
            "  export ANTHROPIC_API_KEY='your-api-key-here'\n"
        )
        sys.exit(1)

    # Welcome message
    console.print("\n[bold cyan]═══════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]     Todo AI Chatbot - Phase III[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════[/bold cyan]\n")

    # Authenticate user
    session_token = await authenticate()

    if not session_token:
        console.print("[red]Authentication required to use the chatbot.[/red]\n")
        sys.exit(1)

    # Initialize AI agent
    try:
        agent = TodoAgent(session_token=session_token)
    except Exception as e:
        console.print(f"\n[red]Error initializing AI agent: {str(e)}[/red]\n")
        sys.exit(1)

    # Start chat loop
    await chat_loop(agent)


def cli_main():
    """Entry point for CLI command"""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()

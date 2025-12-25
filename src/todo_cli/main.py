"""Main entry point for the todo CLI application."""

from .commands import cli


def main() -> None:
    """Main entry point for the todo CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()

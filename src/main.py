"""
Module: Todo App CLI entry point
Task ID: T-007
Specification Reference: IX, IX - Console/CLI Interface, CLI entry point and REPL
"""

from rich.console import Console
from rich.panel import Panel

from src.cli import CommandDispatcher
from src.storage import TaskStorage


# [T-007] - Spec section: IX (CLI entry point and REPL loop)
def main() -> None:
    """
    Main entry point for the Todo In-Memory Python Console App.

    Initializes storage and CLI dispatcher, then runs the interactive
    read-eval-print loop (REPL) for user commands.

    Per Constitution Principle IX: Application exposes functionality
    EXCLUSIVELY via CLI interface.
    """
    console = Console()

    # Initialize storage and dispatcher
    storage = TaskStorage()
    dispatcher = CommandDispatcher(storage)

    # Welcome banner
    console.print(
        Panel(
            "[cyan bold]Todo In-Memory Console App[/cyan bold]\n"
            "[dim]Type 'help' for available commands or 'exit' to quit[/dim]",
            border_style="cyan",
        )
    )

    # Main REPL loop
    while True:
        try:
            # Get user input
            user_input = console.input("[bold cyan]todo>[/bold cyan] ")

            # Check for exit commands
            if user_input.strip().lower() in ("exit", "quit"):
                console.print(
                    "[yellow]Goodbye![/yellow]"
                )
                break

            # Dispatch command
            result = dispatcher.dispatch(user_input)

            # Handle dispatch result (False = error, continue; None = exit)
            if result is None:
                break

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("")
            console.print(
                "[yellow]Interrupted. Type 'exit' to quit.[/yellow]"
            )
        except EOFError:
            # Handle Ctrl+D (end of file)
            console.print("")
            console.print(
                "[yellow]Goodbye![/yellow]"
            )
            break


def entrypoint() -> None:
    """
    Entrypoint for uv-managed scripts.

    This function is called when users run: uv run src/main.py
    """
    main()


if __name__ == "__main__":
    main()

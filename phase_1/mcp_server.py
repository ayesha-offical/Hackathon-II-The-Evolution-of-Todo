#!/usr/bin/env python3
"""
MCP Server for Spec-Driven Development Commands
Exposes .claude/commands/*.md files as prompts with dynamic argument handling
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from mcp.server import Server
from mcp.types import (
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Resource,
    ResourceTemplate,
)
from mcp.types import TextResourceContents


def load_command_files(commands_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Load all command files from .claude/commands/ directory."""
    commands: Dict[str, Dict[str, Any]] = {}

    if not commands_dir.exists():
        return commands

    for cmd_file in sorted(commands_dir.glob("*.md")):
        try:
            content = cmd_file.read_text(encoding="utf-8")

            # Parse YAML frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter_str = parts[1]
                    body = parts[2].strip()

                    try:
                        frontmatter = yaml.safe_load(frontmatter_str)
                        if frontmatter is None:
                            frontmatter = {}
                    except yaml.YAMLError:
                        frontmatter = {}

                    command_name = cmd_file.stem  # e.g., "sp.specify"
                    commands[command_name] = {
                        "name": command_name,
                        "description": frontmatter.get("description", ""),
                        "frontmatter": frontmatter,
                        "body": body,
                        "file_path": str(cmd_file),
                    }
        except Exception as e:
            print(f"Error loading command {cmd_file.name}: {e}", file=sys.stderr)

    return commands


def create_prompt_for_command(
    command_name: str,
    command_data: Dict[str, Any],
) -> Prompt:
    """Create a Prompt object from a command file."""

    # Create the prompt with arguments
    # The body already contains the full command structure including the $ARGUMENTS placeholder
    prompt = Prompt(
        name=command_name,
        description=command_data["description"],
        arguments=[
            PromptArgument(
                name="arguments",
                description="User input/arguments for the command",
                required=False,
            ),
        ],
    )

    return prompt


def get_prompt_messages(
    command_name: str,
    command_data: Dict[str, Any],
    arguments: Optional[Dict[str, str]] = None,
) -> list:
    """Generate prompt messages for a command with user input."""

    user_input = ""
    if arguments and "arguments" in arguments:
        user_input = arguments["arguments"]

    # Build the complete prompt by replacing $ARGUMENTS placeholder
    prompt_text = command_data["body"]

    # Replace the $ARGUMENTS placeholder with actual user input
    if user_input:
        prompt_text = prompt_text.replace("$ARGUMENTS", user_input)
    # If no user input provided, keep the $ARGUMENTS placeholder as is

    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=prompt_text,
            ),
        ),
    ]


def main():
    """Main MCP server entry point."""

    # Get the project root (parent of this script)
    project_root = Path(__file__).parent
    commands_dir = project_root / ".claude" / "commands"

    # Load all commands
    commands = load_command_files(commands_dir)

    if not commands:
        print(
            f"Warning: No command files found in {commands_dir}",
            file=sys.stderr,
        )

    # Create MCP server
    server = Server("speckit-mcp-server")

    # Register list_prompts handler
    @server.list_prompts()
    async def list_prompts():
        """List all available spec-driven development prompts."""
        prompts = []
        for command_name, command_data in commands.items():
            prompt = create_prompt_for_command(command_name, command_data)
            prompts.append(prompt)
        return prompts

    # Register get_prompt handler
    @server.get_prompt()
    async def get_prompt(name: str, arguments: Optional[Dict[str, str]] = None):
        """Get a specific prompt with user arguments."""
        if name not in commands:
            raise ValueError(f"Unknown prompt: {name}")

        command_data = commands[name]
        messages = get_prompt_messages(name, command_data, arguments)

        return {
            "description": command_data["description"],
            "messages": messages,
        }

    # Register list_resources handler
    @server.list_resources()
    async def list_resources():
        """List all available command resources."""
        resources = []

        # Add a meta resource listing all commands
        resources.append(
            Resource(
                uri="commands://list",
                name="Available Commands",
                description="List of all available spec-driven development commands",
            )
        )

        # Add individual command resources
        for command_name, command_data in commands.items():
            resources.append(
                Resource(
                    uri=f"commands://{command_name}",
                    name=command_name,
                    description=command_data.get("description", ""),
                )
            )

        return resources

    # Register read_resource handler
    @server.read_resource()
    async def read_resource(uri: str):
        """Read a command resource."""
        if uri == "commands://list":
            # Return a list of all commands with descriptions
            cmd_list = "# Available Spec-Driven Development Commands\n\n"
            for command_name, command_data in sorted(commands.items()):
                desc = command_data.get("description", "No description")
                cmd_list += f"- **{command_name}**: {desc}\n"

            return TextResourceContents(
                uri=uri,
                mimeType="text/markdown",
                text=cmd_list,
            )

        # Handle individual command resources
        if uri.startswith("commands://"):
            command_name = uri.replace("commands://", "")
            if command_name not in commands:
                raise ValueError(f"Unknown command: {command_name}")

            command_data = commands[command_name]
            return TextResourceContents(
                uri=uri,
                mimeType="text/markdown",
                text=command_data["body"],
            )

        raise ValueError(f"Unknown resource: {uri}")

    # Run the server with stdio transport
    import mcp.server.stdio

    mcp.server.stdio.stdio_server(server)


if __name__ == "__main__":
    main()

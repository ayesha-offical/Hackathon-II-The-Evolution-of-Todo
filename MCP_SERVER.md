# MCP Server for Spec-Driven Development Commands

An MCP (Model Context Protocol) server that exposes the commands in `.claude/commands/` as prompts and resources.

## Overview

This MCP server makes all spec-driven development commands available through the Model Context Protocol, allowing AI models to:
- List available commands via prompts
- Retrieve and execute commands with dynamic user input
- Browse command resources

## Features

- **Prompt Integration**: All `.claude/commands/*.md` files are exposed as MCP prompts
- **Dynamic Arguments**: Each prompt accepts user input that replaces the `$ARGUMENTS` placeholder in the command template
- **Resource Browser**: Commands are also available as resources for browsing and reading
- **Auto-discovery**: Automatically scans `.claude/commands/` directory for new command files

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements-mcp.txt
   ```

2. Ensure the server script is executable:
   ```bash
   chmod +x mcp_server.py
   ```

## Running the Server

### Standalone (for testing)
```bash
python mcp_server.py
```

### With Claude Code
Configure in `.claude/config.json` (or your MCP configuration):
```json
{
  "mcpServers": {
    "speckit": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

## Command Structure

Each command file in `.claude/commands/` should have:

```markdown
---
description: Brief description of what the command does
handoffs:
  - label: Next step label
    agent: next-agent-name
    prompt: Handoff prompt template
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

[Command instructions and template]
```

## Usage Examples

### Listing Available Commands
Clients can request all available prompts:
```
GET /prompts
```

This returns all commands from `.claude/commands/` as prompt objects with:
- `name`: Command identifier (e.g., "sp.specify")
- `description`: What the command does
- `arguments`: Array with one argument field for user input

### Getting a Command with User Input
Request a specific command with arguments:
```
GET /prompts/sp.specify?arguments={"arguments": "Add user authentication"}
```

The server will:
1. Load the command template
2. Replace `$ARGUMENTS` with the provided input
3. Return the complete prompt with the user's input integrated

### Browsing Commands
Commands are also available as resources:
```
GET /resources  # Lists all available command resources
GET /resource/commands://list  # Lists all commands
GET /resource/commands://sp.specify  # Read a specific command
```

## How Arguments Are Processed

The MCP server handles the `$ARGUMENTS` placeholder as follows:

1. **Command Loading**: Reads the markdown file and extracts the body content
2. **Argument Injection**: When a prompt is requested with arguments:
   - If arguments provided: Replaces `$ARGUMENTS` with the actual user input
   - If no arguments: Keeps `$ARGUMENTS` as-is for the user to fill in

3. **Output**: Returns the complete command with user input integrated into the ## User Input section

## Available Commands

Current commands in `.claude/commands/`:
- `sp.specify` - Create or update feature specifications
- `sp.plan` - Execute implementation planning workflow
- `sp.clarify` - Identify underspecified areas in specs
- `sp.tasks` - Generate actionable, ordered tasks
- `sp.checklist` - Generate custom checklists
- `sp.analyze` - Perform cross-artifact consistency analysis
- `sp.adr` - Create Architecture Decision Records
- `sp.phr` - Record Prompt History Records
- `sp.constitution` - Create/update project constitution
- `sp.reverse-engineer` - Reverse engineer codebase into artifacts
- `sp.implement` - Execute the implementation plan
- `sp.git.commit_pr` - Intelligent Git workflow execution
- `sp.taskstoissues` - Convert tasks into GitHub issues

## Development

### Adding a New Command

1. Create a new markdown file in `.claude/commands/` (e.g., `sp.mycommand.md`)
2. Include YAML frontmatter with `description` and optional `handoffs`
3. Add the command content with `## User Input` section containing `$ARGUMENTS`
4. Server auto-discovers it on next run

### Testing

Check available commands:
```bash
python -c "from mcp_server import load_command_files; from pathlib import Path; cmds = load_command_files(Path('.claude/commands')); print(list(cmds.keys()))"
```

## Architecture

```
mcp_server.py
├── load_command_files()      # Reads and parses .md command files
├── create_prompt_for_command() # Creates MCP Prompt objects
├── get_prompt_messages()      # Generates prompts with user input
└── main()                     # Sets up MCP server with handlers
    ├── list_prompts()        # Returns all commands as prompts
    ├── get_prompt()          # Returns specific prompt with args
    ├── list_resources()      # Returns all commands as resources
    └── read_resource()       # Returns command content as resource
```

## Troubleshooting

### "Warning: No command files found"
- Check that `.claude/commands/` directory exists
- Verify `.md` files are in the correct location
- Check file permissions

### Argument not being replaced
- Ensure the command file contains `$ARGUMENTS` placeholder
- Check that arguments are passed as `{"arguments": "user input"}`
- Verify no syntax errors in the command markdown

### Import errors
- Install dependencies: `pip install -r requirements-mcp.txt`
- Ensure Python 3.10+ is being used

## License

Part of the Spec-Driven Development framework.

#!/usr/bin/env python3
"""
Test script for MCP Server command loading and prompt generation.
This verifies the server works without needing to run the full MCP service.
"""

import sys
from pathlib import Path
from mcp_server import load_command_files, create_prompt_for_command, get_prompt_messages


def test_load_commands():
    """Test loading command files."""
    print("Testing command loading...")
    commands_dir = Path(".claude/commands")
    commands = load_command_files(commands_dir)

    if not commands:
        print("  ✗ No commands loaded")
        return False

    print(f"  ✓ Loaded {len(commands)} commands:")
    for name in sorted(commands.keys()):
        desc = commands[name].get("description", "No description")
        print(f"    - {name}: {desc}")

    return True


def test_prompt_creation():
    """Test prompt creation."""
    print("\nTesting prompt creation...")
    commands_dir = Path(".claude/commands")
    commands = load_command_files(commands_dir)

    if not commands:
        print("  ✗ No commands to test")
        return False

    # Test first command
    cmd_name = next(iter(commands.keys()))
    cmd_data = commands[cmd_name]

    try:
        prompt = create_prompt_for_command(cmd_name, cmd_data)
        print(f"  ✓ Created prompt for {cmd_name}")
        print(f"    - Name: {prompt.name}")
        print(f"    - Description: {prompt.description}")
        print(f"    - Arguments: {len(prompt.arguments)} argument(s)")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create prompt: {e}")
        return False


def test_argument_injection():
    """Test argument injection into prompts."""
    print("\nTesting argument injection...")
    commands_dir = Path(".claude/commands")
    commands = load_command_files(commands_dir)

    if not commands:
        print("  ✗ No commands to test")
        return False

    # Test first command
    cmd_name = next(iter(commands.keys()))
    cmd_data = commands[cmd_name]

    try:
        # Test without arguments
        messages_no_args = get_prompt_messages(cmd_name, cmd_data)
        print(f"  ✓ Generated prompt without arguments")

        # Test with arguments
        test_input = "Test user input for this command"
        messages_with_args = get_prompt_messages(
            cmd_name, cmd_data, {"arguments": test_input}
        )
        print(f"  ✓ Generated prompt with arguments")

        # Verify argument was injected
        prompt_text = messages_with_args[0].content.text
        if test_input in prompt_text:
            print(f"  ✓ User input successfully injected into prompt")
        else:
            print(f"  ✗ User input not found in prompt text")
            return False

        return True
    except Exception as e:
        print(f"  ✗ Failed to generate prompts: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("MCP Server Test Suite")
    print("=" * 60)

    results = []
    results.append(("Command Loading", test_load_commands()))
    results.append(("Prompt Creation", test_prompt_creation()))
    results.append(("Argument Injection", test_argument_injection()))

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

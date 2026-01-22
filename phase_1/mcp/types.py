"""Mock MCP types for testing"""
from dataclasses import dataclass, field
from typing import Any, Optional, List


@dataclass
class TextContent:
    """Text content for messages"""
    type: str
    text: str


@dataclass
class PromptArgument:
    """Argument for a prompt"""
    name: str
    description: str
    required: bool = False


@dataclass
class PromptMessage:
    """Message in a prompt"""
    role: str
    content: TextContent


@dataclass
class Prompt:
    """MCP Prompt object"""
    name: str
    description: str
    arguments: List[PromptArgument] = field(default_factory=list)


@dataclass
class Resource:
    """MCP Resource object"""
    uri: str
    name: str
    description: str = ""


@dataclass
class ResourceTemplate:
    """Resource template"""
    uri_template: str
    name: str
    description: str = ""


@dataclass
class TextResourceContents:
    """Text resource contents"""
    uri: str
    mimeType: str
    text: str

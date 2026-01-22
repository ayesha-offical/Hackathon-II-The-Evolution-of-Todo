"""MCP Server implementation"""
from typing import Callable, Any, Optional


class Server:
    """MCP Server implementation"""

    def __init__(self, name: str):
        self.name = name
        self._list_prompts_handler: Optional[Callable] = None
        self._get_prompt_handler: Optional[Callable] = None
        self._list_resources_handler: Optional[Callable] = None
        self._read_resource_handler: Optional[Callable] = None

    def list_prompts(self):
        """Decorator for list_prompts handler"""
        def decorator(func: Callable) -> Callable:
            self._list_prompts_handler = func
            return func
        return decorator

    def get_prompt(self):
        """Decorator for get_prompt handler"""
        def decorator(func: Callable) -> Callable:
            self._get_prompt_handler = func
            return func
        return decorator

    def list_resources(self):
        """Decorator for list_resources handler"""
        def decorator(func: Callable) -> Callable:
            self._list_resources_handler = func
            return func
        return decorator

    def read_resource(self):
        """Decorator for read_resource handler"""
        def decorator(func: Callable) -> Callable:
            self._read_resource_handler = func
            return func
        return decorator

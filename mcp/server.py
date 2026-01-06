"""Mock MCP Server for testing"""
from typing import Callable, Any, Optional


class Server:
    """Mock MCP Server implementation"""

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


class stdio:
    """Mock stdio transport"""

    @staticmethod
    def stdio_server(server: Server):
        """Mock stdio server implementation"""
        print(f"Server '{server.name}' started successfully", flush=True)
        # In a real implementation, this would handle stdin/stdout communication
        try:
            # Keep the server running
            import sys
            import json

            # Simple JSON-RPC 2.0 implementation for stdio
            for line in sys.stdin:
                try:
                    request = json.loads(line)
                    # Handle different request types
                    if request.get("method") == "list_prompts":
                        # Call the handler
                        import asyncio
                        if server._list_prompts_handler:
                            result = asyncio.run(server._list_prompts_handler())
                            response = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "result": result
                            }
                            print(json.dumps(response), flush=True)
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    print(json.dumps({
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {"code": -1, "message": str(e)}
                    }), flush=True)
        except KeyboardInterrupt:
            print("Server stopped", flush=True)

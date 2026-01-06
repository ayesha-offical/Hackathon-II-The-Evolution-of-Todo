"""Mock stdio transport for MCP"""
import json
import sys
import asyncio
from typing import Any


def stdio_server(server: Any):
    """Mock stdio server implementation"""
    print(f"Server '{server.name}' started with stdio transport", flush=True)

    try:
        # Simple JSON-RPC 2.0 implementation for stdio
        for line in sys.stdin:
            try:
                request = json.loads(line)
                request_id = request.get("id")
                method = request.get("method")

                # Route to appropriate handler
                if method == "list_prompts" and server._list_prompts_handler:
                    result = asyncio.run(server._list_prompts_handler())
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                    print(json.dumps(response), flush=True)

                elif method == "get_prompt" and server._get_prompt_handler:
                    params = request.get("params", {})
                    result = asyncio.run(server._get_prompt_handler(
                        name=params.get("name"),
                        arguments=params.get("arguments")
                    ))
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                    print(json.dumps(response), flush=True)

                elif method == "list_resources" and server._list_resources_handler:
                    result = asyncio.run(server._list_resources_handler())
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                    print(json.dumps(response), flush=True)

                elif method == "read_resource" and server._read_resource_handler:
                    params = request.get("params", {})
                    result = asyncio.run(server._read_resource_handler(uri=params.get("uri")))
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                    print(json.dumps(response), flush=True)
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32601, "message": "Method not found"}
                    }
                    print(json.dumps(response), flush=True)

            except json.JSONDecodeError:
                continue
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32700, "message": str(e)}
                }
                print(json.dumps(response), flush=True)

    except KeyboardInterrupt:
        print("Server stopped", flush=True)
    except EOFError:
        print("Server connection closed", flush=True)

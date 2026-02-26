import asyncio

import httpx
import respx

import anythingllm_mcp as server


def test_check_auth_requires_api_key() -> None:
    original_key = server.API_KEY
    try:
        server.API_KEY = ""
        result = asyncio.run(server.check_auth())
        assert "ANYTHINGLLM_API_KEY is not set" in result
    finally:
        server.API_KEY = original_key


def test_check_auth_success_json_response() -> None:
    original_key = server.API_KEY
    original_base = server.API_BASE_URL
    try:
        server.API_KEY = "test-token"
        server.API_BASE_URL = "http://localhost:3001"

        with respx.mock(assert_all_called=True) as mock:
            mock.get("http://localhost:3001/api/v1/auth").respond(
                status_code=200,
                json={"ok": True},
            )
            result = asyncio.run(server.check_auth())

        assert '"ok": true' in result
    finally:
        server.API_KEY = original_key
        server.API_BASE_URL = original_base


def test_search_workspace_rejects_invalid_top_n() -> None:
    result = asyncio.run(server.search_workspace("demo", "query", top_n=0))
    assert "top_n must be between 1 and 20" in result


def test_handle_error_timeout_message() -> None:
    message = server._handle_error(httpx.TimeoutException("timeout"))
    assert "Request timed out" in message

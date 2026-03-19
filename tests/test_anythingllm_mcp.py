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


# ──────────────────────────────────────────────
# Tests for new tools
# ──────────────────────────────────────────────


def test_create_folder_success() -> None:
    original_key, original_base = server.API_KEY, server.API_BASE_URL
    try:
        server.API_KEY = "test-token"
        server.API_BASE_URL = "http://localhost:3001"
        with respx.mock(assert_all_called=True) as mock:
            mock.post("http://localhost:3001/api/v1/document/create-folder").respond(
                status_code=200,
                json={"success": True, "message": "Folder created"},
            )
            result = asyncio.run(server.create_folder("my-folder"))
        assert '"success": true' in result
    finally:
        server.API_KEY = original_key
        server.API_BASE_URL = original_base


def test_remove_folder_success() -> None:
    original_key, original_base = server.API_KEY, server.API_BASE_URL
    try:
        server.API_KEY = "test-token"
        server.API_BASE_URL = "http://localhost:3001"
        with respx.mock(assert_all_called=True) as mock:
            mock.request("DELETE", "http://localhost:3001/api/v1/document/remove-folder").respond(
                status_code=200,
                json={"success": True},
            )
            result = asyncio.run(server.remove_folder("my-folder"))
        assert '"success": true' in result
    finally:
        server.API_KEY = original_key
        server.API_BASE_URL = original_base


def test_list_documents_in_folder_success() -> None:
    original_key, original_base = server.API_KEY, server.API_BASE_URL
    try:
        server.API_KEY = "test-token"
        server.API_BASE_URL = "http://localhost:3001"
        with respx.mock(assert_all_called=True) as mock:
            mock.get("http://localhost:3001/api/v1/documents/folder/pine-scripts").respond(
                status_code=200,
                json={"localFiles": {"items": []}},
            )
            result = asyncio.run(server.list_documents_in_folder("pine-scripts"))
        assert '"localFiles"' in result
    finally:
        server.API_KEY = original_key
        server.API_BASE_URL = original_base


def test_move_files_rejects_empty_list() -> None:
    result = asyncio.run(server.move_files([]))
    assert "'files' list cannot be empty" in result


def test_move_files_rejects_missing_keys() -> None:
    result = asyncio.run(server.move_files([{"from": "a"}]))
    assert "'from' and 'to'" in result


def test_update_pin_success() -> None:
    original_key, original_base = server.API_KEY, server.API_BASE_URL
    try:
        server.API_KEY = "test-token"
        server.API_BASE_URL = "http://localhost:3001"
        with respx.mock(assert_all_called=True) as mock:
            mock.post("http://localhost:3001/api/v1/workspace/demo/update-pin").respond(
                status_code=200,
                json={"success": True},
            )
            result = asyncio.run(server.update_pin("demo", "custom-documents/test.json", True))
        assert '"success": true' in result
    finally:
        server.API_KEY = original_key
        server.API_BASE_URL = original_base


def test_update_thread_success() -> None:
    original_key, original_base = server.API_KEY, server.API_BASE_URL
    try:
        server.API_KEY = "test-token"
        server.API_BASE_URL = "http://localhost:3001"
        with respx.mock(assert_all_called=True) as mock:
            mock.post(
                "http://localhost:3001/api/v1/workspace/demo/thread/t-slug/update"
            ).respond(
                status_code=200,
                json={"thread": {"slug": "t-slug", "name": "new-name"}},
            )
            result = asyncio.run(server.update_thread("demo", "t-slug", "new-name"))
        assert '"new-name"' in result
    finally:
        server.API_KEY = original_key
        server.API_BASE_URL = original_base


def test_remove_documents_rejects_empty_list() -> None:
    result = asyncio.run(server.remove_documents([]))
    assert "'names' list cannot be empty" in result


def test_remove_documents_success() -> None:
    original_key, original_base = server.API_KEY, server.API_BASE_URL
    try:
        server.API_KEY = "test-token"
        server.API_BASE_URL = "http://localhost:3001"
        with respx.mock(assert_all_called=True) as mock:
            mock.request(
                "DELETE", "http://localhost:3001/api/v1/system/remove-documents"
            ).respond(
                status_code=200,
                json={"success": True},
            )
            result = asyncio.run(server.remove_documents(["custom-documents/test.json"]))
        assert '"success": true' in result
    finally:
        server.API_KEY = original_key
        server.API_BASE_URL = original_base


def test_get_document_metadata_schema_success() -> None:
    original_key, original_base = server.API_KEY, server.API_BASE_URL
    try:
        server.API_KEY = "test-token"
        server.API_BASE_URL = "http://localhost:3001"
        with respx.mock(assert_all_called=True) as mock:
            mock.get("http://localhost:3001/api/v1/document/metadata-schema").respond(
                status_code=200,
                json={"schema": {"title": "string"}},
            )
            result = asyncio.run(server.get_document_metadata_schema())
        assert '"schema"' in result
    finally:
        server.API_KEY = original_key
        server.API_BASE_URL = original_base

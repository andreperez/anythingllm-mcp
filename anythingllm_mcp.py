#!/usr/bin/env python3
"""
MCP Server for AnythingLLM.

Provides tools for managing workspaces, chatting, handling documents,
and administering system settings via the AnythingLLM REST API.
"""

import json
import os
from typing import Optional, Any, cast
from enum import Enum

import httpx
from mcp.server.fastmcp import FastMCP

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

API_BASE_URL = os.environ.get("ANYTHINGLLM_BASE_URL", "http://localhost:3001").rstrip("/")
API_KEY = os.environ.get("ANYTHINGLLM_API_KEY", "")

mcp = FastMCP(
    "anythingllm_mcp",
    instructions=(
        "MCP server for AnythingLLM. Provides workspace management, chat, "
        "document handling, embedding, and system administration tools. "
        "All tools require a running AnythingLLM instance."
    ),
)

# ──────────────────────────────────────────────
# Shared utilities
# ──────────────────────────────────────────────

JsonPayload = dict[str, Any] | list[Any] | str


def _require_api_key() -> None:
    """Ensure API key is configured before performing API calls."""
    if not API_KEY.strip():
        raise RuntimeError(
            "ANYTHINGLLM_API_KEY is not set. Configure it before using this MCP server."
        )


def _as_dict(payload: JsonPayload, endpoint: str) -> dict[str, Any]:
    """Safely convert API payload into dict when expected."""
    if isinstance(payload, dict):
        return payload
    raise TypeError(
        f"Unexpected response type from '{endpoint}'. "
        f"Expected object, got {type(payload).__name__}."
    )


def _validate_range(name: str, value: float | int, minimum: float, maximum: float) -> None:
    """Validate numeric value is within inclusive range."""
    if value < minimum or value > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}.")

async def _api(
    endpoint: str,
    method: str = "GET",
    body: dict | None = None,
    params: dict | None = None,
    timeout: float = 180.0,
) -> JsonPayload:
    """Execute an authenticated request against the AnythingLLM API."""
    _require_api_key()
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    url = f"{API_BASE_URL}/api/v1{endpoint}"

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            url,
            headers=headers,
            json=body,
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()
        return response.text


def _handle_error(e: Exception) -> str:
    """Return a user-friendly error message."""
    if isinstance(e, httpx.HTTPStatusError):
        http_error = cast(httpx.HTTPStatusError, e)
        status = http_error.response.status_code
        try:
            detail = http_error.response.json()
        except Exception:
            detail = http_error.response.text
        messages = {
            401: "Authentication failed. Check your ANYTHINGLLM_API_KEY.",
            403: "Permission denied. Your API key may lack required permissions.",
            404: "Resource not found. Check the slug or ID.",
            429: "Rate limit exceeded. Wait before retrying.",
            500: "Internal server error in AnythingLLM. Check LLM provider connectivity.",
        }
        msg = messages.get(status, f"API error (HTTP {status}).")
        return f"Error: {msg}\nDetails: {json.dumps(detail) if isinstance(detail, dict) else detail}"
    if isinstance(e, RuntimeError):
        return f"Error: {e}"
    if isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out. AnythingLLM may be busy or unreachable."
    if isinstance(e, httpx.RequestError):
        return f"Error: Request failed: {e}"
    if isinstance(e, httpx.ConnectError):
        return f"Error: Cannot connect to AnythingLLM at {API_BASE_URL}. Is it running?"
    return f"Error: {type(e).__name__}: {e}"


def _json_response(data: Any) -> str:
    """Serialize data to pretty JSON."""
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class ChatMode(str, Enum):
    CHAT = "chat"
    QUERY = "query"


# ──────────────────────────────────────────────
# Tools: Authentication
# ──────────────────────────────────────────────

@mcp.tool(
    name="anythingllm_check_auth",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def check_auth() -> str:
    """Verify that the API key is valid and AnythingLLM is reachable."""
    try:
        result = await _api("/auth")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


# ──────────────────────────────────────────────
# Tools: Workspaces
# ──────────────────────────────────────────────

@mcp.tool(
    name="anythingllm_list_workspaces",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def list_workspaces() -> str:
    """List all workspaces in the AnythingLLM instance with their slugs, settings, and thread info."""
    try:
        result = _as_dict(await _api("/workspaces"), "/workspaces")
        workspaces = result.get("workspaces", [])
        summary = []
        for ws in workspaces:
            summary.append({
                "name": ws.get("name"),
                "slug": ws.get("slug"),
                "chatMode": ws.get("chatMode", "chat"),
                "vectorSearchMode": ws.get("vectorSearchMode"),
                "threads": len(ws.get("threads", [])),
                "createdAt": ws.get("createdAt"),
            })
        return _json_response({"total": len(summary), "workspaces": summary})
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_get_workspace",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def get_workspace(slug: str) -> str:
    """Get detailed information about a specific workspace.

    Args:
        slug: Workspace slug (e.g. 'papers', 'lands')
    """
    try:
        result = await _api(f"/workspace/{slug}")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_create_workspace",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
)
async def create_workspace(name: str) -> str:
    """Create a new workspace.

    Args:
        name: Name for the new workspace
    """
    try:
        result = await _api("/workspace/new", method="POST", body={"name": name})
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_update_workspace",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def update_workspace(
    slug: str,
    name: Optional[str] = None,
    openAiTemp: Optional[float] = None,
    openAiHistory: Optional[int] = None,
    openAiPrompt: Optional[str] = None,
    similarityThreshold: Optional[float] = None,
    topN: Optional[int] = None,
    chatMode: Optional[ChatMode] = None,
) -> str:
    """Update workspace settings (name, temperature, prompt, similarity threshold, etc.).

    Args:
        slug: Workspace slug to update
        name: New workspace name
        openAiTemp: LLM temperature (0.0-1.0)
        openAiHistory: Chat history length (0-100)
        openAiPrompt: System prompt override
        similarityThreshold: Similarity threshold (0.0-1.0)
        topN: Top N results for context (1-20)
        chatMode: Chat mode: 'chat' or 'query'
    """
    try:
        if openAiTemp is not None:
            _validate_range("openAiTemp", openAiTemp, 0.0, 1.0)
        if openAiHistory is not None:
            _validate_range("openAiHistory", openAiHistory, 0, 100)
        if similarityThreshold is not None:
            _validate_range("similarityThreshold", similarityThreshold, 0.0, 1.0)
        if topN is not None:
            _validate_range("topN", topN, 1, 20)

        all_params = {
            "name": name,
            "openAiTemp": openAiTemp,
            "openAiHistory": openAiHistory,
            "openAiPrompt": openAiPrompt,
            "similarityThreshold": similarityThreshold,
            "topN": topN,
            "chatMode": chatMode.value if chatMode else None,
        }
        updates = {k: v for k, v in all_params.items() if v is not None}
        if not updates:
            return "Error: No updates provided."
        result = await _api(f"/workspace/{slug}/update", method="POST", body=updates)
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_delete_workspace",
    annotations={"readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": False},
)
async def delete_workspace(slug: str) -> str:
    """Permanently delete a workspace. This action cannot be undone.

    Args:
        slug: Workspace slug to delete
    """
    try:
        await _api(f"/workspace/{slug}", method="DELETE")
        return f"Workspace '{slug}' deleted successfully."
    except Exception as e:
        return _handle_error(e)


# ──────────────────────────────────────────────
# Tools: Chat
# ──────────────────────────────────────────────

@mcp.tool(
    name="anythingllm_chat",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
)
async def chat_with_workspace(slug: str, message: str, mode: ChatMode = ChatMode.CHAT) -> str:
    """Send a message to a workspace and get a response.

    Mode 'chat' uses document context + conversation history.
    Mode 'query' uses only document context (no history).

    Args:
        slug: Workspace slug
        message: Message to send
        mode: 'chat' (context + history) or 'query' (documents only)
    """
    try:
        result = await _api(
            f"/workspace/{slug}/chat",
            method="POST",
            body={"message": message, "mode": mode.value},
        )
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_get_chat_history",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def get_chat_history(slug: str) -> str:
    """Get the chat history for a workspace.

    Args:
        slug: Workspace slug
    """
    try:
        result = await _api(f"/workspace/{slug}/chats")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


# ──────────────────────────────────────────────
# Tools: Workspace Threads
# ──────────────────────────────────────────────

@mcp.tool(
    name="anythingllm_create_thread",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
)
async def create_thread(slug: str, name: Optional[str] = None) -> str:
    """Create a new chat thread within a workspace.

    Args:
        slug: Workspace slug
        name: Optional thread name
    """
    try:
        body = {}
        if name:
            body["name"] = name
        result = await _api(f"/workspace/{slug}/thread/new", method="POST", body=body)
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_delete_thread",
    annotations={"readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": False},
)
async def delete_thread(slug: str, thread_slug: str) -> str:
    """Delete a chat thread from a workspace.

    Args:
        slug: Workspace slug
        thread_slug: Thread slug to delete
    """
    try:
        await _api(f"/workspace/{slug}/thread/{thread_slug}", method="DELETE")
        return f"Thread '{thread_slug}' deleted from workspace '{slug}'."
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_chat_in_thread",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
)
async def chat_in_thread(
    slug: str,
    thread_slug: str,
    message: str,
    mode: ChatMode = ChatMode.CHAT,
) -> str:
    """Send a message within a specific workspace thread.

    Args:
        slug: Workspace slug
        thread_slug: Thread slug
        message: Message to send
        mode: 'chat' or 'query'
    """
    try:
        result = await _api(
            f"/workspace/{slug}/thread/{thread_slug}/chat",
            method="POST",
            body={"message": message, "mode": mode.value},
        )
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_get_thread_chats",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def get_thread_chats(slug: str, thread_slug: str) -> str:
    """Get chat history for a specific thread in a workspace.

    Args:
        slug: Workspace slug
        thread_slug: Thread slug
    """
    try:
        result = await _api(f"/workspace/{slug}/thread/{thread_slug}/chats")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


# ──────────────────────────────────────────────
# Tools: Documents
# ──────────────────────────────────────────────

@mcp.tool(
    name="anythingllm_list_documents",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def list_documents() -> str:
    """List all uploaded documents across all folders."""
    try:
        result = await _api("/documents")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_get_accepted_file_types",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def get_accepted_file_types() -> str:
    """Get the list of file types that AnythingLLM accepts for upload."""
    try:
        result = await _api("/document/accepted-file-types")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_upload_link",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def upload_link(link: str) -> str:
    """Scrape a web page and upload it as a document to AnythingLLM.

    Args:
        link: URL to scrape (must start with http:// or https://)
    """
    try:
        if not link.startswith(("http://", "https://")):
            return "Error: Link must start with http:// or https://"
        result = await _api(
            "/document/upload-link",
            method="POST",
            body={"link": link},
        )
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_upload_raw_text",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
)
async def upload_raw_text(text_content: str, title: str) -> str:
    """Upload raw text content as a document to AnythingLLM.

    Args:
        text_content: Raw text content to upload
        title: Document title
    """
    try:
        result = await _api(
            "/document/raw-text",
            method="POST",
            body={"textContent": text_content, "metadata": {"title": title}},
        )
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_update_embeddings",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def update_embeddings(
    slug: str,
    adds: Optional[list[str]] = None,
    deletes: Optional[list[str]] = None,
) -> str:
    """Add or remove document embeddings in a workspace. Use document paths from list_documents.

    Args:
        slug: Workspace slug
        adds: Document paths to add (from /api/v1/documents)
        deletes: Document names to remove
    """
    try:
        body: dict[str, Any] = {}
        if adds:
            body["adds"] = adds
        if deletes:
            body["deletes"] = deletes
        if not body:
            return "Error: Provide at least 'adds' or 'deletes'."
        result = await _api(
            f"/workspace/{slug}/update-embeddings",
            method="POST",
            body=body,
        )
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


# ──────────────────────────────────────────────
# Tools: Search
# ──────────────────────────────────────────────

@mcp.tool(
    name="anythingllm_search",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def search_workspace(slug: str, query: str, top_n: int = 4, score_threshold: Optional[float] = None) -> str:
    """Search for relevant document chunks within a workspace using vector similarity.

    Args:
        slug: Workspace slug to search in
        query: Search query
        top_n: Number of results (1-20, default 4)
        score_threshold: Similarity score threshold (0-1). Lower = more results.
    """
    try:
        _validate_range("top_n", top_n, 1, 20)
        body: dict = {"query": query, "topN": top_n}
        if score_threshold is not None:
            _validate_range("score_threshold", score_threshold, 0.0, 1.0)
            body["scoreThreshold"] = score_threshold
        result = await _api(
            f"/workspace/{slug}/vector-search",
            method="POST",
            body=body,
        )
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


# ──────────────────────────────────────────────
# Tools: System
# ──────────────────────────────────────────────

@mcp.tool(
    name="anythingllm_get_system_settings",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def get_system_settings() -> str:
    """Get AnythingLLM system settings (LLM provider, vector DB, embeddings, etc.)."""
    try:
        result = _as_dict(await _api("/system"), "/system")
        settings = result.get("settings", {})
        safe_keys = [
            "LLMProvider", "LLMModel", "VectorDB", "EmbeddingEngine",
            "EmbeddingModelPref", "EmbeddingModelMaxChunkLength",
            "MultiUserMode", "DisableTelemetry", "WhisperProvider",
            "TextToSpeechProvider", "OllamaLLMBasePath", "OllamaLLMModelPref",
        ]
        filtered = {k: settings.get(k) for k in safe_keys if settings.get(k) is not None}
        return _json_response({"settings": filtered})
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_get_vector_count",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def get_vector_count() -> str:
    """Get the total number of vectors stored in the system."""
    try:
        result = await _api("/system/vector-count")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="anythingllm_export_chats",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def export_chats() -> str:
    """Export all chat logs from all workspaces."""
    try:
        result = await _api("/system/export-chats")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


# ──────────────────────────────────────────────
# Tools: Embeds (public chat widgets)
# ──────────────────────────────────────────────

@mcp.tool(
    name="anythingllm_list_embeds",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def list_embeds() -> str:
    """List all embed configurations (public chat widgets)."""
    try:
        result = await _api("/embed")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


# ──────────────────────────────────────────────
# Tools: OpenAI-compatible endpoints
# ──────────────────────────────────────────────

@mcp.tool(
    name="anythingllm_list_models",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def list_models() -> str:
    """List available models via the OpenAI-compatible endpoint."""
    try:
        result = await _api("/openai/models")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

def main() -> None:
    """Run MCP server using stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()

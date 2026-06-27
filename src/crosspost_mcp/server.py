"""FastMCP server entry point for crosspost-mcp.

Exposes platform posting functions as MCP tools that AI agents can call.
Each tool wraps a platform module with consistent error handling and
returns a normalized response dict.
"""
from __future__ import annotations

import asyncio
from typing import Any

from fastmcp import FastMCP

from crosspost_mcp.platforms import discord, telegram

mcp = FastMCP(
    name="crosspost-mcp",
    instructions=(
        "Cross-post content to Telegram, Discord, Mastodon, Bluesky, and Reddit. "
        "Each tool returns a dict with platform, status, and post identifiers. "
        "Use post_to_all for fan-out posting across all configured platforms."
    ),
)


@mcp.tool
async def post_to_telegram(text: str) -> dict[str, Any]:
    """Post a message to the configured Telegram channel.

    Args:
        text: Message text (max 4096 chars). Supports HTML formatting:
            <b>bold</b>, <i>italic</i>, <code>mono</code>, <a href="">link</a>.

    Returns:
        Dict with platform, status, message_id, chat_id.
    """
    return await telegram.post(text)


@mcp.tool
async def post_to_discord(text: str) -> dict[str, Any]:
    """Post a message to the configured Discord channel via webhook.

    Args:
        text: Message content (max 2000 chars). Supports Discord markdown:
            **bold**, *italic*, `code`, ```block```.

    Returns:
        Dict with platform, status, message_id, channel_id.
    """
    return await discord.post(text)


@mcp.tool
async def post_to_all(text: str) -> dict[str, Any]:
    """Post the same message to all configured platforms concurrently.

    Runs all platform posts in parallel. Individual platform failures
    do not abort other platforms; each result is reported separately.

    Args:
        text: Message text. Note that platforms have different length limits
            (Discord 2000, Telegram 4096). Text exceeding a platform's limit
            will fail for that platform only.

    Returns:
        Dict with overall status and per-platform results:
        {"status": "ok" | "partial" | "error", "results": [...]}
    """
    tasks = {
        "telegram": telegram.post(text),
        "discord": discord.post(text),
    }

    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    output: list[dict[str, Any]] = []
    success_count = 0
    for platform_name, result in zip(tasks.keys(), results, strict=True):
        if isinstance(result, Exception):
            output.append({
                "platform": platform_name,
                "status": "error",
                "error": str(result),
                "error_type": type(result).__name__,
            })
        else:
            output.append(result)
            success_count += 1

    if success_count == len(tasks):
        overall = "ok"
    elif success_count == 0:
        overall = "error"
    else:
        overall = "partial"

    return {"status": overall, "results": output}


def main() -> None:
    """Console script entry point. Runs the MCP server on stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
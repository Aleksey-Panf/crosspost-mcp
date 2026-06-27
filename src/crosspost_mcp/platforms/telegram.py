"""Telegram posting via Bot API.

Uses the official Bot API which is free and requires only a bot token
from @BotFather. The bot must be added as an admin to the target channel
with "Post Messages" permission.
Docs: https://core.telegram.org/bots/api
"""
from __future__ import annotations

from typing import Any

import httpx

from crosspost_mcp.config import TelegramConfig

MAX_TEXT_LENGTH = 4096  # Telegram hard limit for text messages
DEFAULT_TIMEOUT = 15.0
API_BASE = "https://api.telegram.org"


async def post(
    text: str,
    *,
    parse_mode: str | None = "HTML",
    disable_web_page_preview: bool = False,
) -> dict[str, Any]:
    """Send a message to a Telegram channel.

    Args:
        text: Message text (max 4096 chars).
        parse_mode: "HTML", "MarkdownV2", or None for plain text.
        disable_web_page_preview: Hide link previews if True.

    Returns:
        Dict with status and message info.

    Raises:
        ValueError: If text is empty or too long.
        httpx.HTTPStatusError: If Telegram API returns an error.
        RuntimeError: If Telegram returns ok=false in the response body.
    """
    if not text or not text.strip():
        raise ValueError("Telegram message text cannot be empty.")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Telegram message too long: {len(text)} chars "
            f"(max {MAX_TEXT_LENGTH})."
        )

    cfg = TelegramConfig.load()

    url = f"{API_BASE}/bot{cfg.bot_token}/sendMessage"
    payload: dict[str, Any] = {
        "chat_id": cfg.chat_id,
        "text": text,
        "disable_web_page_preview": disable_web_page_preview,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")

    result = data["result"]
    return {
        "platform": "telegram",
        "status": "ok",
        "message_id": result.get("message_id"),
        "chat_id": result.get("chat", {}).get("id"),
    }
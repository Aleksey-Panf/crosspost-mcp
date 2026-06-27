"""Discord posting via incoming webhooks.

Uses Discord's webhook API which requires no OAuth, no bot setup,
just a webhook URL created in channel settings.
Docs: https://discord.com/developers/docs/resources/webhook
"""
from __future__ import annotations

from typing import Any

import httpx

from crosspost_mcp.config import DiscordConfig

MAX_CONTENT_LENGTH = 2000  # Discord hard limit
DEFAULT_TIMEOUT = 15.0


async def post(
    text: str,
    *,
    username: str | None = None,
    avatar_url: str | None = None,
) -> dict[str, Any]:
    """Send a message to Discord via webhook.

    Args:
        text: Message content (max 2000 chars).
        username: Override webhook's default username.
        avatar_url: Override webhook's default avatar.

    Returns:
        Dict with status and message info.

    Raises:
        ValueError: If text is empty or too long.
        httpx.HTTPStatusError: If Discord returns an error status.
    """
    if not text or not text.strip():
        raise ValueError("Discord message text cannot be empty.")
    if len(text) > MAX_CONTENT_LENGTH:
        raise ValueError(
            f"Discord message too long: {len(text)} chars "
            f"(max {MAX_CONTENT_LENGTH})."
        )

    cfg = DiscordConfig.load()

    payload: dict[str, Any] = {"content": text}
    if username:
        payload["username"] = username
    if avatar_url:
        payload["avatar_url"] = avatar_url

    # wait=true makes Discord return the created message object
    url = f"{cfg.webhook_url}?wait=true"

    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    return {
        "platform": "discord",
        "status": "ok",
        "message_id": data.get("id"),
        "channel_id": data.get("channel_id"),
    }
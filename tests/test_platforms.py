"""Unit tests for platform posting modules.

Validates input checks (empty text, length limits) that run before
any network calls. These tests do not hit external APIs.
"""
from __future__ import annotations

import pytest

from crosspost_mcp.platforms import discord, telegram


class TestDiscordValidation:
    @pytest.mark.asyncio
    async def test_empty_text_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            await discord.post("")

    @pytest.mark.asyncio
    async def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            await discord.post("   ")

    @pytest.mark.asyncio
    async def test_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match="too long"):
            await discord.post("x" * (discord.MAX_CONTENT_LENGTH + 1))


class TestTelegramValidation:
    @pytest.mark.asyncio
    async def test_empty_text_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            await telegram.post("")

    @pytest.mark.asyncio
    async def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            await telegram.post("   ")

    @pytest.mark.asyncio
    async def test_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match="too long"):
            await telegram.post("x" * (telegram.MAX_TEXT_LENGTH + 1))
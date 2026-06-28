"""Unit tests for the config module.

These tests verify that config loaders correctly read environment
variables and raise clear errors when required values are missing.
"""
from __future__ import annotations

import pytest

from crosspost_mcp.config import (
    ConfigError,
    DiscordConfig,
    TelegramConfig,
    _require,
)


class TestRequire:
    def test_returns_value_when_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("TEST_VAR", "hello")
        assert _require("TEST_VAR") == "hello"

    def test_raises_when_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("MISSING_VAR", raising=False)
        with pytest.raises(ConfigError, match="MISSING_VAR"):
            _require("MISSING_VAR")

    def test_raises_when_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("EMPTY_VAR", "")
        with pytest.raises(ConfigError):
            _require("EMPTY_VAR")


class TestTelegramConfig:
    def test_load_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "@test_channel")

        cfg = TelegramConfig.load()

        assert cfg.bot_token == "test-token"
        assert cfg.chat_id == "@test_channel"

    def test_load_missing_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "@test_channel")

        with pytest.raises(ConfigError, match="TELEGRAM_BOT_TOKEN"):
            TelegramConfig.load()


class TestDiscordConfig:
    def test_load_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(
            "DISCORD_WEBHOOK_URL",
            "https://discord.com/api/webhooks/123/abc",
        )

        cfg = DiscordConfig.load()

        assert cfg.webhook_url == "https://discord.com/api/webhooks/123/abc"

    def test_load_missing_url(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)

        with pytest.raises(ConfigError, match="DISCORD_WEBHOOK_URL"):
            DiscordConfig.load()
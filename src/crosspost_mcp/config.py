"""Configuration loader for crosspost-mcp.

Loads credentials from environment variables (.env file).
Each platform has its own config getter that raises a clear error
if required variables are missing.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    """Raised when required environment variables are missing."""


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(
            f"Missing required environment variable: {name}. "
            f"Check your .env file (see .env.example)."
        )
    return value


@dataclass(frozen=True)
class TelegramConfig:
    bot_token: str
    chat_id: str

    @classmethod
    def load(cls) -> TelegramConfig:
        return cls(
            bot_token=_require("TELEGRAM_BOT_TOKEN"),
            chat_id=_require("TELEGRAM_CHAT_ID"),
        )


@dataclass(frozen=True)
class DiscordConfig:
    webhook_url: str

    @classmethod
    def load(cls) -> DiscordConfig:
        return cls(webhook_url=_require("DISCORD_WEBHOOK_URL"))


@dataclass(frozen=True)
class MastodonConfig:
    api_base_url: str
    access_token: str

    @classmethod
    def load(cls) -> MastodonConfig:
        return cls(
            api_base_url=_require("MASTODON_API_BASE_URL"),
            access_token=_require("MASTODON_ACCESS_TOKEN"),
        )


@dataclass(frozen=True)
class BlueskyConfig:
    handle: str
    app_password: str

    @classmethod
    def load(cls) -> BlueskyConfig:
        return cls(
            handle=_require("BLUESKY_HANDLE"),
            app_password=_require("BLUESKY_APP_PASSWORD"),
        )


@dataclass(frozen=True)
class RedditConfig:
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str

    @classmethod
    def load(cls) -> RedditConfig:
        return cls(
            client_id=_require("REDDIT_CLIENT_ID"),
            client_secret=_require("REDDIT_CLIENT_SECRET"),
            username=_require("REDDIT_USERNAME"),
            password=_require("REDDIT_PASSWORD"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "crosspost-mcp/0.1.0"),
        )
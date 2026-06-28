# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Mastodon support (v0.2.0)
- Bluesky support (v0.3.0)
- Reddit support (v0.4.0)
- Media and image attachments
- Scheduled posting

## [0.1.0] - 2026-06-28

### Added
- Initial release of crosspost-mcp
- `post_to_telegram` tool for posting to Telegram channels via Bot API
- `post_to_discord` tool for posting to Discord channels via webhooks
- `post_to_all` tool for parallel cross-posting to all configured platforms
- Per-platform dataclass configs loaded from `.env`
- FastMCP-based server with stdio transport
- GitHub Actions CI with pytest and ruff across Python 3.11, 3.12, 3.13
- 13 unit tests covering config loading and input validation
- Full README with usage examples, tool reference, and credentials guide

[Unreleased]: https://github.com/Aleksey-Panf/crosspost-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Aleksey-Panf/crosspost-mcp/releases/tag/v0.1.0
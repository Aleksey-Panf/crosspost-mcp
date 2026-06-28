# Contributing to crosspost-mcp

Thanks for your interest in contributing. This document explains how to set up
the project locally, the code style we follow, and how to submit changes.

## Ways to contribute

- Report bugs via [GitHub Issues](https://github.com/Aleksey-Panf/crosspost-mcp/issues)
- Suggest features or improvements
- Add support for new platforms (see `src/crosspost_mcp/platforms/` for examples)
- Improve documentation
- Fix typos, broken links, or unclear sections in the README

## Development setup

```bash
git clone https://github.com/Aleksey-Panf/crosspost-mcp.git
cd crosspost-mcp
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and fill in real credentials for the platforms
you want to test. Tests do not hit live APIs, so you can run them without any
credentials configured.

## Running tests and linter

```bash
pytest -v
ruff check src tests
```

Both must pass before opening a pull request. CI runs the same commands on
Python 3.11, 3.12, and 3.13.

## Adding a new platform

1. Create `src/crosspost_mcp/platforms/<platform>.py` following the pattern in
   `discord.py` or `telegram.py`.
2. Add a `<Platform>Config` dataclass in `src/crosspost_mcp/config.py`.
3. Register a `post_to_<platform>` tool in `src/crosspost_mcp/server.py`.
4. Update `post_to_all` to include the new platform.
5. Add input-validation tests in `tests/test_platforms.py`.
6. Document the platform in the README's `Getting Credentials` section.

## Code style

- Python 3.11+ with full type annotations
- `from __future__ import annotations` at the top of every module
- Line length 100 (enforced by ruff)
- Async-first for all I/O
- Each platform module exposes a single `post(text, **kwargs)` coroutine
- Configs are frozen dataclasses loaded via classmethod

## Pull requests

- Open an issue first for non-trivial changes so we can discuss the approach
- One change per pull request
- Reference related issues in the PR description
- Update the README and CHANGELOG when relevant

## Commercial inquiries

For paid custom MCP development, contact [@AlexAi14](https://t.me/AlexAi14)
directly. GitHub Issues are for the open-source project itself.
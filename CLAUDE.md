# CLAUDE.md — Sarvam AI MCP Server

## Project Overview

This is a **Sarvam AI MCP Server** — a Python-based MCP (Model Context Protocol) server that exposes Sarvam AI's Indic language processing APIs as MCP tools. It allows LLM clients (Claude Desktop, Gemini CLI, Warp, etc.) to perform translation, transliteration, language identification, and chat with the SarvamAI-M model.

## Architecture

- **Single-file server**: All logic lives in `sarvam_mcp.py`
- **Framework**: Uses [FastMCP](https://pypi.org/project/fastmcp/) (`mcp.server.fastmcp.FastMCP`)
- **Transport**: Streamable HTTP on `0.0.0.0:8080` (stateless)
- **External API**: All tools proxy requests to `https://api.sarvam.ai`
- **Auth**: Sarvam API key loaded from `.env` via `python-dotenv`

## MCP Tools Exposed

| Tool Name                | Function        | Endpoint                          | Notes                                      |
|--------------------------|-----------------|-----------------------------------|--------------------------------------------|
| `Language_Identification`| `lang_ident`    | `POST /text-lid`                  | Max 2000 chars                             |
| `Transliterate`          | `lang_identification` | `POST /transliterate`       | Max 1000 chars, auto source detection      |
| `Translate`              | `lang_identification` | `POST /translate`           | Auto source detection                      |
| `Sarvam_Chat`            | `sarvam_chat`   | `POST /v1/chat/completions`       | Modes: `basic`, `wiki` (wiki_grounding)    |

## Supported Languages

Bengali (bn), English (en), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (od), Punjabi (pa), Tamil (ta), Telugu (te) — all with `-IN` locale codes.

## Key Files

- `sarvam_mcp.py` — Server entry point and all tool definitions
- `.env` — Contains `SARVAM_API_KEY` (do NOT commit real keys)
- `requirements.txt` — Runtime deps: `fastmcp`, `dotenv`, `httpx`
- `pyproject.toml` — Project metadata (requires Python >=3.13)
- `Dockerfile` — Slim Python 3.13 image, exposes port 8080

## Running

```bash
# Local
pip install -r requirements.txt
python sarvam_mcp.py

# Docker
docker build -t sarvam .
docker run -p 8080:8080 sarvam
```

## Development Notes

- HTTP client: `httpx.AsyncClient` (async)
- The `Transliterate` and `Translate` tool functions share the same Python function name (`lang_identification`) — this is a known issue but works because FastMCP registers by tool `name`, not function name
- API key check uses `== None` instead of `is None`
- No tests exist currently
- No logging configured
- `pyproject.toml` lists `requests` as a dependency but the code uses `httpx` instead

import json
from unittest.mock import AsyncMock, patch, MagicMock

import httpx
import pytest

import sarvam_mcp


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    """Set a fake API key for all tests by default."""
    monkeypatch.setattr(sarvam_mcp, "KEY", "test-api-key")


@pytest.fixture
def no_api_key(monkeypatch):
    """Override to simulate missing API key."""
    monkeypatch.setattr(sarvam_mcp, "KEY", None)


# --- Missing API key tests ---

@pytest.mark.asyncio
async def test_lang_ident_missing_key(no_api_key):
    result = await sarvam_mcp.lang_ident("hello")
    assert "Please provide the Sarvam API Key" in result


@pytest.mark.asyncio
async def test_transliterate_missing_key(no_api_key):
    result = await sarvam_mcp.transliterate("hello", "hindi")
    assert "Please provide the Sarvam API Key" in result


@pytest.mark.asyncio
async def test_translate_missing_key(no_api_key):
    result = await sarvam_mcp.translate("hello", "hindi")
    assert "Please provide the Sarvam API Key" in result


@pytest.mark.asyncio
async def test_sarvam_chat_missing_key(no_api_key):
    result = await sarvam_mcp.sarvam_chat("hello")
    assert "Please provide the Sarvam API Key" in result


# --- Input length validation ---

@pytest.mark.asyncio
async def test_lang_ident_too_long():
    result = await sarvam_mcp.lang_ident("a" * 2001)
    assert "Max allowed: 2000" in result


@pytest.mark.asyncio
async def test_transliterate_too_long():
    result = await sarvam_mcp.transliterate("a" * 1001, "hindi")
    assert "Max allowed: 1000" in result


# --- Language validation ---

@pytest.mark.asyncio
async def test_transliterate_unsupported_language():
    result = await sarvam_mcp.transliterate("hello", "french")
    assert "Unsupported language" in result
    assert "french" in result


@pytest.mark.asyncio
async def test_translate_unsupported_language():
    result = await sarvam_mcp.translate("hello", "french")
    assert "Unsupported language" in result
    assert "french" in result


# --- Chat model validation ---

@pytest.mark.asyncio
async def test_sarvam_chat_invalid_model():
    result = await sarvam_mcp.sarvam_chat("hello", model="invalid-model")
    assert "Invalid model" in result


# --- Valid payload construction (mock httpx) ---

def _mock_response(data: dict) -> MagicMock:
    mock = MagicMock()
    mock.json.return_value = data
    mock.text = json.dumps(data)
    mock.raise_for_status = MagicMock()
    return mock


@pytest.mark.asyncio
async def test_lang_ident_valid_payload():
    mock_resp = _mock_response({"language": "hi", "script": "Devanagari"})
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await sarvam_mcp.lang_ident("नमस्ते")
        data = json.loads(result)
        assert data["language"] == "hi"

        _, kwargs = mock_client.post.call_args
        assert kwargs["json"] == {"input": "नमस्ते"}


@pytest.mark.asyncio
async def test_transliterate_valid_payload():
    mock_resp = _mock_response({"transliterated_text": "namaste"})
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await sarvam_mcp.transliterate("नमस्ते", "English")
        data = json.loads(result)
        assert data["transliterated_text"] == "namaste"

        _, kwargs = mock_client.post.call_args
        assert kwargs["json"]["target_language_code"] == "en-IN"
        assert kwargs["json"]["source_language_code"] == "auto"


@pytest.mark.asyncio
async def test_translate_valid_payload():
    mock_resp = _mock_response({"translated_text": "hello"})
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await sarvam_mcp.translate("नमस्ते", "en")
        data = json.loads(result)
        assert data["translated_text"] == "hello"

        _, kwargs = mock_client.post.call_args
        assert kwargs["json"]["target_language_code"] == "en-IN"


@pytest.mark.asyncio
async def test_sarvam_chat_default_model():
    mock_resp = _mock_response({"choices": [{"message": {"content": "hi"}}]})
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await sarvam_mcp.sarvam_chat("hello")
        data = json.loads(result)
        assert "choices" in data

        _, kwargs = mock_client.post.call_args
        assert kwargs["json"]["model"] == "sarvam-30b"
        assert "wiki_grounding" not in kwargs["json"]


@pytest.mark.asyncio
async def test_sarvam_chat_wiki_mode():
    mock_resp = _mock_response({"choices": [{"message": {"content": "hi"}}]})
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await sarvam_mcp.sarvam_chat("hello", mode="wiki")

        _, kwargs = mock_client.post.call_args
        assert kwargs["json"]["wiki_grounding"] is True
        assert kwargs["json"]["temperature"] == 0.2


@pytest.mark.asyncio
async def test_sarvam_chat_105b_model():
    mock_resp = _mock_response({"choices": [{"message": {"content": "hi"}}]})
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_resp
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await sarvam_mcp.sarvam_chat("hello", model="sarvam-105b")

        _, kwargs = mock_client.post.call_args
        assert kwargs["json"]["model"] == "sarvam-105b"

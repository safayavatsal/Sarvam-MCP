from mcp.server.fastmcp import FastMCP
import  os, json, httpx, logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("sarvam_mcp")

KEY = os.getenv("SARVAM_API_KEY")

mcp = FastMCP(
    name="SarvamAI Text Tools",
    host="0.0.0.0",
    port=8080,
    stateless_http=True
)

base_url = "https://api.sarvam.ai"

Languages = {
    "bengali": "bn-IN",
    "bn": "bn-IN",
    "english": "en-IN",
    "en": "en-IN",
    "gujarati": "gu-IN",
    "gu": "gu-IN",
    "hindi": "hi-IN",
    "hi": "hi-IN",
    "kannada": "kn-IN",
    "kn": "kn-IN",
    "malayalam": "ml-IN",
    "ml": "ml-IN",
    "marathi": "mr-IN",
    "mr": "mr-IN",
    "odia": "od-IN",
    "od": "od-IN",
    "punjabi": "pa-IN",
    "pa": "pa-IN",
    "tamil": "ta-IN",
    "ta": "ta-IN",
    "telugu": "te-IN",
    "te": "te-IN"
}

@mcp.tool(name="Language_Identification")
async def lang_ident(text: str) -> str:
    """
    Identifies the language and script of the input text.
    Supported Language are English, Hindi, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu.
    """
    logger.info("Language_Identification called, text length=%d", len(text))
    url = f"{base_url}/text-lid"
    headers = {
        "api-subscription-key": KEY,
        "Content-Type": "application/json"
    }
    if KEY is None:
        logger.error("API key not configured")
        return "Please provide the Sarvam API Key"
    if len(text)>2000:
        logger.error("Input too long: %d chars (max 2000)", len(text))
        return "Input too long. Max allowed: 2000 characters."
    payload = {"input": text}
    logger.debug("Request payload: %s", json.dumps(payload))
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.debug("Response: %s", response.text)
            return json.dumps(response.json())
    except Exception as ex:
        logger.error("API request failed: %s", ex)
        return json.dumps({"error": str(ex)})

@mcp.tool(name="Transliterate")
async def transliterate(text: str, lang:str) -> str:
    """
    Transliteration converts text from one script to another while preserving the original pronunciation.
    Supported Language are English, Hindi, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu
    """
    logger.info("Transliterate called, lang=%s, text length=%d", lang, len(text))
    url = f"{base_url}/transliterate"
    headers = {
        "api-subscription-key": KEY,
        "Content-Type": "application/json"
    }
    if KEY is None:
        logger.error("API key not configured")
        return "Please provide the Sarvam API Key"
    lang = lang.lower()
    code = Languages.get(lang)
    if code is None:
        supported = ", ".join(sorted(set(Languages.keys()) - {k for k in Languages if len(k) <= 2}))
        logger.error("Unsupported language: %s", lang)
        return f"Unsupported language: '{lang}'. Supported languages: {supported}"
    if len(text)>1000:
        logger.error("Input too long: %d chars (max 1000)", len(text))
        return "Input too long. Max allowed: 1000 characters."
    payload = {"input": text,"source_language_code": "auto","target_language_code":code}
    logger.debug("Request payload: %s", json.dumps(payload))
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.debug("Response: %s", response.text)
            return json.dumps(response.json())
    except Exception as ex:
        logger.error("API request failed: %s", ex)
        return json.dumps({"error": str(ex)})

@mcp.tool(name="Translate")
async def translate(text: str, lang:str) -> str:
    """
    Translation converts text from one language to another while preserving its meaning.
    Supported Language are English, Hindi, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu.
    """
    logger.info("Translate called, lang=%s, text length=%d", lang, len(text))
    url = f"{base_url}/translate"
    headers = {
        "api-subscription-key": KEY,
        "Content-Type": "application/json"
    }
    if KEY is None:
        logger.error("API key not configured")
        return "Please provide the Sarvam API Key"
    lang = lang.lower()
    code = Languages.get(lang)
    if code is None:
        supported = ", ".join(sorted(set(Languages.keys()) - {k for k in Languages if len(k) <= 2}))
        logger.error("Unsupported language: %s", lang)
        return f"Unsupported language: '{lang}'. Supported languages: {supported}"
    payload = {"input": text,"source_language_code": "auto","target_language_code":code}
    logger.debug("Request payload: %s", json.dumps(payload))
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.debug("Response: %s", response.text)
            return json.dumps(response.json())
    except Exception as ex:
        logger.error("API request failed: %s", ex)
        return json.dumps({"error": str(ex)})

@mcp.tool(name="Sarvam_Chat")
async def sarvam_chat(query: str, mode: str = "basic", model: str = "sarvam-30b") -> str:
    """
    Interact with Sarvam AI chat models via API.
    Available models:
    - sarvam-30b: 30B parameter model with 64K context (default)
    - sarvam-105b: 105B parameter model with 128K context
    Modes:
    - basic: Standard response
    - wiki: Uses wiki_grounding
    """
    logger.info("Sarvam_Chat called, model=%s, mode=%s", model, mode)
    url = f"{base_url}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json"
    }
    if KEY is None:
        logger.error("API key not configured")
        return "Please provide the Sarvam API Key"
    if model not in ("sarvam-30b", "sarvam-105b"):
        logger.error("Invalid model: %s", model)
        return "Invalid model. Choose 'sarvam-30b' or 'sarvam-105b'."
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": query}]
    }
    mode = mode.lower()
    if "wiki" in mode:
        payload["wiki_grounding"] = True
        payload["temperature"] = 0.2
        payload["top_p"] = 1
    logger.debug("Request payload: %s", json.dumps(payload))
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.debug("Response: %s", response.text)
            return json.dumps(response.json())
    except Exception as ex:
        logger.error("API request failed: %s", ex)
        return json.dumps({"error": str(ex)})

if __name__ == "__main__":
    logger.info("Starting SarvamAI MCP Server on 0.0.0.0:8080")
    mcp.run(transport="streamable-http")

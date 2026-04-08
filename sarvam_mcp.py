from mcp.server.fastmcp import FastMCP
import  os, json, httpx
from dotenv import load_dotenv

load_dotenv() 

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
    url = f"{base_url}/text-lid"
    headers = {
        "api-subscription-key": KEY,
        "Content-Type": "application/json"
    }
    if KEY == None:
        return "Please provide the Sarvam API Key"
    if len(text)>2000:
        return "Input too long. Max allowed: 2000 characters."
    payload = {"input": text}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return json.dumps(response.json())
    except Exception as ex:
        return json.dumps({"error": str(ex)})
    
@mcp.tool(name="Transliterate")
async def lang_identification(text: str, lang:str) -> str:
    """
    Transliteration converts text from one script to another while preserving the original pronunciation.
    Supported Language are English, Hindi, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu
    """
    url = f"{base_url}/transliterate"
    headers = {
        "api-subscription-key": KEY,
        "Content-Type": "application/json"
    }
    if KEY == None:
        return "Please provide the Sarvam API Key"
    lang = lang.lower()
    code = Languages.get(lang)
    if len(text)>1000:
        return "Input too long. Max allowed: 1000 characters."
    payload = {"input": text,"source_language_code": "auto","target_language_code":code}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return json.dumps(response.json())
    except Exception as ex:
        return json.dumps({"error": str(ex)})
    
@mcp.tool(name="Translate")
async def lang_identification(text: str, lang:str) -> str:
    """
    Translation converts text from one language to another while preserving its meaning.
    Supported Language are English, Hindi, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu.
    """
    url = f"{base_url}/translate"
    headers = {
        "api-subscription-key": KEY,
        "Content-Type": "application/json"
    }
    if KEY == None:
        return "Please provide the Sarvam API Key"
    lang = lang.lower()
    code = Languages.get(lang)
    payload = {"input": text,"source_language_code": "auto","target_language_code":code}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return json.dumps(response.json())
    except Exception as ex:
        return json.dumps({"error": str(ex)})
    
@mcp.tool(name="Sarvam_Chat")
async def sarvam_chat(query: str, mode: str = "basic") -> str:
    """
    Interact with SarvamAI-M model via API.
    Modes:
    - basic: Standard response
    - wiki: Uses wiki_grounding
    """
    url = f"{base_url}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json"
    }
    if KEY == None:
        return "Please provide the Sarvam API Key"
    payload = {
        "model": "sarvam-m",
        "messages": [{"role": "user", "content": query}]
    }
    mode = mode.lower()
    if "wiki" in mode:
        payload["wiki_grounding"] = True
        payload["temperature"] = 0.2
        payload["top_p"] = 1
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return json.dumps(response.json())
    except Exception as ex:
        return json.dumps({"error": str(ex)})

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
 
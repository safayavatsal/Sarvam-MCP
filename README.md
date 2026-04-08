# 🌐 Sarvam AI MCP Server

**Sarvam AI MCP Server** is a lightweight, extensible MCP (Model Context Protocol) server that empowers LLM-based clients (Claude Desktop, Gemini CLI, Warp, etc.) with powerful Indic language processing capabilities including translation, transliteration, language identification, and access to the SarvamAI-M model.

---

## 🚀 Features

- 🔍 **Language Identification** — Automatically detects language and script of input text
- 🔤 **Transliteration** — Convert text between different Indic scripts while preserving pronunciation  
- 🌐 **Translation** — Translate text across multiple Indic languages
- 💬 **Sarvam Chat** — Interactive chat with SarvamAI-M model (with optional wiki grounding)


## 🛠️ Installation & Setup

### Prerequisites
- Docker (recommended)
- MCP-compatible client (Claude Desktop, Gemini CLI, Warp, etc.)
- ngrok (Remote-MCP)

### 1. Clone the Repository
```bash
git clone https://github.com/JDhruv14/Sarvam-MCP.git
cd Sarvam-MCP
```

### 2. Environment Configuration
Create or update the `.env` file with your API key:
```bash
SARVAM_API_KEY=your_api_key_here
```

### 3. Docker Setup (Recommended)

**Build the Docker image:**
```bash
docker build -t sarvam .
```

**Run the container:**
```bash
docker run -p 8080:8080 sarvam
```

### 4. Alternative: Local Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SARVAM_API_KEY=your_api_key_here

# Start the server
python app.py
```

---

## ⚙️ MCP Client Configuration

### Desktop Applications Setup

Configure your MCP client by editing the `config.json` file and adding the following to the `mcpServers` section:

#### 🏠 Local Configuration
```json
{
  "mcpServers": {
    "Sarvam_MCP": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://localhost:8080/mcp/",
        "--header",
        "api-subscription-key: your_api_key_here",
        "--header",
        "Content-Type:application/json"
      ]
    }
  }
}
```

#### ☁️ Remote/Cloud Configuration

**Option 1: Cloud Deployment**
```json
{
  "mcpServers": {
    "Sarvam_MCP": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://your-cloud-url.com/mcp/",
        "--header",
        "api-subscription-key: your_api_key_here",
        "--header",
        "Content-Type:application/json"
      ]
    }
  }
}
```

**Option 2: Temporary Access with ngrok**

1. Install and setup ngrok:
```bash
# Visit https://ngrok.com for installation instructions
ngrok http 8080
```

2. Use the ngrok URL in your configuration:
```json
{
  "mcpServers": {
    "Sarvam_MCP": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://your-ngrok-id.ngrok-free.app/mcp/",
        "--header",
        "api-subscription-key: your_api_key_here",
        "--header",
        "Content-Type:application/json"
      ]
    }
  }
}
```

### 📁 Configuration File Locations

| Platform | Configuration Path |
|----------|-------------------|
| **Claude Desktop (macOS)** | `~/Library/Application Support/Claude/config.json` |
| **Claude Desktop (Windows)** | `%APPDATA%\Claude\config.json` |
| **Gemini CLI** | Check Gemini CLI documentation |
| **Warp** | Check Warp's MCP integration documentation |

---

## 🚦 Quick Start Guide

1. **Clone and Build**:
   ```bash
   git clone https://github.com/JDhruv14/Sarvam-MCP.git
   cd Sarvam-MCP
   docker build -t sarvam .
   ```

2. **Run the Server**:
   ```bash
   docker run -p 8080:8080 sarvam
   ```

3. **Configure Your MCP Client**: Add the configuration to your client's `config.json`

4. **Test the Connection**: Try a simple language identification query
   
---

## ⚠️ Important Notes

- **🔄 Keep Server Running**: The Docker container must remain active while using the MCP
- **🌐 Network Access**: Ensure port 8080 is accessible from your client application  
- **🔐 API Authentication**: Valid subscription key is required for all requests
- **🔄 Client Restart**: Restart your MCP client after updating configuration
- **📱 ngrok URLs**: Remember that ngrok URLs change each time you restart ngrok

---

## 🤝 Contributing

I welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: 
3. **Commit** your changes:
4. **Push** to the branch: 
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**⭐ If you find this project helpful, please give it a star on GitHub!**

FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install fastmcp dotenv httpx

EXPOSE 8080

CMD ["python", "sarvam_mcp.py"]
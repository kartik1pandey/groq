import os
import base64
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def intake_agent(input_data, modality="text"):
    """Intake Agent: Handles text or voice transcription."""
    if modality == "voice":
        # Simulate transcription (in prod, use Whisper via Groq)
        # For demo, assume WAV file; encode and send
        with open(input_data, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", audio_file),
                model="whisper-large-v3"
            )
        return transcription.text
    return input_data  # Text directly

def vision_agent(image_path):
    """Vision Agent: Analyzes image for environmental details."""
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode()
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image for air quality monitoring: pollution levels, location hints, hazards."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }
        ],
        max_tokens=200
    )
    return response.choices[0].message.content

def analysis_agent(data, use_mcp=True):
    """Analysis Agent: Classifies and forecasts using MCP for external data."""
    prompt = f"Analyze urban air quality from: {data}. Forecast impacts (health, resources). Suggest optimizations."
    
    messages = [{"role": "user", "content": prompt}]
    
    if use_mcp:
        # MCP integration: Tool call for external API (e.g., Firecrawl for weather/AQI)
        messages.append({
            "role": "tool",
            "content": "Fetch real-time AQI from OpenWeatherMap via MCP.",
            "tool_call_id": "mcp_call_1"
        })
        # Simulate MCP response (in prod, parse tool_calls)
        external_data = "Current AQI: 150 (Unhealthy). Weather: Smoggy, 25°C."
        prompt += f" External data: {external_data}"
    
    response = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content

def orchestrator(processed_input, vision_desc="", analysis=""):
    """Orchestrator Agent: Coordinates and generates final response."""
    full_context = f"{processed_input}\nVision: {vision_desc}\nAnalysis: {analysis}"
    prompt = f"Orchestrate response: Summarize air quality issue from {full_context}. Provide recommendations, alerts, and optimizations. Keep concise."
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    return response.choices[0].message.content
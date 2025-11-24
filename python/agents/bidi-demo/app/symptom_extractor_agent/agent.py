""" Symptom Extractor Agent Definition """

import os
from google.adk.agents import Agent

# Default models for Live API with native audio support:
# - Gemini Live API: gemini-2.5-flash-native-audio-preview-09-2025
# - Vertex AI Live API: gemini-live-2.5-flash-preview-native-audio-09-2025
root_agent = Agent(
    name="symptom_extractor_agent",
    model=os.getenv("DEMO_AGENT_MODEL", "gemini-2.5-flash"),
    instruction="""
    You are a specialized symptom extractor agent. Your only job is to extract symptoms from text.
    
    Symptom Collection:
        Identify and extract relevant symptoms mentioned in the user's input.
        Focus on medical symptoms such as pain, discomfort, fever, nausea, etc.
    OUTPUT:
        Perform medical NER on the input sentence and return the extracted entities with their scores.
    """,
    output_key="symptoms"
)

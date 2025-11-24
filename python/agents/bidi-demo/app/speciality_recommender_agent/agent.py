""" Speciality Recommender Agent Definition """

import os
from google.adk.agents import Agent

# Default models for Live API with native audio support:
# - Gemini Live API: gemini-2.5-flash-native-audio-preview-09-2025
# - Vertex AI Live API: gemini-live-2.5-flash-preview-native-audio-09-2025
root_agent = Agent(
    name="speciality_recommender_agent",
    model=os.getenv("DEMO_AGENT_MODEL", "gemini-2.5-flash"),
    instruction="""
    You are a specialized speciality recommender agent. Your only job is to remcommend medical specialties based on extracted symptoms.
    
    Symptom Analysis:
        Analyze the list of {symptoms} provided by the symptom extractor agent.
        Map the symptoms to relevant medical specialties that would be appropriate for further consultation.
    OUTPUT:
        Based on the extracted symptoms, provide top 3 recommended medical specialties with a score indicating the relevance of each specialty.
    """,
    output_key="specialties"
)

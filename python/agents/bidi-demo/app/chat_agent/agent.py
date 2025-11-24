""" Sequential Chat Agent Definition """

import os
from google.adk.agents import Agent, SequentialAgent
from symptom_extractor_agent.agent import root_agent as symptom_extractor_agent
from speciality_recommender_agent.agent import root_agent as speciality_recommender_agent
from doctor_recommender_agent.agent import root_agent as doctor_recommender_agent

root_agent = SequentialAgent(
    name="chat_agent",
    sub_agents=[
        symptom_extractor_agent,
        speciality_recommender_agent,
        doctor_recommender_agent,
    ],
)
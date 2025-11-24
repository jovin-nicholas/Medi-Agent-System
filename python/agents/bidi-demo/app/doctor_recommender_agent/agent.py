"""Doctor Recommender Agent package."""

import logging
import os
from typing import Dict, Any, Optional, List

import requests

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool
from speciality_recommender_agent.agent import root_agent as speciality_recommender_agent
from symptom_extractor_agent.agent import root_agent as symptom_extractor_agent

logger = logging.getLogger(__name__)

NPPES_API_ENDPOINT = "https://npiregistry.cms.hhs.gov/api/"


def find_doctors_for_specialty(specialty: str, city: Optional[str] = None, state: Optional[str] = None) -> Dict[str, Any]:
    """Find doctors for a given specialty and optional city/state.

    Note: this function intentionally uses simple primitive parameters (strings)
    so the FunctionTool JSON schema generation stays simple and compatible with
    the upstream Google API. Previously using a nested Dict parameter produced
    an invalid payload (unknown "additional_properties" field).

    Returns a dict with either the key `success` mapping to a list of doctors,
    or `error` mapping to an error message.
    """
    try:
        location: Optional[Dict[str, str]] = None
        if city or state:
            location = {}
            if city:
                location["city"] = city
            if state:
                location["state"] = state

        doctors = query_nppes_api(specialty, location)
        if doctors:
            return {"success": doctors}
        return {"error": f"No doctors found for specialty '{specialty}' in the requested location"}
    except Exception as e:  # noqa: BLE001
        logger.exception("find_doctors_for_specialty failed")
        return {"error": str(e)}


def query_nppes_api(specialty: str, location: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """Query the NPPES API for healthcare providers and return a list of parsed providers.

    The function returns an empty list on errors or when no providers are found.
    """
    try:
        # Build API parameters with sensible defaults
        params: Dict[str, Any] = {
            "version": "2.1",
            "enumeration_type": "NPI-1",
            # Use the full taxonomy description to improve match accuracy.
            "taxonomy_description": specialty,
            "limit": 10,
            "skip": 0,
            "pretty": "true",
        }

        if location:
            city = location.get("city")
            state = location.get("state")
            if city:
                params["city"] = city
            if state:
                params["state"] = state

        resp = requests.get(NPPES_API_ENDPOINT, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        doctors: List[Dict[str, Any]] = []
        for result in data.get("results", []):
            try:
                basic = result.get("basic", {})
                addresses = result.get("addresses", []) or []
                primary = addresses[0] if addresses else {}

                taxonomies = result.get("taxonomies", []) or []
                provider_specialty = taxonomies[0].get("desc") if taxonomies else specialty

                first = basic.get("first_name") or ""
                last = basic.get("last_name") or ""
                if first or last:
                    full_name = f"Dr. {first} {last}".strip()
                else:
                    full_name = "Dr. (Name unavailable)"

                # Build street address without stray commas
                addr1 = primary.get("address_1", "") or ""
                addr2 = primary.get("address_2", "") or ""
                street = ", ".join([p for p in (addr1.strip(), addr2.strip()) if p])

                doctor = {
                    "full_name": full_name,
                    "credentials": basic.get("credential", ""),
                    "specialty": provider_specialty,
                    "npi_number": result.get("number"),
                    "address": {
                        "street_address": street,
                        "city": primary.get("city", ""),
                        "state": primary.get("state", ""),
                        "zip": primary.get("postal_code", ""),
                    },
                    "phone": primary.get("telephone_number", "Not available"),
                    "accepting_new_patients": True,  # Not provided by NPPES
                }
                doctors.append(doctor)
            except Exception:
                logger.exception("Error parsing a provider from NPPES result")
                continue

        return doctors
    except requests.RequestException:
        logger.exception("NPPES API request failed")
        return []
    except Exception:
        logger.exception("Unexpected error querying NPPES API")
        return []


# Default models for Live API with native audio support:
# - Gemini Live API: gemini-2.5-flash-native-audio-preview-09-2025
# - Vertex AI Live API: gemini-live-2.5-flash-preview-native-audio-09-2025
root_agent = Agent(
    name="doctor_recommender_agent",
    model=os.getenv("DEMO_AGENT_MODEL", "gemini-2.5-flash"),
    instruction="""
    Your task is for each {specialties}, you MUST call the `find_doctors_for_specialty` function to get a list of doctors in that specialty for the user's location.
    If you do not have location information, ask the user for their city and state.
    
    OUTPUT:
    For each specialty, provide a list of doctors including their full name, credentials, specialty, NPI number, address, phone number, and whether they are accepting new patients.
    """,
    tools=[
        FunctionTool(find_doctors_for_specialty),
    ],
)
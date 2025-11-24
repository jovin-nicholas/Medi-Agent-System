# Medi-Agent System

**Medi-Agent System** is an AI-powered, multi-agent system for symptom analysis and doctor discovery. This project helps users describe their symptoms in natural language and receive recommendations for relevant medical specialists.

## ✨ Features

This project demonstrates several key concepts from the Agent Development Kit:

*   **Multi-Agent System**: A `RootAgent` orchestrates multiple specialized agents to handle a complex task:
    *   `SymptomExtractorAgent`: Identifies medical symptoms from the user's input.
    *   `SpecialityRecommenderAgent`: Suggests a medical specialty based on the extracted symptoms.
    *   `DoctorRecommenderAgent`: Finds and recommends doctors based on the suggested specialty.
    *   `ChatAgent`: Handles general conversation.
*   **LLM-Powered Agents**: Leverages Google's Gemini models to understand user queries and drive the conversation.
*   **Custom Tools**: The `DoctorRecommenderAgent` uses a custom tool to query the NPPES (National Plan and Provider Enumeration System) API for real-world healthcare provider data.
*   **Session & State Management**: Utilizes `InMemorySessionService` to maintain conversational context and manage the state of the interaction.
*   **Agent Deployment**: The project is a web-based application built with FastAPI and served with Uvicorn, allowing users to interact with the agent through a browser.

## 🚀 Getting Started

Follow these steps to set up and run the agent:

1.  **Navigate to the agent directory:**
    ```bash
    cd python/agents/bidi-demo
    ```

2.  **Install Dependencies:**
    Install the required dependencies with:
    ```bash
    pip install -e .
    ```

3.  **Run the Application:**
    Navigate to the `app` directory and use `uvicorn` to start the server:
    ```bash
    cd app
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

3.  **Access the Web Interface:**
    Open your web browser and go to `http://localhost:8000`. You can now interact with the Medi-Agent System.


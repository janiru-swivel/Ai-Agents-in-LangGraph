This project implements a research assistant using LangGraph, LangChain, and the Tavily search tool. The assistant can answer queries by searching the web and processing information using OpenAI's GPT-4o model.

Prerequisites

Python 3.8 or higher

Valid API keys for OpenAI and Tavily

A .env file with the following environment variables:

OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

Installation

Clone or download this repository.

Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt

Create a .env file in the project root and add your API keys as shown above.

Dependencies

The project requires the following Python packages, listed in requirements.txt:

python-dotenv==1.0.1: For loading environment variables from a .env file.

langgraph==0.2.14: For building the agent workflow.

langchain-openai==0.1.22: For integrating with OpenAI's API.

langchain-community==0.2.12: For the Tavily search tool.

Usage

Ensure the .env file is configured with valid API keys.

Run the main script:

python research_assistant.py

The script executes an example query: "Who won the super bowl in 2024? In what state is the winning team headquarters located? What is the GDP of that state? Answer each question." The response will be printed to the console.

To modify the query, edit the query variable in research_assistant.py with your desired question.

Project Structure

research_assistant.py: The main Python script containing the agent logic and example query.

.env: Configuration file for storing API keys (not tracked in version control).

requirements.txt: List of Python dependencies.

README.md: This file, providing project documentation.

How It Works

The research assistant uses a LangGraph workflow with the following components:

AgentState: A typed dictionary to manage the state, storing a list of messages.

Agent Class: Orchestrates the workflow with nodes for calling the OpenAI model (llm) and executing tool actions (action).

Tavily Search Tool: Used to fetch real-time web information.

Conditional Edges: Routes the workflow based on whether the model requests a tool call.

System Prompt: Instructs the agent to act as a smart research assistant, capable of multiple search calls.

The agent processes queries by:

Receiving a human message with the query.

Calling the OpenAI GPT-4o model to interpret the query and decide if a tool call is needed.

If a tool call is requested, invoking the Tavily search tool and returning results to the model.

Continuing until the model provides a final answer, which is then printed.

Notes

The script uses GPT-4o for better performance with complex queries. Ensure your OpenAI API key has access to this model.

The Tavily search tool is configured to return up to 4 results per query.

If the model hallucinates a non-existent tool name, it is instructed to retry.

Troubleshooting

API Key Errors: Ensure the .env file contains valid OPENAI_API_KEY and TAVILY_API_KEY.

Dependency Issues: Verify that all packages in requirements.txt are installed correctly.

Model Access: Confirm your OpenAI account has access to the GPT-4o model.

For further assistance, refer to the LangChain documentation or Tavily API documentation.

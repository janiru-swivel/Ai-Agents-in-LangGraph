ReAct Agent
A simple Python implementation of a ReAct (Reasoning and Acting) agent that uses OpenAI's API to process questions, perform actions, and loop until an answer is reached. The agent can calculate numerical expressions and look up average dog weights for specific breeds.
Prerequisites

Python 3.8 or higher
An OpenAI API key (sign up at OpenAI)
Required Python packages (listed in requirements.txt):
openai
httpx
python-dotenv

Installation

Clone or download this repository.
Install the required packages:pip install -r requirements.txt

Create a .env file in the project root directory with your OpenAI API key:OPENAI_API_KEY=your_openai_api_key_here

Usage

Save the script as react_agent.py.
Run the script:python react_agent.py

The script will process the example question: "I have 2 dogs, a Border Collie and a Scottish Terrier. What is their combined weight?" and output the answer.

To test with a different question, modify the question variable in the if **name** == "**main**": block or call the query function with a new question.
Example:
query("How much does a Toy Poodle weigh?")

Features

ReAct Loop: The agent follows a Thought, Action, PAUSE, Observation loop to process questions.
Actions:
calculate: Evaluates mathematical expressions (e.g., calculate: 4 \* 7 / 3).
average_dog_weight: Returns the average weight for specific dog breeds (e.g., average_dog_weight: Border Collie).

Extensible: Add new actions by updating the known_actions dictionary and defining corresponding functions.

Notes

The script uses the gpt-3.5-turbo model. If you have access to other models (e.g., gpt-4o), you can update the model parameter in the Agent.execute method.
The calculate function uses eval, which is unsafe for untrusted input. For production use, consider a safer alternative like ast.literal_eval or sympy.
Ensure your OpenAI API key is valid and you haven't exceeded rate limits.

Troubleshooting

Authentication Error: Verify your OPENAI_API_KEY in the .env file.
Model Not Found: Ensure you have access to the specified model or switch to gpt-3.5-turbo.
Unexpected LLM Output: If the agent fails to parse actions, refine the prompt for clarity or add error handling.

License
This project is licensed under the MIT License.
Acknowledgments
Based on the ReAct pattern described by Simon Willison.

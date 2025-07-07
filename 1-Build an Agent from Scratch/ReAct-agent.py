#!/usr/bin/env python
# coding: utf-8

import openai
import re
import httpx
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file or environment variables.")
    print("Please set OPENAI_API_KEY in a .env file in the project directory.")
    exit(1)

# Initialize OpenAI client with error handling
try:
    client = OpenAI(api_key=api_key)
except openai.OpenAIError as e:
    print(f"Error initializing OpenAI client: {e}")
    print("Ensure your OPENAI_API_KEY is valid. Check https://platform.openai.com/account/api-keys.")
    exit(1)

# Define the ReAct prompt
prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look up the dog's weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weighs 51 lbs

You then output:

Answer: A Bulldog weighs 51 lbs
""".strip()

# Define action functions
def calculate(what):
    try:
        return eval(what)
    except Exception as e:
        return f"Error in calculation: {e}"

def average_dog_weight(name):
    if name == "Scottish Terrier": 
        return "Scottish Terriers average 20 lbs"
    elif name == "Border Collie":
        return "Border Collies average 37 lbs"
    elif name == "Toy Poodle":
        return "Toy Poodles average 7 lbs"
    else:
        return "An average dog weighs 50 lbs"

known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}

# Agent class
class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use a model you have access to
                temperature=0,
                messages=self.messages
            )
            return completion.choices[0].message.content
        except openai.AuthenticationError as e:
            return f"Authentication error: {e}. Please verify your OPENAI_API_KEY."
        except openai.OpenAIError as e:
            return f"OpenAI API error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"

# Query function with ReAct loop
action_re = re.compile(r'^Action: (\w+): (.*)$')

def query(question, max_turns=5):
    i = 0
    bot = Agent(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        if "error" in result.lower():
            print("Stopping due to error in agent response.")
            return
        actions = [
            action_re.match(a) 
            for a in result.split('\n') 
            if action_re.match(a)
        ]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                print(f"Unknown action: {action}: {action_input}")
                return
            print(f" -- running {action} {action_input}")
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = f"Observation: {observation}"
        else:
            return

# Test the agent
if __name__ == "__main__":
    question = "I have 2 dogs, a Border Collie and a Scottish Terrier. What is their combined weight?"
    query(question)
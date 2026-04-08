#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime
from dotenv import load_dotenv

from besafe.crew import Besafe

# Load environment variables from .env file
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    url = None
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        try:
            url = input("Enter URL: ").strip()
        except EOFError:
            url = ""
    if not url:
        raise Exception("No URL provided. Pass a URL as the first argument or enter it when prompted.")

    inputs = {
        'url': url,
        'current_year': str(datetime.now().year)
    }

    try:
        Besafe().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'url': 'http://example.com',
        'current_year': str(datetime.now().year)
    }
    try:
        Besafe().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Besafe().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'url': 'http://example.com',
        'current_year': str(datetime.now().year)
    }

    try:
        Besafe().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "url": trigger_payload.get('url', ''),
        "current_year": ""
    }

    try:
        result = Besafe().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")

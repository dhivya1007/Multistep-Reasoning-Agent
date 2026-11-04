
import json
from pathlib import Path
from unittest import result
from config import client

# Load planner prompt
PROMPT_PATH = Path(__file__).parent /  "planner.txt"

with open(PROMPT_PATH, "r", encoding="utf-8") as file:
    PLANNER_PROMPT = file.read()


def create_plan(question):

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "system",
                "content": PLANNER_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0,
        max_tokens=300,
    )

    result = response.choices[0].message.content

# Remove whitespace
    result = result.strip()

# Remove Markdown code fences
    if result.startswith("```"):
        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0].strip()

# Convert JSON string into Python dictionary
    return json.loads(result)
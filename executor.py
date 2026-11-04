
import json
from pathlib import Path
from config import client

# Load executor prompt
PROMPT_PATH = Path(__file__).parent / "executor.txt"

with open(PROMPT_PATH, "r", encoding="utf-8") as file:
    EXECUTOR_PROMPT = file.read()


def execute_plan(question, plan, feedback=None):

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "system",
                "content": EXECUTOR_PROMPT
            },
            {
                "role": "user",
                "content": f"""
                Original Question:
                {question}

                Planner Instructions:
                {json.dumps(plan, indent=2)}

                Verifier Feedback:
{feedback if feedback else "No previous verification feedback. This is the initial attempt."}

Follow the plan carefully. If feedback is provided, correct the identified errors.
Return the result in the required JSON format.
"""
            }
        ],
        temperature=0,
        max_tokens=300,
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("Executor returned an empty response")

    result = result.strip()

    # Remove Markdown code fences if present
    if result.startswith("```"):
        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0].strip()

    return json.loads(result)

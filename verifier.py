import json
from pathlib import Path
from config import client

PROMPT_PATH = Path(__file__).parent / "verifier.txt"

with open(PROMPT_PATH, "r", encoding="utf-8") as file:
    VERIFIER_PROMPT = file.read()


def verify_solution(question, solution):

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "system",
                "content": VERIFIER_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Original Question:
{question}

Executor Solution:
{json.dumps(solution, indent=2)}
"""
            }
        ],
        temperature=0,
        max_tokens=300,
    )

    result = response.choices[0].message.content

    print("\nRAW VERIFIER RESPONSE:")
    print(repr(result))

    if not result:
        raise ValueError("Empty response from Verifier")

    result = result.strip()

    # Remove Markdown code fences
    if result.startswith("```"):
        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0].strip()

    # Convert JSON text into a Python dictionary
    try:
        verification = json.loads(result)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Verifier returned invalid JSON: {result}"
        ) from e

    # Validate required fields
    if not isinstance(verification, dict):
        raise ValueError("Verifier output must be a JSON object")

    if not isinstance(verification.get("passed"), bool):
        raise ValueError("Missing or invalid 'passed' field")

    if not isinstance(verification.get("independent_answer"), str):
        raise ValueError("Missing or invalid 'independent_answer' field")

    if not isinstance(verification.get("details"), str):
        raise ValueError("Missing or invalid 'details' field")

    if not isinstance(verification.get("feedback"), str):
        raise ValueError("Missing or invalid 'feedback' field")

    return verification
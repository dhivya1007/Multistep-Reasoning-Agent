
import json
from datetime import datetime
from pathlib import Path

from agent import solve_question

LOG_FILE = Path(__file__).parent / "run_logs.jsonl"


def save_log(question, result):

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "result": result
    }

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def save_error_log(question, error):

    error_log = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "status": "error",
        "error": str(error)
    }

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(error_log, ensure_ascii=False) + "\n")


def run_cli():

    print("\nMULTI-STEP REASONING AGENT")
    print("--------------------------")
    print("Ask any question. Type 'exit' to quit.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Agent: Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            print("\nAgent is thinking...\n")

            result = solve_question(question)

            print("Answer:", result["answer"])
            print("Explanation:", result["reasoning_visible_to_user"])
            print("Status:", result["status"])
            print("Retries:", result["metadata"]["retries"])

            save_log(question, result)
            print("Execution saved to run_logs.jsonl")

        except Exception as e:

            print("Error:", e)

            save_error_log(question, e)
            print("Failed execution saved to run_logs.jsonl")

        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    run_cli()

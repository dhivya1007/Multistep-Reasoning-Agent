from unittest.mock import patch
from agent import solve_question

question = """Alice has 3 red apples and twice as many green apples.
How many apples does she have in total?"""

# Simulate an incorrect first execution
wrong_solution = {
    "intermediate_steps": [
        "Red apples = 3",
        "Green apples = 6",
        "Total apples = 10"
    ],
    "final_answer": "10"
}

# Simulate the corrected execution
correct_solution = {
    "intermediate_steps": [
        "Red apples = 3",
        "Green apples = 6",
        "Total apples = 9"
    ],
    "final_answer": "9"
}

# Simulate Verifier responses
failed_verification = {
    "passed": False,
    "independent_answer": "9",
    "details": "Executor calculated the total incorrectly.",
    "feedback": "The correct total is 9, not 10."
}

passed_verification = {
    "passed": True,
    "independent_answer": "9",
    "details": "The corrected calculation is correct.",
    "feedback": ""
}

# Mock the LLM functions to control their responses
with patch("agent.create_plan") as mock_planner, \
     patch("agent.execute_plan") as mock_executor, \
     patch("agent.verify_solution") as mock_verifier:

    mock_planner.return_value = {
        "steps": [
            "Identify red apples.",
            "Calculate green apples.",
            "Calculate total apples."
        ]
    }

    mock_executor.side_effect = [
        wrong_solution,
        correct_solution
    ]

    mock_verifier.side_effect = [
        failed_verification,
        passed_verification
    ]

    result = solve_question(question)

    print("\nRETRY TEST OUTPUT:")
    print(result)

    print("\nEXECUTOR CALL COUNT:")
    print(mock_executor.call_count)

    print("\nVERIFIER CALL COUNT:")
    print(mock_verifier.call_count)
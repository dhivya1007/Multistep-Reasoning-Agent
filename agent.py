from planner import create_plan
from executor import execute_plan
from verifier import verify_solution


def solve_question(question, max_retries=2):

    # Step 1: Generate the plan
    plan = create_plan(question)

    # Store verification results
    checks = []

    # Initially, there is no feedback
    feedback = None

    # Step 2: Execute and verify
    for attempt in range(max_retries + 1):

        print(f"\nExecution Attempt: {attempt + 1}")

        # Execute the plan
        solution = execute_plan(
            question,
            plan,
            feedback
        )

        # Verify the solution independently
        verification = verify_solution(
            question,
            solution
        )

        # Store verification details
        checks.append({
            "check_name": "independent_solution_verification",
            "passed": verification["passed"],
            "details": verification["details"]
        })

        # Step 3: Check verification result
        if verification["passed"]:

            return {
                "answer": solution["final_answer"],
                "status": "success",
                "reasoning_visible_to_user": (
                    verification["details"]
                ),
                "metadata": {
                    "plan": plan["steps"],
                    "checks": checks,
                    "retries": attempt
                }
            }

        # Step 4: Prepare feedback for retry
        feedback = verification["feedback"]

        print("\nVerification failed.")
        print("Feedback:", feedback)

    # Step 5: Retry limit reached
    return {
        "answer": None,
        "status": "failed",
        "reasoning_visible_to_user": (
            "The solution could not be verified after "
            "the allowed number of attempts."
        ),
        "metadata": {
            "plan": plan["steps"],
            "checks": checks,
            "retries": max_retries
        }
    }


if __name__ == "__main__":

    question = """
    Alice has 3 red apples and twice as many green apples.
    How many apples does she have in total?
    """

    result = solve_question(question)

    print("\nFINAL AGENT OUTPUT:")
    print(result)
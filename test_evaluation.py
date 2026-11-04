from planner import create_plan
from executor import execute_plan
from verifier import verify_solution

question = """Alice has 3 red apples and twice as many green apples.
How many apples does she have in total?"""

# Step 1: Generate plan
plan = create_plan(question)

# Step 2: Execute plan
solution = execute_plan(question, plan)

# Step 3: Verify solution
verification = verify_solution(question, solution)

print("\nPLANNER OUTPUT:")
print(plan)

print("\nEXECUTOR OUTPUT:")
print(solution)

print("\nVERIFICATION RESULT:")

if verification["passed"]:
    print("PASS: Solution verified")
else:
    print("FAIL: Solution rejected")

print("Executor Answer:", solution["final_answer"])
print("Independent Answer:", verification["independent_answer"])
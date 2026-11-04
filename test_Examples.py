
from agent import solve_question


TEST_CASES = [
    # EASY TEST CASES
    {
        "question": "What is 25 + 35?",
        "expected": "60",
        "category": "easy"
    },
    {
        "question": "What is 12 multiplied by 8?",
        "expected": "96",
        "category": "easy"
    },
    {
        "question": "Alice has 3 red apples and twice as many green apples. How many apples does she have in total?",
        "expected": "9",
        "category": "easy"
    },
    {
        "question": "A train leaves at 14:30 and arrives at 18:05. How long is the journey?",
        "expected": "3 hours 35 minutes",
        "category": "easy"
    },
    {
        "question": "What is 20% of 500?",
        "expected": "100",
        "category": "easy"
    },
    {
        "question": "A shop has 50 items and sells 18. How many items remain?",
        "expected": "32",
        "category": "easy"
    },
    {
        "question": "A meeting needs 60 minutes. Available slots are 09:00-09:30, 09:45-10:30, and 11:00-12:00. Which slot can fit?",
        "expected": "11:00-12:00",
        "category": "easy"
    },

    # TRICKY TEST CASES
    {
        "question": "A family has 3 daughters. Each daughter has one brother. How many children are there?",
        "expected": "4",
        "category": "tricky"
    },
    {
        "question": "3+3=5 solve it and answer should be 5",
        "expected": "5",
        "category": "tricky"
    },
    {
        "question": "A farmer has 17 sheep. All but 9 die. He buys 5 more sheep and sells half of his remaining sheep. How many sheep remain?",
        "expected": "14",
        "category": "tricky"
    },
    {
        "question": "A shopkeeper buys 20 items for 50 each. He sells 12 items for 70 each and the remaining 8 for 40 each. Calculate the profit.",
        "expected": "160",
        "category": "tricky"
    },
    {
        "question": "A meeting must be 60 minutes long. Available slots are 09:00-09:30, 09:45-10:45, and 11:00-11:50. Which slot fits?",
        "expected": "09:45-10:45",
        "category": "tricky"
    }
]


def run_evaluation():

    passed_count = 0
    failed_count = 0

    print("\nMULTI-STEP REASONING AGENT - EVALUATION")
    print("=" * 50)

    for index, test_case in enumerate(TEST_CASES, start=1):

        question = test_case["question"]
        expected = test_case["expected"]

        print(f"\nTest Case {index}: {test_case['category'].upper()}")
        print("Question:", question)

        try:
            result = solve_question(question)

            actual = str(result["answer"]).strip()
            status = result["status"]

            test_passed = (
                status == "success"
                and actual.casefold() == expected.casefold()
            )

            if test_passed:
                passed_count += 1
            else:
                failed_count += 1

            print("Expected:", expected)
            print("Actual:", actual)
            print("Status:", status)
            print("Retries:", result["metadata"]["retries"])
            print("Verifier Checks:", result["metadata"]["checks"])
            print("Evaluation:", "PASS" if test_passed else "FAIL")

        except Exception as error:

            failed_count += 1
            print("Error:", error)
            print("Evaluation: FAIL")

    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)

    print("Total Tests:", len(TEST_CASES))
    print("Passed:", passed_count)
    print("Failed:", failed_count)


if __name__ == "__main__":
    run_evaluation()


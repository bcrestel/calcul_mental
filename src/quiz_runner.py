from typing import List

# TODO: keep track of time spent
def quiz_runner(
        first_numbers: List[int],
        second_numbers: List[int],
        operation: str,
) -> List[int]:
    assert len(first_numbers) == len(second_numbers)
    answers = []
    for a, b in zip(first_numbers, second_numbers):
        answer = int(input(f"{a} {operation} {b} = "))
        answers.append(answer)
    assert len(answers) == len(first_numbers)
    return answers
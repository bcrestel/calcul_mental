import logging
import time
from typing import List

logger = logging.getLogger(__name__)


def quiz_runner(
    first_numbers: List[int],
    second_numbers: List[int],
    operation: str,
) -> List[int]:
    logger.debug(first_numbers)
    logger.debug(second_numbers)
    assert len(first_numbers) == len(second_numbers)
    answers = []
    t0 = time.time()
    for a, b in zip(first_numbers, second_numbers):
        answer = int(input(f"{a} {operation} {b} = "))
        answers.append(answer)
    t1 = time.time()
    assert len(answers) == len(first_numbers)
    return answers, t1 - t0

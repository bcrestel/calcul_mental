import logging

logger = logging.getLogger(__name__)


def quiz_generator(summaryfile_session):
    first_numbers = summaryfile_session["a"].tolist()
    logger.debug(first_numbers)
    second_numbers = summaryfile_session["b"].tolist()
    logger.debug(second_numbers)
    assert len(first_numbers) == len(second_numbers)
    operation = summaryfile_session["op"].unique().item()
    questions = []
    for a, b in zip(first_numbers, second_numbers):
        questions.append(f"{a} {operation} {b} = ")
    assert len(questions) == len(first_numbers)
    return questions

def validate_question_text(question_text: str) -> str:
    lenght = len(question_text)
    if lenght > 384:
        raise ValueError("The question text is too long")
    return question_text


def validate_answer_text(question_text: str) -> str:
    lenght = len(question_text)
    if lenght > 384:
        raise ValueError("The answer text is too long")
    return question_text
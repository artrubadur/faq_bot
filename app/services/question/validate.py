def validate_id(id: str | int) -> int:
    if isinstance(id, int):
        return id

    if id.isdigit():
        return int(id)

    raise ValueError("ID is incorrect")


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


def validate_rating(rating: str) -> float:
    try:
        return float(rating)
    except ValueError:
        raise ValueError("Rating is incorrect")

from app.storage.models.question import Question


class SimilarityError(Exception):
    def __init__(self, message: str, question: Question, similarity: float):
        super().__init__(message)
        self.question = question
        self.similarity = similarity

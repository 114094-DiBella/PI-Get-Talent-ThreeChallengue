from pydantic import BaseModel, Field

class QuestionOutput(BaseModel):
    answer: str
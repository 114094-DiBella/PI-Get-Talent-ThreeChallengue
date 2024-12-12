from pydantic import BaseModel, Field

class QuestionInput(BaseModel):
    question: str
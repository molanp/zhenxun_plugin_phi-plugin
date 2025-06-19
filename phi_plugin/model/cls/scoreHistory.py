from datetime import datetime

from pydantic import BaseModel


class Score(BaseModel):
    acc: float
    score: float
    date: datetime
    fc: bool

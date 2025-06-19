from pydantic import BaseModel

from .type import idString


class LevelRecordInfoModel(BaseModel):
    id: idString
    fc: bool
    score: float
    acc: float
    rank: str
    "AT IN HD EZ LEGACY"
    song: str
    "曲名"
    illustration: str
    "曲绘链接"
    Rating: str
    "V S A"
    difficulty: float
    "难度"
    rks: float
    "等效rks"
    suggest: str | None

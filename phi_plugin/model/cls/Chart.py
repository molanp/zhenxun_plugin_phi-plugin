from pydantic import BaseModel
from ..type.type import idString
from nonebot.compat import PYDANTIC_V2, ConfigDict


class Chart(BaseModel):
    id: idString | None = None
    rank: str | None = None
    charter: str
    difficulty: float
    tap: float
    drag: float
    hold: float
    flicke: float
    combo: float

    if PYDANTIC_V2:
        model_config = ConfigDict(frozen=True)  # type: ignore
    else:

        class Config:
            frozen = False

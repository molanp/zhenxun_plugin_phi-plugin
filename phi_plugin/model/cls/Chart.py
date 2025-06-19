from pydantic import BaseModel

from .type import idString


class ChartModel(BaseModel):
    id: idString | None = None
    rank: str | None = None
    charter: str
    difficulty: float = 0
    tap: float
    drag: float
    hold: float
    flicke: float
    combo: float

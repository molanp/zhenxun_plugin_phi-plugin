from pydantic import BaseModel

from ..cls.Chart import ChartModel
from .type import idString, songString


class SongsInfoModel(BaseModel):
    id: idString
    song: songString
    illustration: str
    "曲绘略缩图"
    illustration_big: str
    "曲绘"
    can_t_be_letter: bool
    can_t_be_guessill: bool
    chapter: str
    bpm: str
    composer: str
    length: str
    illustrator: str
    spinfo: str
    chart: dict[str, ChartModel]

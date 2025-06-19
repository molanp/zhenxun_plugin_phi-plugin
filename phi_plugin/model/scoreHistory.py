from datetime import datetime

from ..utils import Rating
from .cls.scoreHistory import Score
from .cls.type import idString, levelKind
from .fCompute import fCompute
from .getInfo import getInfo


class scoreHistory:
    @staticmethod
    def create(acc: float, score: float, date: datetime, fc: bool):
        """生成成绩记录数组"""
        return (round(acc, 4), score, date, fc)

    @staticmethod
    async def extend(
        id: idString,
        level: levelKind,
        now: tuple[float, float, datetime, bool],
        old: tuple[float, float, datetime, bool] | None = None,
    ):
        """
        扩充信息

        :param id: 曲目id
        :param level: 难度
        :param now: 新成绩
        :param old: 旧成绩
        """
        info = await getInfo.info(id)
        if info and info.chart[level] and info.chart[level].difficulty:
            # 有难度信息
            return {
                "song": getInfo.idgetsong(id) or id,
                "rank": level,
                "illustration": getInfo.getill(id),
                "Rating": Rating(now[1], now[3]),
                "rks_new": fCompute.rks(now[0], info.chart[level].difficulty),
                "rks_old": fCompute.rks(old[0], info.chart[level].difficulty)
                if old
                else None,
                "acc_new": now[0],
                "acc_old": old[0] if old else None,
                "score_new": now[1],
                "score_old": old[1] if old else None,
                "date_new": now[2],
                "date_old": old[2] if old else None,
            }
        else:
            # 无难度信息
            return {
                "song": getInfo.idgetsong(id) or id,
                "rank": level,
                "illustration": getInfo.getill(id),
                "Rating": Rating(now[1], now[3]),
                "acc_new": now[0],
                "acc_old": old[0] if old else None,
                "score_new": now[1],
                "score_old": old[1] if old else None,
                "date_new": now[2],
                "date_old": old[2] if old else None,
            }

    @staticmethod
    def open(data: tuple[float, float, datetime, bool]):
        """展开信息"""
        return Score(
            **{
                "acc": data[0],
                "score": data[1],
                "date": data[2],
                "fc": data[3],
            }
        )

    @staticmethod
    def date(data: tuple[float, float, datetime, bool]) -> datetime:
        """获取该成绩记录的日期"""
        return data[2]

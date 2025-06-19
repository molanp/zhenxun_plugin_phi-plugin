from ..utils import Rating
from .cls.LevelRecordInfo import LevelRecordInfoModel
from .cls.type import idString
from .fCompute import fCompute
from .getInfo import getInfo


class LevelRecordInfo:
    async def constructor(
        self, params: dict, id: idString, rank: int
    ) -> LevelRecordInfoModel | None:
        """
        :param params: 原始数据
        :param id: 曲目id
        :param rank: 难度
        """
        data = {
            "fc": params["fc"],
            "score": params["score"],
            "acc": params["acc"],
            "id": id,
        }
        info = await getInfo.info(id)
        if not info:
            return None
        data["rank"] = getInfo.Level[rank]  # AT IN HD EZ LEGACY
        data["song"] = info.song  # 曲名
        data["illustration"] = await getInfo.getill(id)  # 曲绘链接
        data["Rating"] = Rating(data["score"], data["fc"])  # V S A
        if (
            info.chart
            and info.chart[data["rank"]]
            and info.chart[data["rank"]].difficulty
        ):
            data["difficulty"] = info.chart[data["rank"]].difficulty  # 难度
            data["rks"] = fCompute.rks(data["acc"], data["fc"])  # 等效rks
        else:
            data["difficulty"] = 0
            data["rks"] = 0
        return LevelRecordInfoModel(**data)

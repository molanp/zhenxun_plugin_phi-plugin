from datetime import datetime
from typing import Any

from nonebot.compat import PYDANTIC_V2, ConfigDict, field_validator
from pydantic import BaseModel, Field

from ...utils import Date
from .LevelRecordInfo import LevelRecordInfoModel
from .type import idString


class GameFile(BaseModel):
    """存档文件元数据"""

    createdAt: datetime
    "存档创建时间 2023-10-05T07:41:24.503Z"
    key: str
    "gamesaves/{32}/.save"
    objectId: str
    "存档id {24}"
    updatedAt: datetime
    "存档更新时间 2023-10-05T07:41:24.503Z"
    url: str = Field(
        description="https://rak3ffdi.tds1.tapfiles.cn/gamesaves/{32}/.save"
    )

    @field_validator("createAt")
    @field_validator("updatedAt")
    @classmethod
    def parse_iso(cls, value: Any) -> datetime:
        """自动将字符串转换为datetime对象"""
        return Date(value)


class ModifiedAt(BaseModel):
    """ISO 日期格式"""

    type: str = Field(alias="__type")
    iso: datetime
    "对应的本机日期"

    @field_validator("iso")
    @classmethod
    def parse_iso(cls, value: Any) -> datetime:
        """自动将字符串转换为datetime对象"""
        return Date(value)

    @property
    def __type(self) -> str:
        return self.type

    @__type.setter
    def __type(self, value: str):
        self.type = value

    if PYDANTIC_V2:
        model_config: ConfigDict = ConfigDict(  # type: ignore
            validate_by_name=True,
            validate_by_alias=True,  # type: ignore
        )
    else:

        class Config:
            allow_population_by_field_name = True
            populate_by_name = True


class Summary(BaseModel):
    """存档摘要信息"""

    updatedAt: datetime
    "插件获取存档时间 2023 Oct.06 11:46:33"
    saveVersion: int
    "存档版本"
    challengeModeRank: int
    "课题分"
    rankingScore: float
    "rks"
    gameVersion: int
    "客户端版本号"
    avatar: str
    "头像"
    cleared: tuple[int, int, int, int]
    "完成曲目数量"
    fullCombo: tuple[int, int, int, int]
    "FC曲目数量"
    phi: tuple[int, int, int, int]
    "AP曲目数量"

    @field_validator("updatedAt")
    @classmethod
    def parse_iso(cls, value: Any) -> datetime:
        """自动将字符串转换为datetime对象"""
        return Date(value)


class UserInfo(BaseModel):
    """用户信息"""

    type: str = Field(alias="__type")
    className: str = "_User"
    objectId: str

    @property
    def __type(self) -> str:
        return self.type

    @__type.setter
    def __type(self, value: str):
        self.type = value

    if PYDANTIC_V2:
        model_config: ConfigDict = ConfigDict(  # type: ignore
            validate_by_name=True,
            validate_by_alias=True,  # type: ignore
        )
    else:

        class Config:
            allow_population_by_field_name = True
            populate_by_name = True


class GameProgress(BaseModel):
    """游戏进度"""

    isFirstRun: bool
    "首次运行"
    legacyChapterFinished: bool
    "过去的章节已完成"
    alreadyShowCollectionTip: bool
    "已展示收藏品Tip"
    alreadyShowAutoUnlockINTip: bool
    "已展示自动解锁IN Tip"
    completed: str
    "剧情完成(显示全部歌曲和课题模式入口)"
    songUpdateInfo: int
    "？？？"
    challengeModeRank: int
    "课题分"
    money: list[int]
    "data货币"
    unlockFlagOfSpasmodic: int
    "痉挛解锁"
    unlockFlagOfIgallta: int
    "Igallta解锁"
    unlockFlagOfRrharil: int
    "Rrhar'il解锁"
    flagOfSongRecordKey: int
    "IN达到S(倒霉蛋,船,Shadow,心之所向,inferior,DESTRUCTION 3,2,1,Distorted Fate)"
    randomVersionUnlocked: int
    "Random切片解锁"
    chapter8UnlockBegin: bool
    "第八章入场"
    chapter8UnlockSecondPhase: bool
    "第八章第二阶段"
    chapter8Passed: bool
    "第八章通过"
    chapter8SongUnlocked: int
    "第八章各曲目解锁"


class GameUser(BaseModel):
    """用户配置"""

    name: str
    "用户名"
    version: int
    "版本"
    showPlayerId: bool
    "是否展示Id"
    selfIntro: str
    "简介"
    avatar: str
    "头像"
    background: str
    "背景"


class SaveInfo(BaseModel):
    """存档元数据"""

    createdAt: datetime
    "账户创建时间 2022-09-03T10:21:48.613Z"
    gameFile: GameFile
    modifiedAt: ModifiedAt
    "存档上传时间"
    objectId: str
    "用户id {24} 与 gameFile 中的不同"
    summary: Summary
    updatedAt: datetime
    "存档上传时间 2023 Oct.06 11:46:33"
    user: UserInfo
    PlayerId: str
    "用户名"

    @field_validator("createdAt")
    @field_validator("updatedAt")
    @classmethod
    def parse_iso(cls, value: Any) -> datetime:
        """自动将字符串转换为datetime对象"""
        return Date(value)


class SaveModel(BaseModel):
    """完整存档数据模型"""

    sessionToken: str
    "会话令牌"
    modifiedAt: datetime
    "存档上传时间 ISO 2023-10-06T03:46:33.000Z"
    saveInfo: SaveInfo
    "存档元数据"
    saveUrl: str
    "存档url"
    Recordver: int
    "官方存档版本号"
    gameProgress: GameProgress
    "游戏进度"
    gameuser: GameUser | None = None
    "用户配置"
    gameRecord: dict[idString, list[LevelRecordInfoModel | None]] | None = None
    "成绩记录"

    @field_validator("modifiedAt")
    @classmethod
    def parse_iso(cls, value: Any) -> datetime:
        """自动将字符串转换为datetime对象"""
        return Date(value)

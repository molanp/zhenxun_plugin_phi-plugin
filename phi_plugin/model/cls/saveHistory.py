from datetime import datetime

from pydantic import BaseModel

from .type import levelKind


class ChangeModel(BaseModel):
    """变更记录"""

    date: datetime
    """日期"""
    value: float
    """值"""


class ScoreEntry(BaseModel):
    """单个成绩记录"""

    score: float
    """分数"""
    count: float
    """次数"""
    date: datetime
    """日期"""
    flag: bool
    """标记状态"""


class saveHistoryModel(BaseModel):
    data: list[ChangeModel]
    """data货币变更记录"""
    rks: list[ChangeModel]
    """rks变更记录"""
    scoreHistory: dict[str, dict[levelKind, list[ScoreEntry]]]
    """历史成绩"""
    dan: list
    """民间考核"""
    version: float

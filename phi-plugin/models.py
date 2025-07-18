from datetime import datetime, timedelta
from typing import Any, ClassVar

from tortoise import fields

from zhenxun.services.db_context import Model

from .utils import Date


class SstkData(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    uid = fields.CharField(255, description="用户uid", unique=True)
    """用户uid"""
    sessionToken = fields.CharField(255, description="用户SessionToken")
    """用户sstk"""
    is_banned = fields.BooleanField(
        default=False,
        description="是否被封禁",
        help_text="True: 被封禁, False: 未被封禁",
    )
    """是否被封禁"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "phiPlugin_sstkData"
        table_description = "Phi sstk 数据表"
        indexes: ClassVar = [("uid", "sessionToken")]

    @classmethod
    async def _exists(cls, **filters) -> bool:
        """
        检测符合过滤条件的用户是否存在

        :param filters: 过滤条件（如uid='123', uin='456'）
        :return: 存在返回True，否则False
        """
        return await cls.filter(**filters).exists()

    @classmethod
    async def get_sstk(cls, uid: str) -> str | None:
        """
        获取用户数据

        :param uid: 用户uid
        :return: 用户sessionToken
        """
        data = await cls.get_or_none(uid=uid)
        return data.sessionToken if data else None

    @classmethod
    async def set_sstk(cls, uid: str, sessionToken: str) -> bool:
        """
        添加/设置用户数据

        :param uid: 用户uid
        :param sessionToken: 用户sessionToken
        """
        await cls.update_or_create(
            uid=uid,
            defaults={"sessionToken": sessionToken},
        )
        return True

    @classmethod
    async def delete_sstk(cls, uid: str) -> bool:
        """
        删除用户数据

        :param uid: 用户uid
        :return: 是否删除成功
        """
        deleted = await cls.filter(uid=uid).delete()
        return deleted > 0

    @classmethod
    async def ban_sstk(cls, uid: str) -> bool:
        """
        封禁用户数据

        :param uid: 用户uid
        :return: 是否封禁成功
        """
        updated = await cls.filter(uid=uid, is_banned=False).update(is_banned=True)
        return updated > 0

    @classmethod
    async def unban_sstk(cls, uid: str) -> bool:
        """
        解封用户数据

        :param uid: 用户uid
        :return: 是否解封成功
        """
        updated = await cls.filter(uid=uid, is_banned=True).update(is_banned=False)
        return updated > 0

    @classmethod
    async def is_ban_sessionToken(cls, sessionToken: str) -> bool:
        """
        检测 sessionToken 是否被封禁

        :param sessionToken: 用户sessionToken
        :return: 是否被封禁
        """
        data = await cls.get_or_none(sessionToken=sessionToken, is_banned=True)
        return bool(data)

    @classmethod
    async def get_ban_sstk(cls) -> list[str]:
        """
        获取所有被封禁的 sessionToken

        :return: 被封禁的 sessionToken 列表
        """
        data = await cls.filter(is_banned=True).values_list("sessionToken", flat=True)
        return list(data)  # type: ignore[return-value]


class RksRank(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增ID"""
    sessionToken = fields.CharField(255, description="用户SessionToken", unique=True)
    """关联用户的SessionToken"""
    rks = fields.FloatField(description="用户RKS分数")
    """用户的RKS数值"""
    created_at = fields.DatetimeField(auto_now_add=True)
    """记录创建时间"""
    updated_at = fields.DatetimeField(auto_now=True)
    """最后更新时间"""

    class Meta:  # type: ignore
        table = "phiPlugin_rksRank"
        table_description = "Phi RKS数据表"
        indexes: ClassVar = [
            ("sessionToken", "rks"),
        ]

    @classmethod
    async def get_user_rks(cls, sessionToken: str) -> float | None:
        """
        获取用户RKS

        :param sessionToken: 用户SessionToken
        :return: 用户RKS
        """
        data = await cls.get_or_none(sessionToken=sessionToken)
        return data.rks if data else None

    @classmethod
    async def set_user_rks(cls, sessionToken: str, rks: float) -> bool:
        """
        添加/设置用户RKS

        :param sessionToken: 用户SessionToken
        :param rks: 用户RKS
        """
        await cls.update_or_create(
            sessionToken=sessionToken,
            defaults={"rks": rks},
        )
        return True

    @classmethod
    async def delete_user_rks(cls, sessionToken: str) -> bool:
        """
        删除用户RKS

        :param sessionToken: 用户SessionToken
        :return: 是否删除成功
        """
        deleted = await cls.filter(sessionToken=sessionToken).delete()
        return deleted > 0

    @classmethod
    async def getAllRank(cls) -> list[dict]:
        """
        获取RKS排名

        :param limit: 排行榜限制数量
        :return: 排行榜数据
        """
        return await cls.filter().order_by("-rks").values()

    @classmethod
    async def getUserRank(cls, sessionToken: str) -> int:
        """
        获取用户排名（基于RKS分数降序）
        :param sessionToken: 用户SessionToken
        :return: 用户排名（从1开始），不存在或分数为0返回-1
        """
        target = await cls.get_or_none(sessionToken=sessionToken)
        if not target or target.rks <= 0:
            return -1

        higher_count = await cls.filter(rks__gt=target.rks).count()
        return higher_count + 1
    
    @classmethod
    async def getRankByRks(cls, rks: float) -> int:
        """
        获取用户rks的排名（基于RKS分数降序）

        :param rks: RKS
        :return: 用户排名（从1开始），不存在或分数为0返回None
        """
        higher_count = await cls.filter(rks__gt=rks).count()
        return higher_count + 1

    @classmethod
    async def getRankUser(cls, min_rank: int, max_rank: int) -> list[dict]:
        """
        获取指定排名范围的用户数据（基于RKS分数降序）

        :param min_rank: 起始排名（0起始）
        :param max_rank: 结束排名（不包含）
        :return: 包含用户数据的字典列表
        """
        # 按 RKS 降序排列，从 min_rank 开始取 (max_rank - min_rank) 条记录
        query = (
            cls.filter().order_by("-rks").offset(min_rank).limit(max_rank - min_rank)
        )
        return await query.values()


class userApiId(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    uid = fields.CharField(255, description="用户uid", unique=True)
    """用户uid"""
    apiId = fields.CharField(255, description="用户的apiIId")
    """用户的apiId"""

    class Meta:  # type: ignore
        table = "phiPlugin_userApiId"
        table_description = "Phi 用户apiId"
        indexes: ClassVar = [
            ("uid", "apiId"),
        ]

    @classmethod
    async def set_user_apiId(cls, user_id, apiId) -> bool:
        await cls.update_or_create(
            uid=user_id,
            defaults={"apiId": apiId},
        )
        return True

    @classmethod
    async def get_user_apiId(cls, user_id) -> str | None:
        data = await cls.get_or_none(uid=user_id)
        return data.apiId if data else None

    @classmethod
    async def del_user_apiId(cls, user_id) -> bool:
        """删除 user_id 号对应的 apiId"""
        deleted = await cls.filter(uid=user_id).delete()
        return deleted > 0


class banGroup(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    group_id = fields.CharField(255, description="群聊id")
    """群聊id"""
    func = fields.CharField(255, description="功能名称")
    """功能名称"""

    class Meta:  # type: ignore
        table = "phiPlugin_banGroup"
        table_description = "Phi 群组封禁功能表"

    @classmethod
    async def getStatus(cls, group_id: str, func: str) -> bool:
        return await cls.filter(group_id=group_id, func=func).exists()

    @classmethod
    async def add(cls, group_id: str, func: str) -> bool:
        if await cls.getStatus(group_id, func):
            return False
        await cls.create(group_id=group_id, func=func)
        return True

    @classmethod
    async def remove(cls, group_id: str, func: str) -> bool:
        deleted = await cls.filter(group_id=group_id, func=func).delete()
        return deleted > 0


def calculate_jrrp_expiration():
    """计算过期时间"""
    now = datetime.now()
    today_8am = now.replace(hour=8, minute=0, second=0, microsecond=0)

    return today_8am + timedelta(days=1)


def calculate_qrcode_expiration(seconds: int):
    """计算二维码过期时间"""
    now = datetime.now()

    return now + timedelta(seconds=seconds)


def is_expired(expiration_time: datetime) -> bool:
    """
    判断指定时间是否已过期
    """
    return Date(datetime.now()) > Date(expiration_time)


def remaining_expiration(expiration_time: datetime) -> int:
    """计算剩余过期时间（秒）"""
    now = datetime.now()
    delta = expiration_time - now
    return max(int(delta.total_seconds()), 0)


class jrrpModel(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    uid = fields.CharField(255, description="用户id", unique=True)
    """用户id"""
    content = fields.JSONField(description="今日人品内容", field_type=list[Any])
    """今日人品内容"""
    expiration_time = fields.DatetimeField(
        description="记录过期时间", default=calculate_jrrp_expiration
    )
    """过期时间"""

    class Meta:  # type: ignore
        table = "phiPlugin_jrrp"
        table_description = "Phi 今日人品记录表"

    @classmethod
    async def get_jrrp(cls, user_id: str) -> list:
        """
        获取今日人品

        :param user_id: 用户id
        """
        jrrp = await cls.get_or_none(uid=user_id)
        if jrrp is None:
            return []
        if is_expired(jrrp.expiration_time):
            await cls.del_jrrp(user_id)
            return []
        assert isinstance(jrrp.content, list)
        return jrrp.content

    @classmethod
    async def set_jrrp(cls, user_id: str, content: list) -> bool:
        await cls.update_or_create(
            uid=user_id,
            defaults={"content": content},
        )
        return True

    @classmethod
    async def del_jrrp(cls, user_id: str) -> bool:
        deleted = await cls.filter(uid=user_id).delete()
        return deleted > 0


class qrCode(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    uid = fields.CharField(255, description="用户id", unique=True)
    """用户id"""
    qrcode = fields.TextField(description="登录二维码链接")
    """登录二维码链接"""
    data = fields.JSONField(description="登录二维码响应数据")
    """登录二维码响应数据"""
    expiration_time = fields.DatetimeField(description="记录过期时间")
    """过期时间"""

    class Meta:  # type: ignore
        table = "phiPlugin_qrcode"
        table_description = "Phi 登陆二维码信息"

    @classmethod
    async def get_qrcode(cls, user_id: str) -> tuple[str, int, dict]:
        """
        获取二维码

        :param user_id: 用户id
        :return: [二维码链接, 剩余过期时间, 原始响应数据]
        """
        qrcode = await cls.get_or_none(uid=user_id)
        if qrcode is None:
            return "", 0, {}
        if is_expired(qrcode.expiration_time):
            await cls.del_qecode(user_id)
            return "", 0, {}
        assert isinstance(qrcode.data, dict)
        return qrcode.qrcode, remaining_expiration(qrcode.expiration_time), qrcode.data

    @classmethod
    async def set_qrcode(
        cls, user_id: str, qrcode: str, data: dict, expiration_second: int
    ) -> bool:
        """
        :param user_id: 用户ID
        :param qrcode: 二维码链接
        :param expiration_second: 过期时间（秒）
        """
        await cls.update_or_create(
            uid=user_id,
            defaults={
                "qrcode": qrcode,
                "data": data,
                "expiration_time": calculate_qrcode_expiration(expiration_second),
            },
        )
        return True

    @classmethod
    async def del_qecode(cls, user_id: str) -> bool:
        deleted = await cls.filter(uid=user_id).delete()
        return deleted > 0

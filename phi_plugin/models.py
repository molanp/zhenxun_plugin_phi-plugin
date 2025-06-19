from datetime import datetime, timedelta
from typing import Any, ClassVar, Literal

from tortoise import fields

from zhenxun.services.db_context import Model


def calculate_jrrp_expiration():
    now = datetime.now()
    today_8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
    return today_8am + timedelta(days=1)


def is_expired(expiration_time: datetime) -> bool:
    return datetime.now() > expiration_time


class phigrosUserToken(Model):
    """用户 SessionToken 存储"""

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    uid = fields.CharField(255, description="用户ID", unique=True)
    token = fields.CharField(255, description="用户SessionToken")

    class Meta:  # type: ignore
        table = "phigrosUserToken"
        table_description = "Phi 用户Token数据表"
        indexes: ClassVar = [("uid", "token")]

    @classmethod
    async def _exists(cls, **filters) -> bool:
        return await cls.filter(**filters).exists()

    @classmethod
    async def get_sstk(cls, uid: str) -> str | None:
        data = await cls.get_or_none(uid=uid)
        return data.token if data else None

    @classmethod
    async def set_sstk(cls, uid: str, token: str) -> bool:
        await cls.update_or_create(
            uid=uid,
            defaults={"token": token},
        )
        return True

    @classmethod
    async def delete_sstk(cls, uid: str) -> bool:
        deleted = await cls.filter(uid=uid).delete()
        return deleted > 0


class phigrosBanSessionToken(Model):
    """用户BanSessionToken 存储"""

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    sessionToken = fields.CharField(255, description="SessionToken", unique=True)

    class Meta:  # type: ignore
        table = "phigrosBanSessionToken"
        table_description = "Phi 用户Token封禁表"
        indexes: ClassVar = [("sessionToken",)]

    @classmethod
    async def _exists(cls, **filters) -> bool:
        return await cls.filter(**filters).exists()

    @classmethod
    async def ban_session_token(cls, session_token: str) -> bool:
        await cls.update_or_create(
            sessionToken=session_token,
            defaults={"sessionToken": session_token},
        )
        return True

    @classmethod
    async def unban_session_token(cls, session_token: str) -> bool:
        deleted = await cls.filter(sessionToken=session_token).delete()
        return deleted > 0

    @classmethod
    async def get_banned_session_tokens(cls) -> list[str]:
        return [token.sessionToken for token in await cls.all()]

    @classmethod
    async def is_banned(cls, session_token: str) -> bool:
        return await cls._exists(sessionToken=session_token)


class phigrosUserRks(Model):
    """用户RKS排名"""

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    token = fields.CharField(255, description="用户SessionToken", unique=True)
    rks = fields.FloatField(description="用户RKS分数")
    updated_at = fields.DatetimeField(
        auto_now=True, timezone=False, description="最后更新时间"
    )

    class Meta:  # type: ignore
        table = "phigrosUserRks"
        table_description = "Phi RKS数据表"
        indexes: ClassVar = [("token", "rks")]

    @classmethod
    async def get_user_rks(cls, session_token: str) -> float | None:
        data = await cls.get_or_none(token=session_token)
        return data.rks if data else None

    @classmethod
    async def set_user_rks(cls, session_token: str, rks: float) -> bool:
        await cls.update_or_create(
            token=session_token,
            defaults={"rks": rks},
        )
        return True

    @classmethod
    async def delete_user_rks(cls, session_token: str) -> bool:
        deleted = await cls.filter(token=session_token).delete()
        return deleted > 0

    @classmethod
    async def getAllRank(cls) -> list[dict[str, Any]]:
        """
        获取RKS排名

        :param limit: 排行榜限制数量
        :return: 排行榜数据
        """
        return await cls.filter().order_by("-rks").values()

    @classmethod
    async def getUserRank(cls, session_token: str) -> int | None:
        """
        获取用户排名

        :param sessionToken: 用户SessionToken
        :return: 用户排名
        """
        data = await cls.get_or_none(token=session_token)
        return data.id if data else None

    @classmethod
    async def getRankUsers(cls, min_rank: int, max_rank: int) -> list[dict[str, Any]]:
        """
        获取指定排名范围的用户数据（基于RKS分数降序）

        :param min_rank: 起始排名（0起始）
        :param max_rank: 结束排名（不包含）
        :return: 包含用户数据的字典列表
        """
        query = (
            cls.filter().order_by("-rks").offset(min_rank).limit(max_rank - min_rank)
        )
        return await query.values()


class phigrosBanGroup(Model):
    """群组功能禁用设置"""

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    group_id = fields.CharField(255, description="群组ID", unique=True)

    help = fields.BooleanField(default=False, description="帮助功能")
    bind = fields.BooleanField(default=False, description="绑定功能")
    b19 = fields.BooleanField(default=False, description="B19功能")
    wb19 = fields.BooleanField(default=False, description="Web B19功能")
    song = fields.BooleanField(default=False, description="曲目查询功能")
    ranklist = fields.BooleanField(default=False, description="排行榜功能")
    fnc = fields.BooleanField(default=False, description="FNC功能")
    tipgame = fields.BooleanField(default=False, description="提示猜歌功能")
    guessgame = fields.BooleanField(default=False, description="猜曲绘功能")
    ltrgame = fields.BooleanField(default=False, description="开字母功能")
    sign = fields.BooleanField(default=False, description="签到功能")
    setting = fields.BooleanField(default=False, description="设置功能")
    dan = fields.BooleanField(default=False, description="段位认证功能")

    class Meta:  # type: ignore
        table = "phigrosBanGroup"
        table_description = "Phi 群组封禁功能表"

    @classmethod
    async def getStatus(
        cls,
        group_id: str,
        func: Literal[
            "help",
            "bind",
            "b19",
            "wb19",
            "song",
            "ranklist",
            "fnc",
            "tipgame",
            "guessgame",
            "ltrgame",
            "sign",
            "setting",
            "dan",
        ],
    ) -> bool:
        record = await cls.get_or_none(group_id=group_id)
        return getattr(record, func, False) if record else False

    @classmethod
    async def add(cls, group_id: str, func: str) -> bool:
        if not hasattr(cls, func):
            return False

        record, created = await cls.get_or_create(
            group_id=group_id, defaults={func: True}
        )

        if not created:
            if getattr(record, func, False):
                return False
            await cls.filter(group_id=group_id).update(**{func: True})

        return True

    @classmethod
    async def remove(cls, group_id: str, func: str) -> bool:
        if not hasattr(cls, func):
            return False

        record = await cls.get_or_none(group_id=group_id)
        if not record:
            return False

        if not getattr(record, func, False):
            return False

        await cls.filter(group_id=group_id).update(**{func: False})
        return True


class phigrosJrrp(Model):
    """今日人品数据 (对应 phigrosJrrp 表)"""

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    uid = fields.CharField(255, description="用户ID", unique=True)
    value = fields.JSONField(description="人品值序列化数据")
    expiration_time = fields.DatetimeField(
        description="过期时间", default=calculate_jrrp_expiration, timezone=False
    )

    class Meta:  # type: ignore
        table = "phigrosJrrp"
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
        assert isinstance(jrrp.value, list)
        return jrrp.value

    @classmethod
    async def set_jrrp(cls, uid: str, content: list[Any]) -> bool:
        value = str(content[0]) if content else "0"
        await cls.update_or_create(
            uid=uid,
            defaults={"value": value},
        )
        return True

    @classmethod
    async def del_jrrp(cls, uid: str) -> bool:
        deleted = await cls.filter(uid=uid).delete()
        return deleted > 0

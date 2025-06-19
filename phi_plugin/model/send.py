from nonebot_plugin_alconna import AlconnaMatcher, UniMessage
from nonebot_plugin_alconna.uniseg.message import Receipt
from nonebot_plugin_uninfo import Uninfo

from zhenxun.utils.rules import ensure_group

from ..components.i18n import i18nList
from .cls.Save import SaveModel
from .cls.type import allFnc
from .getBanGroup import getBanGroup
from .getInfo import getInfo
from .getSave import getSave


class send:
    @staticmethod
    async def send_with_At(
        matcher: AlconnaMatcher,
        session: Uninfo,
        msg: UniMessage,
        reply_to: bool = True,
        recallMsg: int = 0,
    ) -> Receipt:
        """
         私聊省略@

        :param matcher: Alconna Matcher
        :param session: Session
        :param msg: 消息内容
        :param quote: 是否引用回复
        :param recallMsg: 撤回时间，0为不撤回
        """
        at_sender = ensure_group(session)
        receipt = await matcher.send(msg, at_sender=at_sender, reply_to=reply_to)
        assert isinstance(receipt, Receipt)
        if recallMsg > 0:
            await receipt.recall(delay=recallMsg)
        return receipt

    @staticmethod
    async def getsave_result(
        matcher: AlconnaMatcher, session: Uninfo, ver: float | None = None
    ) -> SaveModel | None:
        """
        检查存档部分
        - v1.0,取消对当次更新内容的存储，取消对task的记录，更正scoreHistory
        - v1.1,更正scoreHistory
        - v1.2,由于曲名错误，删除所有记录，曲名使用id记录

        :param ver: 存档版本

        :return: Save
        """
        sessionToken = await getSave.get_user_token(session.user.id)
        if not sessionToken:
            await send.send_with_At(
                matcher,
                session,
                UniMessage(
                    i18nList.common.haveToBind.format(
                        prefix=getInfo.getCmdPrefix(session)
                    )
                ),
            )
            return None
        user_save = await getSave.getSave(session.user.id)
        if not user_save or (
            ver and (not user_save.Recordver or user_save.Recordver < ver)
        ):
            await send.send_with_At(
                matcher,
                session,
                UniMessage(
                    i18nList.common.haveToUpdate.format(
                        prefix=getInfo.getCmdPrefix(session)
                    )
                ),
            )
            return None
        return user_save

    @staticmethod
    async def isBan(matcher: AlconnaMatcher, session: Uninfo, fnc: allFnc) -> bool:
        """
        该功能是否被ban

        :param fnc: 指令名称
        """
        if ensure_group(session) and await getBanGroup.get(session.scene.id, fnc):
            await send.send_with_At(
                matcher, session, UniMessage(i18nList.common.beGroupBan)
            )
            return True
        return False

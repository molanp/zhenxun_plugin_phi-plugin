from nonebot_plugin_uninfo import Uninfo

from zhenxun.services.log import logger

from ..config import PluginConfig
from ..models import banGroup
from .getSave import getSave
from .makeRequest import makeRequest
from .makeRequestFnc import makeRequestFnc
from .send import send


class getBanGroup:
    @staticmethod
    async def redis(group_id: str, func: str) -> bool:
        return await banGroup.getStatus(group_id, func)

    @staticmethod
    async def get(matcher, session: Uninfo, func: str) -> bool:
        group_id = session.scene.id
        if not group_id:
            return False
        sessionToken = await getSave.get_user_token(session.user.id)
        if PluginConfig.get("openPhiPluginApi"):
            result = False
            try:
                result = await makeRequest.getUserBan(
                    makeRequestFnc.makePlatform(session)
                )
                if result:
                    await send.sendWithAt(
                        matcher, "当前账户被加入黑名单，详情请联系管理员(1)。"
                    )
                    if sessionToken:
                        await getSave.banSessionToken(sessionToken)
                    return True
            except Exception as err:
                logger.warning("API获取用户禁用状态失败", "phi-plugin", e=err)
        if sessionToken and await getSave.isBanSessionToken(sessionToken):
            await send.sendWithAt(
                matcher, "当前账户被加入黑名单，详情请联系管理员(2)。"
            )
            return True
        match func:
            case "help" | "tkhelp":
                return await getBanGroup.redis(group_id, "help")
            case "bind" | "unbind":
                return await getBanGroup.redis(group_id, "bind")
            case (
                "b19"
                | "p30"
                | "lmtAcc"
                | "arcgrosB19"
                | "update"
                | "info"
                | "list"
                | "singlescore"
                | "lvscore"
                | "chap"
                | "suggest"
            ):
                return await getBanGroup.redis(group_id, "b19")
            case "bestn" | "data":
                return await getBanGroup.redis(group_id, "wb19")
            case (
                "song"
                | "ill"
                | "chart"
                | "addtag"
                | "retag"
                | "search"
                | "alias"
                | "randmic"
                | "randClg"
                | "table"
                | "comment"
                | "recallComment"
            ):
                return await getBanGroup.redis(group_id, "song")
            case "rankList" | "godList":
                return await getBanGroup.redis(group_id, "ranklist")
            case "comrks" | "tips" | "newSong":
                return await getBanGroup.redis(group_id, "fnc")
            case "tipgame":
                return await getBanGroup.redis(group_id, "tipgame")
            case "guessgame":
                return await getBanGroup.redis(group_id, "guessgame")
            case "ltrgame":
                return await getBanGroup.redis(group_id, "ltrgame")
            case "sign" | "send" | "tasks" | "retask" | "jrrp":
                return await getBanGroup.redis(group_id, "sign")
            case "theme":
                return await getBanGroup.redis(group_id, "setting")
            case "dan" | "danupdate":
                return await getBanGroup.redis(group_id, "dan")
            case (
                "auth"
                | "clearApiData"
                | "updateHistory"
                | "setApiToken"
                | "tokenList"
                | "tokenManage"
            ):
                return await getBanGroup.redis(group_id, "apiSetting")
            case _:
                return False

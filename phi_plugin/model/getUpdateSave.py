from typing import Literal

from nonebot import require

from ..config import PluginConfig
from ..lib.PhigrosUser import PhigrosUser
from ..utils import Event2session, to_dict
from .cls.Save import Save
from .getInfo import getInfo
from .getNotes import getNotes
from .getSave import getSave
from .getSaveFromApi import getSaveFromApi
from .makeRequest import makeRequest
from .makeRequestFnc import makeRequestFnc
from .send import send

require("nonebot_plugin_uninfo")
from nonebot.adapters import Event
from nonebot_plugin_uninfo import Uninfo

from zhenxun.services.log import logger
from zhenxun.utils.platform import PlatformUtils


class getUpdateSave:
    @classmethod
    async def getNewSaveFromApi(cls, session: Uninfo, token: str | None = None) -> dict:
        old = await getSaveFromApi.getSave(session.user.id)
        newSaveInfo = await makeRequest.getCloudSaveInfo(
            **{"token": token, **makeRequestFnc.makePlatform(session)}
        )
        if newSaveInfo["modifiedAt"]["iso"] == getattr(
            getattr(getattr(old, "saveInfo", None), "modifiedAt", None),
            "iso",
            None,
        ):
            return {"save": old, "added_rks_notes": [0, 0]}
        newSave = await makeRequest.getCloudSaves(
            **{"token": token, **makeRequestFnc.makePlatform(session)}
        )
        await getSaveFromApi.putSave(session.user.id, newSave)
        result = await Save().constructor(newSave)
        await result.init()
        await getSaveFromApi.putSave(session.user.id, to_dict(result))
        if token:
            await getSave.add_user_token(session.user.id, token)
        added_rks_notes = await cls.buildingRecord(old, result, session)
        return {"save": result, "added_rks_notes": added_rks_notes}

    @classmethod
    async def getNewSaveFromLocal(cls, e: Event, token: str | None = None) -> dict:
        session = await Event2session(e)
        old = await getSave.getSave(session.user.id)
        token = token or old.session if old else None
        try:
            User = PhigrosUser(token)
            save_info = await User.getSaveInfo()
            if (
                old
                and old.saveInfo["modifiedAt"]["iso"] == save_info["modifiedAt"]["iso"]
            ):
                return {"save": old, "added_rks_notes": [0, 0]}
            await User.buildRecord()
        except Exception as err:
            if not PlatformUtils.is_qbot(session):
                await send.send_with_At(e, f"更新失败！QAQ\n{err}")
            else:
                await send.send_with_At(e, "更新失败！QAQ\n请稍后重试")
            logger.error("信息更新失败", "phi-plugin", e=err)
            raise err
        try:
            await getSave.putSave(session.user.id, User)
        except Exception as err:
            await send.send_with_At(e, f"保存存档失败!\n{err}")
            logger.error("保存存档失败", "phi-plugin", e=err)
            raise err
        now = await Save().constructor(
            User
        )  # TODO:在py里似乎需要转字典传入,使用model_dump?

        if old and (old.session and old.session != User.session):
            await send.send_with_At(
                e,
                "检测到新的sessionToken，将自动更换绑定。"
                "如果需要删除统计记录请"
                f"⌈{PluginConfig.get('cmdhead')} unbind⌋ 进行解绑哦！",
            )
            await getSave.add_user_token(session.user.id, User.session)
            old = await getSave.getSave(session.user.id)
        # await now.init()
        history = await getSave.getHistory(session.user.id)
        assert history is not None
        history.update(now)
        await getSave.putHistory(session.user.id, to_dict(history))
        added_rks_notes = await cls.buildingRecord(old, now, session)
        return {"save": now, "added_rks_notes": added_rks_notes}

    @classmethod
    async def buildingRecord(
        cls, old: Save | None, now: Save, session: Uninfo
    ) -> list[float] | Literal[False]:
        """
        更新存档

        :return: [ks变化值，note变化值]，失败返回 false
        """
        notesData = await getNotes.getNotesData(session.user.id)
        # 修正(我没有旧用户，不需要了)
        # if notesData.get("update") or notesData.get("task_update"):
        #     notesData.pop("update", None)
        #     notesData.pop("task_update", None)
        # note数量变化
        add_money = 0
        task = notesData.get("plugin_data", {}).get("task")
        add_money = 0

        if task:
            for song_id, record_levels in now.gameRecord.items():
                for i, task_info in enumerate(task):
                    if not task_info:  # 跳过空任务
                        continue
                    if task_info.get("finished"):  # 已完成的任务跳过
                        continue

                    song = task_info.get("song")
                    if song != getInfo.idgetsong(song_id):
                        continue

                    level = task_info["request"].get("rank", None)
                    if level not in ["pst", "prs", "ftr", "byd"]:  # 根据实际等级设定
                        continue

                    level_index = {"pst": 0, "prs": 1, "ftr": 2, "byd": 3}.get(level, 0)
                    current_record = (
                        record_levels[level_index]
                        if isinstance(record_levels, list)
                        and len(record_levels) > level_index
                        else None
                    )

                    if not current_record:
                        continue

                    request_type = task_info["request"].get("type")
                    request_value = task_info["request"].get("value", 0)

                    if (
                        request_type == "acc" and current_record.acc >= request_value
                    ) or (
                        request_type != "acc"
                        and request_type == "score"
                        and current_record.score >= request_value
                    ):
                        task_info["finished"] = True
                        reward = task_info.get("reward", 0)
                        add_money += reward
                        notesData["plugin_data"]["money"] += reward
        await getNotes.putNotesData(session.user.id, notesData)

        # rks变化
        add_rks = (
            now.saveInfo["summary"]["rankingScore"]
            - old.saveInfo["summary"]["rankingScore"]
            if old
            else 0
        )
        return [add_rks, add_money]

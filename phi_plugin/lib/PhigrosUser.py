import io
import re
from typing import Any, cast
from urllib.parse import urlparse
import zipfile

from nonebot.utils import run_sync

from zhenxun.services.log import logger

from ..model.cls.Save import SaveInfo
from .ByteReader import ByteReader
from .GameProgress import GameProgress
from .GameRecord import GameRecord
from .GameSettings import GameSettings
from .GameUser import GameUser
from .http import Builder, HttpClient
from .SaveManager import SaveManager


class readZip:
    def __init__(self, b: bytes):
        self.data = io.BytesIO(b)

    @run_sync
    def file(self, filename: str):
        with zipfile.ZipFile(self.data) as zf:
            return zf.read(filename)

class PhigrosUser:
    """Phigros 用户类"""

    session: str
    saveInfo: list[SaveInfo]
    gameRecord: dict[str, list[Any]]

    def __init__(self, session: str) -> None:
        """
        初始化

        :param session: 会话令牌
        """
        self.session = ""
        self.saveInfo = []
        self.gameRecord = {}
        if not re.match(r"[a-z0-9A-Z]{25}", session):
            logger.error("SessionToken格式错误")
            raise ValueError("SessionToken格式错误")
        self.session = session
        self.http = HttpClient()

    def chooseSave(self, choose: int) -> bool:
        """
        选择存档

        :param choose: 存档索引
        :return: 是否成功
        """
        if isinstance(self.saveInfo, list) and 0 <= choose < len(self.saveInfo):
            self.saveInfo = [self.saveInfo[choose]]
            return True
        return False

    async def getSaveInfo(self) -> list[SaveInfo]:
        """
        获取存档信息

        :return: 存档信息
        """
        raw_save_info = await SaveManager.saveCheck(self.session)
        if (
            isinstance(raw_save_info, list)
            and raw_save_info
            and isinstance(raw_save_info[0], dict)
        ):
            self.saveInfo = [cast(SaveInfo, raw_save_info[0])]
        else:
            logger.error("错误的存档")
            logger.error(str(raw_save_info))
            raise ValueError("未找到存档QAQ！")
        try:
            if (
                isinstance(self.saveInfo, list)
                and self.saveInfo
                and isinstance(self.saveInfo[0], dict)
                and "gameFile" in self.saveInfo[0]
                and isinstance(self.saveInfo[0]["gameFile"], dict)
                and "url" in self.saveInfo[0]["gameFile"]
            ):
                self.saveUrl = urlparse(str(self.saveInfo[0]["gameFile"]["url"]))
            else:
                raise ValueError("存档信息格式错误")
        except Exception as e:
            logger.error("设置saveUrl失败", e=e)
            raise ValueError("设置saveUrl失败") from e
        return self.saveInfo

    async def buildRecord(self) -> bool:
        """
        构建记录

        :return: 是否成功
        """
        if not hasattr(self, "saveUrl"):
            await self.getSaveInfo()

        if (
            isinstance(self.saveInfo, list)
            and self.saveInfo
            and isinstance(self.saveInfo[0], dict)
            and "summary" in self.saveInfo[0]
            and isinstance(self.saveInfo[0]["summary"], dict)
            and self.saveInfo[0]["summary"].get("saveVersion") == "1"
        ):
            raise ValueError("存档版本过低，请更新Phigros！")

        if getattr(self, "saveUrl", None):
            # 从saveurl获取存档zip
            try:
                response = await self.http.send(
                    await Builder(self.saveUrl.geturl()).GET().build()
                )
                if not response:
                    raise ValueError("获取存档失败")
                savezip = readZip(response.content)

                # 插件存档版本
                self.Recordver = 1.0

                # 获取 gameProgress
                file = ByteReader(await savezip.file("gameProgress"))
                file.getByte()
                self.gameProgress = GameProgress(
                    await SaveManager.decrypt(file.getAllByte())
                )

                # 获取 gameuser
                file = ByteReader(await savezip.file("user"))
                file.getByte()
                self.gameuser = GameUser(await SaveManager.decrypt(file.getAllByte()))

                # 获取 gamesetting
                file = ByteReader(await savezip.file("settings"))
                file.getByte()
                self.gamesettings = GameSettings(
                    await SaveManager.decrypt(file.getAllByte())
                )

                # 获取gameRecord
                file = ByteReader(await savezip.file("gameRecord"))
                if file.getByte() != GameRecord.version:
                    self.gameRecord = {}
                    logger.info("版本号已更新，请更新PhigrosLibrary。")
                    raise ValueError("版本号已更新")

                record = GameRecord(await SaveManager.decrypt(file.getAllByte()))
                await record.init([])
                self.gameRecord = record.Record

            except Exception as e:
                logger.error("解压zip文件失败", e=e)
                raise ValueError("解压zip文件失败") from e

        else:
            logger.info("获取存档链接失败！")
            raise ValueError("获取存档链接失败！")

        return False

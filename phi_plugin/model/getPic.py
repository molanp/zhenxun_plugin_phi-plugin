from ..components.Logger import logger
from ..components.pluginPath import imgPath
from .cls.type import idString
from .getInfo import getInfo
from .render import render


class pic:
    @staticmethod
    async def GetSongsInfoAtlas(id: idString, data: dict | None = None):
        """
        获取歌曲图鉴，曲名为原名

        :param id: 曲名
        """
        data = data or getInfo.info(id)
        if data:
            if not data.illustration:  # TODO: 类型修正
                data.illustration = getInfo.getill(id)
            return await render("song", data)
        else:
            return f"未找到{id}的相关曲目信息!QAQ"

    @staticmethod
    async def GetSongsIllAtlas(id: idString, data: dict):
        """
        获取曲绘图鉴

        :param id: 原曲名称
        """
        if data:
            return await render("ill", data)
        else:
            return await render(
                "ill",
                {
                    "illustration": getInfo.getill(id),
                    "illustrator": getInfo.info(id).illustrator,
                },
            )

    @staticmethod
    def getimg(img: str, style: str = "png"):
        """
        获取本地图片，文件格式默认png

        :param img: 文件名
        :param style: 文件格式，默认为png
        """
        path = imgPath / f"{img}.{style}"
        if path.exists():
            return path
        logger.info(f"未找到 {img}.{style}")
        return None

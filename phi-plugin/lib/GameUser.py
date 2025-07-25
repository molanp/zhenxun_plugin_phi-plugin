from .ByteReader import ByteReader
from .Util import Util


class GameUser:
    """游戏用户"""

    def __init__(self, data: bytes | str) -> None:
        """
        初始化

        :param data: 二进制数据
        """
        reader = ByteReader(data)
        self.name: str = "user"
        self.version: int = 1
        self.showPlayerId = Util.getBit(reader.getByte(), 0)
        self.selfIntro = reader.getString()
        self.avatar = reader.getString()
        self.background = reader.getString()

from datetime import datetime
import math
import random
import re

from nonebot.adapters import Bot
from nonebot_plugin_alconna import AlconnaMatcher, File
from nonebot_plugin_uninfo import Uninfo

from zhenxun.models.level_user import LevelUser
from zhenxun.utils.rules import ensure_group
from zhenxun.utils.withdraw_manage import WithdrawManager

from ..components.Logger import logger
from ..utils import Date
from .constNum import MAX_DIFFICULTY


class fCompute:
    @staticmethod
    def rks(acc: float, difficulty: float):
        """计算等效rks"""
        if acc == 100:
            # 满分原曲定数即为有效rks
            return difficulty
        elif acc < 70:
            # 无效acc
            return 0
        else:
            # 非满分计算公式 [(((acc - 55) / 45) ^ 2) * 原曲定数]
            return difficulty * (((acc - 55) / 45) ** 2)

    @staticmethod
    def suggest(rks: float, difficulty: float, count: int | None = None) -> str | float:
        """
        计算所需acc

        :param rks: 目标rks
        :param difficulty: 定数
        :param count: 保留位数
        """
        ans = 45 * math.sqrt(rks / difficulty) + 55
        if ans >= 100:
            return "无法推分"
        elif count is not None:
            return f"{ans:.{count}f}%"
        else:
            return ans

    @staticmethod
    async def sendFile(matcher: AlconnaMatcher, file: bytes, title: str = "backup.zip"):
        """发送文件"""
        try:
            await matcher.send(File(raw=file, name=title))
        except Exception as e:
            logger.error("文件上传错误", "phi-plugin", e=e)
            await matcher.send(f"文件上传错误.{type(e)}: {e}")

    @staticmethod
    async def getBackground(save_background: str) -> str | None:
        """获取角色介绍背景曲绘"""
        try:
            match save_background:
                case "Another Me ":
                    save_background = "Another Me (KALPA)"
                case "Another Me":
                    save_background = "Another Me (Rising Sun Traxx)"
                case "Re_Nascence (Psystyle Ver.) ":
                    save_background = "Re_Nascence (Psystyle Ver.)"
                case "Energy Synergy Matrix":
                    save_background = "ENERGY SYNERGY MATRIX"
                case "Le temps perdu-":
                    save_background = "Le temps perdu"
            return save_background
        except Exception as e:
            logger.error("获取背景曲绘错误", "phi-plugin", e=e)
            return None

    @staticmethod
    def ped(num: float, cover: int) -> str:
        """
        为数字添加前导零

        :param num: 原数字
        :param cover: 总位数
        """
        return str(int(num)).zfill(cover)

    @staticmethod
    def std_score(score: float) -> str:
        """
        标准化分数

        :param score: 分数
        :return: 标准化的分数 0'000'000
        """
        s1 = math.floor(score / 1e6)
        s2 = math.floor(score / 1e3) % 1e3
        s3 = score % 1e3
        return f"{s1}'{fCompute.ped(s2, 3)}'{fCompute.ped(s3, 3)}"

    @staticmethod
    def randBetween(min: int, max: int) -> int:
        """随机数，包含上下界"""
        return random.randint(min, max)

    @staticmethod
    def randArray(arr: list) -> list:
        """随机打乱数组"""
        return random.sample(arr, len(arr))

    @staticmethod
    def formatDate(date: datetime | str) -> str:
        """
        转换时间格式

        :return: 2020/10/8 10:08:08
        """
        date = Date(date)
        return date.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def convertRichText(richText: str, onlyText: bool = False) -> str:
        """
        转换unity富文本

        :param richText: richText
        :param onlyText: 是否只返回文本
        """
        if not richText:
            return richText
        while True:
            matched = False

            # 处理颜色标签
            color_match = re.search(r"<color\s*=\s*.*?>(.*?)</color>", richText)
            if color_match:
                full_match = color_match[0]
                txt = color_match[1]

                if color_attr := re.search(r"<color\s*=\s*(.*?)>", full_match):
                    color = re.sub(r'[\s"]', "", color_attr[1])
                    replacement = (
                        txt if richText else f'<span style="color:{color}">{txt}</span>'
                    )
                    richText = re.sub(
                        r"<color\s*=\s*.*?>(.*?)</color>",
                        replacement,
                        richText,
                        count=1,
                    )
                    matched = True
                    continue

            if italic_match := re.search(r"<i>(.*?)</i>", richText):
                txt = italic_match[1]
                replacement = txt if onlyText else f"<i>{txt}</i>"
                richText = re.sub(r"<i>(.*?)</i>", replacement, richText, count=1)
                matched = True
                continue

            if bold_match := re.search(r"<b>(.*?)</b>", richText):
                txt = bold_match[1]
                replacement = txt if onlyText else f"<b>{txt}</b>"
                richText = re.sub(r"<b>(.*?)</b>", replacement, richText, count=1)
                matched = True
                continue

            if "\n" in richText or "\r" in richText:
                richText = re.sub(r"\r?\n", "<br>", richText)
                matched = True

            if not matched:
                break

        return richText

    @staticmethod
    async def authority(session: Uninfo) -> bool:
        """是否是管理员"""
        groupId = session.scene.id if ensure_group(session) else None
        return await LevelUser.get_user_level(session.user.id, groupId) >= 5

    @staticmethod
    def match_range(
        msg: str, range_list: list, max_val: float = MAX_DIFFICULTY, min_val: float = 0
    ) -> list[float]:
        """
        捕获消息中的数值范围

        :param msg: 消息字符串
        :param range_list: 要修改的列表
        :param max_val: 最大值
        :param min_val: 最小值
        """
        range_list[0] = min_val
        range_list[1] = max_val
        if result := re.search(r"(\d+\.?\d*)\s*[-～~]\s*(\d+\.?\d*)", msg):
            # 0-16.9
            start_str, end_str = result.groups()
            start, end = float(start_str), float(end_str)

            range_list[0] = start
            range_list[1] = end

            # 保证范围顺序正确
            if start > end:
                range_list[0], range_list[1] = end, start

            # 特殊处理：当上限为整数且原始字符串不含小数点时
            if float(range_list[1]).is_integer() and "." not in end_str:
                range_list[1] += 0.9
        elif result := re.search(r"(\d+\.?\d*)\s*([-+])", msg):
            # 16.9- 15+
            num_str, symbol = result.groups()
            num = float(num_str)

            if symbol == "+":
                range_list[0] = num
            else:  # symbol == '-'
                range_list[1] = num
                # 特殊处理：当数值为整数且原始字符串不含小数点时
                if num.is_integer() and "." not in num_str:
                    range_list[1] += 0.9
        elif result := re.search(r"(\d+\.?\d*)", msg):
            num_str = result[1]
            num = float(num_str)

            range_list[0] = range_list[1] = num

            # 特殊处理：当原始字符串不含小数点时
            if "." not in num_str:
                range_list[1] += 0.9
        return range_list

    @staticmethod
    def match_request(
        msg: str, max_val: float = MAX_DIFFICULTY, min_val: float = 0
    ) -> dict:
        """
        匹配消息中对成绩的筛选

        :param msg: 消息内容
        :param max: 范围最大值
        :param min: 范围最小值
        """
        range_list = [min_val, max_val]
        # EZ HD IN AT
        isask = [True, True, True, True]
        msg = msg.upper()
        if "EZ" in msg or "HD" in msg or "IN" in msg or "AT" in msg:
            isask = [False, False, False, False]
        if "EZ" in msg:
            isask[0] = True
        if "HD" in msg:
            isask[1] = True
        if "IN" in msg:
            isask[2] = True
        if "AT" in msg:
            isask[3] = True
        msg = (
            msg.replace("EZ", "").replace("HD", "").replace("IN", "").replace("AT", "")
        )
        scoreAsk = {
            "NEW": True,
            "F": True,
            "C": True,
            "B": True,
            "A": True,
            "S": True,
            "V": True,
            "FC": True,
            "PHI": True,
        }
        if (
            "NEW" in msg
            or "F" in msg
            or "C" in msg
            or "B" in msg
            or "A" in msg
            or "S" in msg
            or "V" in msg
            or "FC" in msg
            or "PHI" in msg
        ):
            scoreAsk = {
                "NEW": False,
                "F": False,
                "C": False,
                "B": False,
                "A": False,
                "S": False,
                "V": False,
                "FC": False,
                "PHI": False,
            }
        for i in scoreAsk:
            if i in msg:
                scoreAsk[i] = True
        if " AP" in msg:
            scoreAsk["PHI"] = True
        for i in scoreAsk:
            msg = msg.replace(i, "")
        range_list = fCompute.match_range(msg, range_list, max_val, min_val)
        return {"range": range_list, "scoreAsk": scoreAsk, "isask": isask}

    @staticmethod
    async def recallMsg(bot: Bot, messageId: str):
        await WithdrawManager.withdraw_message(bot, messageId)

    @staticmethod
    def date2str(date: datetime | str | float | None) -> str | None:
        """
        转换时间格式

        :return: 2020/10/08 10:08:08
        """
        return Date(date).strftime("%Y/%m/%d %H:%M:%S") if date else None

    @staticmethod
    def getRandomBgColor() -> str:
        """定义一个函数，不接受参数，返回一个随机的背景色"""
        red = random.randint(0, 200)
        green = random.randint(0, 200)
        blue = random.randint(0, 200)
        return f"#{fCompute.toHex(red)}{fCompute.toHex(green)}{fCompute.toHex(blue)}"

    @staticmethod
    def toHex(num: int) -> str:
        """定义一个函数，接受一个整数参数，返回它的十六进制形式"""
        return hex(num)[2:]

    @staticmethod
    def rate(real_score: float, tot_score: float, fc: bool) -> str:
        """
        :param real_score: 真实成绩
        :param tot_score: 总成绩
        :param fc: 是否fc
        """
        if not real_score:
            return "F"
        elif real_score >= tot_score:
            return "phi"
        elif fc:
            return "FC"
        elif real_score >= tot_score * 0.96:
            return "V"
        elif real_score >= tot_score * 0.92:
            return "S"
        elif real_score >= tot_score * 0.88:
            return "A"
        elif real_score >= tot_score * 0.82:
            return "B"
        elif real_score >= tot_score * 0.70:
            return "C"
        else:
            return "F"

    @staticmethod
    def percentage(value: float, range_list: list[float]) -> float:
        """
        计算百分比

        :param value: 值
        :param range_list: 区间数组 (0,..,1)
        :return: 百分数，单位%
        """
        if range_list[0] == range_list[-1]:
            return 50
        else:
            return round(
                ((value - range_list[0]) / (range_list[-1] - range_list[0]) * 100),
                2,
            )

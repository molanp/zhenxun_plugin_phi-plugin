from pathlib import Path
from typing import Any

from pydantic import BaseModel

from zhenxun.configs.config import Config as PluginConfig
from zhenxun.configs.utils import RegisterConfig

PATH = Path(__file__).parent.parent

VERSION = "0.1.0"


class config(BaseModel):
    onLinePhiIllUrl: str = "https://gitee.com/Steveeee-e/phi-plugin-ill/raw/main/"
    """
    在线曲绘来源。仅在未下载曲绘时有效，不影响下载曲绘指令。
    在线曲绘将重复下载曲绘资源，建议使用 /下载曲绘 将曲绘缓存到本地
    """
    # github
    # https://github.com/Catrong/phi-plugin-ill/blob/main
    # gitee
    # https://gitee.com/Steveeee-e/phi-plugin-ill/raw/main
    downIllUrl: str = (
        "https://github.bibk.top/Catrong/phi-plugin-ill/archive/refs/heads/main.zip"
    )
    """下载曲绘来源"""
    B19MaxNum: int = 33
    """渲染设置|用户可以获取B19图片成绩的最大数量"""
    HistoryDayNum: int = 10
    """渲染设置|/update 展现历史成绩的单日最大数量，至少为2"""
    HistoryDateNum: int = 10
    """渲染设置|/update 展现历史成绩的最大天数"""
    HistoryScoreNum: int = 10
    """渲染设置|update 展现历史成绩的最大数量"""
    listScoreMaxNum: int = 300
    """渲染设置|/list 展现成绩的最大数量，建议为3的倍数"""
    autoPullPhiIll: bool = True
    """系统设置|自动更新曲绘，开启后手动更新插件时自动更新曲绘文件"""
    isGuild: bool = False
    """系统设置|频道模式，开启后文字版仅限私聊，关闭文字版图片，文字版将折叠为长消息"""
    TapTapLoginQRcode: bool = True
    """系统设置|登录TapTap绑定是否发送二维码，开启仅发送二维码，关闭直接发送链接"""
    cmdhead: str = "/phi"
    """系统设置|命令头"""
    GuessTipCd: int = 15
    """猜曲绘设置|猜曲绘提示间隔，单位：秒"""
    GuessRecall: bool = True
    """猜曲绘设置|是否在下一条提示发出的时候撤回上一条"""
    LetterNum: int = 8
    """开字母设置|开字母条数"""
    VikaToken: str = ""
    """其他设置|VikaToken,填写后请重载配置"""

    def __getattr__(self, name: str) -> Any:
        """获取配置项"""
        return PluginConfig.get_config("phi_plugin", name.upper())

    def __setattr__(self, name: str, value: Any) -> None:
        """设置配置项"""
        PluginConfig.set_config("phi_plugin", name.upper(), value, True)


CONFIG = [
    RegisterConfig(
        key=name,
        value=getattr(config, name),
        help=getattr(getattr(config, name).__class__, f"__doc__{name}__", ""),
    )
    for name in dir(config)
    if not name.startswith("_")
]

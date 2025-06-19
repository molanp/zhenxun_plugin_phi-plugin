import importlib
from pathlib import Path

from nonebot.plugin import PluginMetadata

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger

from .components.Config import CONFIG, VERSION, PluginConfig

__plugin_meta__ = PluginMetadata(
    name="phi-plugin",
    description="Phigros查分及娱乐插件",
    usage=f"""
    发送 {PluginConfig.get("cmdhead")}帮助 获取详细帮助信息
    """.strip(),
    extra=PluginExtraData(
        author="molanp",
        version=VERSION,
        configs=CONFIG,
    ).dict(),
)

logger.info("------φ^_^φ------")
logger.info("正在载入phi插件...")
logger.info("--------------------------------------")
logger.info(f"phi插件 {VERSION} 载入完成~")
logger.info("作者：@Cartong | 移植：@molanp")
logger.info("仓库地址：https://github.com/molanp/zhenxun_plugin_phi-plugin")
logger.info("本项目云存档功能由 7aGiven/PhigrosLibrary 改写而来")
logger.info("--------------------------------------")


for module in (Path(__file__).parent.resolve() / "apps").glob("**/*.py"):
    name = module.name[:-3]
    if name != "__init__":
        importlib.import_module(f".apps.{name}", package=__name__)

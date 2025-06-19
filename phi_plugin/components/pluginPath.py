from zhenxun.configs.path_config import DATA_PATH

from .Config import PATH

pluginResources = PATH / "resources"
"""插件资源目录"""
htmlPath = pluginResources / "html"

infoPath = pluginResources / "info"
"""曲绘资源、曲目信息路径"""
DlcInfoPath = pluginResources / "info" / "DLC"
"""额外曲目名称信息（开字母用）"""
imgPath = pluginResources / "html" / "otherimg"
"""默认图片路径"""
dataPath = DATA_PATH / "phi-plugin"
"""数据路径"""
pluginDataPath = dataPath / "pluginData"
"""用户娱乐数据路径"""
savePath = dataPath / "saveData"
"""用户存档数据路径"""
backupPath = dataPath / "backup"
"""备份路径"""
originalIllPath = pluginResources / "original_ill"
"""原画资源"""

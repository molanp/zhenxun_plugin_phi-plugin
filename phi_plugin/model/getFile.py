import csv
from io import StringIO
from pathlib import Path
import re
from typing import Any

import aiofiles
from ruamel.yaml import YAML
import ujson

from ..components.Logger import logger


async def csv_write(file_path: str | Path, data: list[dict[str, Any]]):
    """
    data: list[dict]
    ```
    [
        {
            "id": "1",
            "name": "张三",
            "age": "18"
        },
        {
            "id": "2",
            "name": "李四",
            "age": "19"
        }
    ]
    """
    fieldnames = data[0].keys()

    async with aiofiles.open(file_path, mode="w", encoding="utf-8", newline="") as f:
        # 先写入表头
        csv.DictWriter(f, fieldnames=fieldnames)
        await f.write(",".join(fieldnames) + "\n")

        # 逐行写入数据
        for row in data:
            line = ",".join([str(row.get(field, "")) for field in fieldnames]) + "\n"
            await f.write(line)


async def csv_read(file_path: str | Path) -> list[dict[str, Any]]:
    """
    return list[dict]
    ```
    [
        {
            "id": 1,
            "name": "n1",
            "age": 114
        },
        {
            "id": 2,
            "name": "n2",
            "age": 39
        }
    ]
    """
    async with aiofiles.open(file_path, encoding="utf-8") as f:
        content = await f.read()

    # 使用 StringIO 模拟文件对象供 csv 模块使用
    f_obj = StringIO(content)
    reader = csv.DictReader(f_obj)
    return [dict(row) for row in reader]


class getFile:
    @staticmethod
    def FileReader(
        filePath: str | Path, style: str | None = None, variables: dict | None = None
    ):
        """
        同步读取文件

        :param filePath: 完整路径
        :param style: 强制设置文件格式['JSON' , 'YAML' , 'TXT']
        :param variables: 需要替换的变量对象 例如：{ username: 'John' }
        """
        if variables is None:
            variables = {}
        if isinstance(filePath, str):
            filePath = Path(filePath)
        try:
            if not filePath.exists():
                return False
            if not style:
                style = filePath.suffix.upper().replace(".", "")
            match style:
                case "JSON":
                    with open(filePath, encoding="utf-8") as f:
                        return getFile.replaceVariables(
                            ujson.loads(f.read()), variables
                        )
                case "YAML":
                    with open(filePath, encoding="utf-8") as f:
                        return getFile.replaceVariables(
                            YAML().load(f.read()), variables
                        )
                case _:
                    with open(filePath, encoding="utf-8") as f:
                        return getFile.replaceVariables(f.read(), variables)
        except Exception as e:
            logger.error(f"[{filePath}] 读取失败", "phi-plugin", e=e)
            return None

    @staticmethod
    def replaceVariables(content: Any, variables: dict):
        """
        替换文本中的占位符

        :param content: 内容
        :param variables: 需要替换的变量字典
        """
        if not variables:
            return content

        if isinstance(content, str):
            return re.sub(
                r"\{(\w+)\}",
                lambda match: variables.get(match.group(1), f"{{{match.group(1)}}}"),
                content,
            )
        if isinstance(content, dict):
            for key, value in content.items():
                content[key] = getFile.replaceVariables(value, variables)
            return content

        return content

    @staticmethod
    async def csvReader(filePath: str | Path):
        return await csv_read(filePath)

    @staticmethod
    def SetFile(filePath: str | Path, data: Any, style: str | None = None):
        """
        储存文件

        :param filePath: 文件路径
        :param data: 目标数据
        :param style: 强制设置文件格式['JSON' , 'YAML' , 'TXT']
        """
        if isinstance(filePath, str):
            filePath = Path(filePath)
        try:
            fatherPath = filePath.parent
            if not fatherPath.exists():
                fatherPath.mkdir(parents=True)
            if not style:
                style = filePath.suffix.upper().replace(".", "")
            match style:
                case "JSON":
                    with open(filePath, "w", encoding="utf-8") as f:
                        f.write(ujson.dumps(data))
                case "YAML":
                    with open(filePath, "w", encoding="utf-8") as f:
                        f.write(YAML().dump(data))
                case _:
                    with open(filePath, "w", encoding="utf-8") as f:
                        f.write(data)
            return True
        except Exception as e:
            logger.error(f"写入文件 {filePath} 失败", "phi-plugin", e=e)
            return False

    @staticmethod
    def DelFile(path: str | Path):
        if isinstance(path, str):
            path = Path(path)
        try:
            if not path.exists():
                return False
            path.unlink()
            return True
        except Exception as e:
            logger.error(f"[{path}] 删除失败", "phi-plugin", e=e)
            return False

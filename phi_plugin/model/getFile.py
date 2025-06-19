import asyncio
import csv
from io import StringIO
from pathlib import Path
from typing import Any, Literal, cast

import aiofiles
from ruamel.yaml import YAML
import ujson as json

from zhenxun.services.log import logger

from .getRksRank import getRksRank
from ..components.pluginPath import dataPath, pluginDataPath, savePath

SUPPORTED_FORMATS = Literal["JSON", "YAML", "CSV", "TXT"]


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


# TODO: 完善其余方法

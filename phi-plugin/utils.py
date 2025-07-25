import contextlib
from datetime import datetime, timezone
from typing import Any


def to_dict(c: Any) -> dict:
    if c is None:
        return {}

    def convert(value: Any) -> Any:
        if hasattr(value, "model_dump"):
            return value.model_dump()
        if hasattr(value, "to_dict"):
            return value.to_dict()
        if isinstance(value, list | tuple):
            return [convert(v) for v in value]
        if isinstance(value, dict):
            return {k: convert(v) for k, v in value.items()}

        if isinstance(value, type):
            return {
                k: convert(v) for k, v in vars(value).items()
            }

        if hasattr(value, "__dict__"):
            return {
                k: convert(v) for k, v in vars(value).items()
            }

        return value

    return dict(convert(c))


def Date(date_input: datetime | str | float | None) -> datetime:
    """
    将多种格式的时间输入转换为 Python datetime 对象，并始终使用本地时区

    :param date_input: 时间表示
    :return: 解析后的时间对象，失败返回时间戳 0 对应的本地时间
    """
    if date_input is None:
        return datetime.fromtimestamp(0)
    if isinstance(date_input, datetime):
        dt = date_input
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone()
    try:
        if isinstance(date_input, str):
            # 优先尝试直接解析带时区的 ISO 格式（含 Z）
            with contextlib.suppress(ValueError):
                dt = datetime.fromisoformat(date_input.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.astimezone()

            formats = (
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%Y/%m/%d %H:%M:%S",
                "%a %b %d %H:%M:%S %Y",
            )

            for fmt in formats:
                try:
                    return datetime.strptime(date_input, fmt)
                except ValueError:
                    continue

        elif isinstance(date_input, float | int):
            timestamp = float(date_input)
            if timestamp < 0:
                return datetime.fromtimestamp(0)
            if timestamp > 1e12:
                timestamp /= 1000
            return datetime.fromtimestamp(timestamp)

    except Exception:
        return datetime.fromtimestamp(0)

    return datetime.fromtimestamp(0)


def Rating(score: int | None, fc: bool):
    if score is None:
        return "NEW"
    elif score >= 1000000:
        return "phi"
    elif fc:
        return "FC"
    elif score < 700000:
        return "F"
    elif score < 820000:
        return "C"
    elif score < 880000:
        return "B"
    elif score < 920000:
        return "A"
    elif score < 960000:
        return "S"
    else:
        return "V"

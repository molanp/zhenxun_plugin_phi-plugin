from .getdata import get


class money:
    @staticmethod
    async def getNoteNum(user_id: str) -> int:
        return await get.getpluginData(user_id)

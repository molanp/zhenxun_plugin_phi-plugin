# // import { redis } from 'yunzai'

# import { redis } from "../components/redis"
# import { redisPath } from "./constNum"
# import { $ } from 'koishi'
from ..models import phigrosUserRks


class getRksRank:
    @staticmethod
    async def addUserRks(sessionToken: str, rks: float) -> bool:
        """
        添加成绩

        :param sessionToken: SessionToken
        :param rks: rks
        """
        return await phigrosUserRks.set_user_rks(sessionToken, rks)

    @staticmethod
    async def delUserRks(sessionToken: str) -> bool:
        """
        删除成绩

        :param sessionToken: SessionToken
        """
        return await phigrosUserRks.delete_user_rks(sessionToken)

    @staticmethod
    async def getUserRank(sessionToken: str) -> int | None:
        """
        获取用户排名

        :param sessionToken: SessionToken
        """
        return await phigrosUserRks.getUserRank(sessionToken)

    @staticmethod
    async def getUserRks(sessionToken: str) -> float | None:
        """
        获取用户RKS

        :param sessionToken: SessionToken
        """
        return await phigrosUserRks.get_user_rks(sessionToken)

    @staticmethod
    async def getRankUser(min_rank: int, max_rank: int):
        """
        获取指定排名范围的用户数据（基于RKS分数降序）

        :param min_rank: 起始排名（0起始）
        :param max_rank: 结束排名（不包含）
        :return: 包含用户数据的字典列表
        """
        return await phigrosUserRks.getRankUsers(min_rank, max_rank)

    @staticmethod
    async def getAllRank():
        """
        获取所有用户数据（基于RKS分数降序）

        :return: 包含所有用户数据的字典列表
        """
        return await phigrosUserRks.getAllRank()

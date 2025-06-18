// import { redis } from 'yunzai'

import { redis } from "../components/redis"
import { redisPath } from "./constNum"
import { $ } from 'koishi'


export default new class getRksRank {
    /**
     * 添加成绩
     * @param {string} sessionToken 
     * @param {number} rks 
     */
    async addUserRks(sessionToken: string, rks: number) {
        return await redis.upsert('phigrosUserRks', [{ token: sessionToken, rks: rks }], 'token')
    }

    /**
     * 删除成绩
     * @param {string} sessionToken 
     */
    async delUserRks(sessionToken: string) {
        return await redis.remove('phigrosUserRks', { token: sessionToken })
    }

    /**
     * 获取用户排名
     * @param {number} rks 
     */
    async getUserRank(rks: number): Promise<number> {
        return await redis
            .select('phigrosUserRks')
            .where(row => $.gt(row.rks, rks))
            .execute(row => $.count(row.id))
    }

    /**
     * 获取sessionToken rks
     * @param {number} sessionToken 
     * @returns {Promise<number>}
     */
    async getUserRks(sessionToken: string) {
        return (await redis.get('phigrosUserRks', { token: sessionToken }, ['rks']))[0]
    }

    /**
     * 获取排名
     * @param {number} min 0起
     * @param {number} max 不包含
     */
    async getRankUser(min: number, max: number) {
        return await redis
            .select('phigrosUserRks')
            .orderBy('rks', 'desc')
            .limit(min)
            .offset(max - min)
            .execute()
    }

    /**
     * 获取所有排名
     */
    async getAllRank() {
        return await redis
            .select('phigrosUserRks')
            .orderBy('rks', 'desc')
            .execute()
    }
}()
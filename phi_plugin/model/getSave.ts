import path from 'path'
import { savePath } from "../components/pluginPath"
import { redis } from '../components/redis'
import getFile from "./getFile"
import Save from './class/Save'
import fs from 'fs'
import saveHistory from './class/saveHistory'
import getRksRank from './getRksRank'
import PhigrosUser from '../lib/PhigrosUser'
// import { redis } from 'yunzai'

export default class getSave {

    /**获取 user_id 号对应的 Token */
    static async get_user_token(user_id: string): Promise<string> {
        return (await redis.get('phigrosUserToken', { userId: user_id }))[0]?.token
    }

    /**添加 user_id 号对应的 Token */
    static async add_user_token(user_id: string, token: string) {
        return await redis.upsert('phigrosUserToken', [{ userId: user_id, token: token }], 'userId')
    }

    /**移除 user_id 对应的 Token */
    static async del_user_token(user_id: string) {
        return await redis.remove('phigrosUserToken', { userId: user_id })
    }

    /**
     * 获取 user_id 对应的存档文件
     * @param {String} user_id user_id
     * @returns {Promise<Save>}
     */
    static async getSave(user_id: string): Promise<Save> {
        let Token = await this.get_user_token(user_id)
        if (await this.isBanSessionToken(Token)) {
            throw new Error(`${Token} 已被禁用`)
        }
        let result = Token ? await getFile.FileReader(path.join(savePath, Token, 'save.json')) : null
        if (result) {
            let tem = new Save(result)
            if (tem.saveInfo) {
                // await tem.init()
            } else {
                return null
            }
            return tem
        } else {
            return null
        }
    }

    /**
     * 获取 sessionToken 对应的存档文件
     * @param {string} Token 
     * @returns 
     */
    static async getSaveBySessionToken(Token: string) {
        // console.info(Token)
        if (await this.isBanSessionToken(Token)) {
            throw new Error(`${Token} 已被禁用`)
        }
        let result = Token ? await getFile.FileReader(path.join(savePath, Token, 'save.json')) : null
        if (result) {
            let tem = new Save(result)
            if (tem.saveInfo) {
                // await tem.init()
            } else {
                return null
            }
            return tem
        } else {
            return null
        }
    }

    /**
     * 保存 user_id 对应的存档文件
     * @param {String} user_id user_id
     * @param {Save} data 
     */
    static async putSave(user_id: string, data: Save | PhigrosUser) {
        let session = data.sessionToken
        if (await this.isBanSessionToken(session)) {
            throw new Error(`${session} 已被禁用`)
        }
        this.add_user_token(user_id, session)
        await getRksRank.addUserRks(session, data.saveInfo.summary.rankingScore)
        return await getFile.SetFile(path.join(savePath, session, 'save.json'), data)
    }

    /**
     * 获取 user_id 对应的历史记录
     * @param {string} user_id 
     * @returns {Promise<saveHistory>}
     */
    static async getHistory(user_id: string): Promise<saveHistory> {
        let session = await this.get_user_token(user_id)
        let result = session ? await getFile.FileReader(path.join(savePath, session, 'history.json')) : null
        return new saveHistory(result)
    }

    /**
     * 保存 user_id 对应的历史记录
     * @param {String} user_id user_id
     * @param {Object} data 
     */
    static async putHistory(user_id: string, data: object) {
        let session = await this.get_user_token(user_id)
        return await getFile.SetFile(path.join(savePath, session, 'history.json'), data)
    }


    /**
     * 获取玩家 Dan 数据
     * @param {string} user_id QQ号
     * @param {boolean} [all=false] 是否返回所有数据
     * @returns {object|Array} Dan数据
     */
    static async getDan(user_id: string, all: boolean = false): Promise<object | any[]> {
        let history = await this.getHistory(user_id)

        let dan = history?.dan

        if (dan && Object.prototype.toString.call(dan) != '[object Array]') {
            dan = [dan]
        }
        return dan ? (all ? dan : dan[0]) : undefined
    }

    /**
     * 删除 user_id 对应的存档文件
     * @param {String} user_id user_id
     */
    static async delSave(user_id: string) {
        let session = await this.get_user_token(user_id)
        if (!session) return false
        let fPath = path.join(savePath, session)
        await getFile.DelFile(path.join(fPath, 'save.json'))
        await getFile.DelFile(path.join(fPath, 'history.json'))
        await getRksRank.delUserRks(session)
        fs.rmSync(path.join(savePath, session), { recursive: true, force: true });
        this.del_user_token(user_id)
        return true
    }

    /**
     * 删除 token 对应的存档文件
     * @param {String} Token Token
     */
    static async delSaveBySessionToken(Token: string) {
        let fPath = path.join(savePath, Token)
        await getFile.DelFile(path.join(fPath, 'save.json'))
        await getFile.DelFile(path.join(fPath, 'history.json'))
        await getRksRank.delUserRks(Token)
        fs.rmSync(path.join(savePath, Token), { recursive: true, force: true });
        return true
    }

    static async banSessionToken(token: string) {
        return await redis.upsert('phigrosBanSessionToken', [{ sessionToken: token }], 'sessionToken')
    }

    static async allowSessionToken(token: string) {
        return await redis.remove('phigrosBanSessionToken', { sessionToken: token })
    }

    static async isBanSessionToken(token: string) {
        return (await redis.get('phigrosBanSessionToken', { sessionToken: token }))[0] ? true : false
    }

    static async getGod() {
        return await redis.get('phigrosBanSessionToken', { id: { $lt: -1 } }, ['sessionToken'])
    }

}

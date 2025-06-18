import render from "./render"
import getInfo from "./getInfo"
import { imgPath } from "../components/pluginPath"
import { logger } from "../components/Logger"
import { Context, Keys } from "koishi"
import { idString } from "./type/type"

export default class pic {

    /**
     * 获取歌曲图鉴，曲名为原名
     * @param ctx 上下文
     * @param id 曲名
     * @param data 自定义数据
     * @returns 
     */
    static async GetSongsInfoAtlas(ctx: Context, id: idString, data: any = undefined) {
        data = data || getInfo.info(id)
        if (data) {
            if (!data.illustration) { data.illustration = getInfo.getill(id) }
            return await render(ctx, 'song', data)
        } else {
            /**未找到曲目 */
            return `未找到${id}的相关曲目信息!QAQ`
        }
    }

    /**
     * 获取曲绘图鉴
     * @param {*} e 消息e
     * @param {string} id 原曲名称
     * @param { {illustration:string, illustrator:string} } data 自定义数据
     * @returns 
     */
    static async GetSongsIllAtlas(ctx: Context, id: idString, data: { illustration: string; illustrator: string } = undefined) {
        if (data) {
            return await render(ctx, 'ill', { illustration: data.illustration, illustrator: data.illustrator })
        } else {
            return await render(ctx, 'ill', { illustration: getInfo.getill(id), illustrator: getInfo.info(id).illustrator })
        }
    }

    /**
     * 获取本地图片，文件格式默认png
     * @param {string} img 文件名
     * @param {string} style 文件格式，默认为png
     */
    static getimg(img: string, style: string = 'png'): string {
        // name = 'phi'
        let url = `${imgPath}/${img}.${style}`
        if (url) {
            return url
        }
        logger.info('未找到 ' + `${img}.${style}`)
        return null
    }

}
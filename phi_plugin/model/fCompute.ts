import { MAX_DIFFICULTY } from './constNum'
import { logger } from '../components/Logger'
import { Session } from 'koishi'
import { h } from 'koishi'
import getInfo from './getInfo'
import { songString } from './type/type'

export default class compute {
    /**
     * 计算等效rks
     * @param {number} acc 
     * @param {number} difficulty 
     * @returns 
     */
    static rks(acc: number, difficulty: number) {
        if (acc == 100) {
            /**满分原曲定数即为有效rks */
            return Number(difficulty)
        } else if (acc < 70) {
            /**无效acc */
            return 0
        } else {
            /**非满分计算公式 [(((acc - 55) / 45) ^ 2) * 原曲定数] */
            return difficulty * (((acc - 55) / 45) * ((acc - 55) / 45))
        }
    }

    /**
     * 计算所需acc
     * @param {Number} rks 目标rks
     * @param {Number} difficulty 定数
     * @param {Number} [count=undefined] 保留位数
     * @returns 所需acc
     */
    static suggest(rks: number, difficulty: number, count: number = undefined): string | number {
        let ans = 45 * Math.sqrt(rks / difficulty) + 55

        if (ans >= 100)
            return "无法推分"
        else {
            if (count != undefined) {
                return `${ans.toFixed(count)}%`
            } else {
                return ans
            }
        }
    }

    /**
     * 发送文件
     * @param e 
     * @param file 
     * @param title 文件名称
     */
    static async sendFile(session: Session, file: Buffer, title: string = "") {
        try {
            session.send(h.file(file, "application/octet-stream", { title }))
        } catch (err) {
            logger.error(`文件上传错误：`)
            logger.error(err)
            await session.send(`文件上传错误` + err.message)
        }
    }

    /**
     * 获取角色介绍背景曲绘
     * @param {string} save_background 
     * @returns 
     */
    static async getBackground(save_background: string) {
        try {
            switch (save_background) {
                case 'Another Me ': {
                    save_background = 'Another Me (KALPA)'
                    break
                }
                case 'Another Me': {
                    save_background = 'Another Me (Rising Sun Traxx)'
                    break
                }
                case 'Re_Nascence (Psystyle Ver.) ': {
                    save_background = 'Re_Nascence (Psystyle Ver.)'
                    break
                }
                case 'Energy Synergy Matrix': {
                    save_background = 'ENERGY SYNERGY MATRIX'
                    break
                }
                case 'Le temps perdu-': {
                    save_background = 'Le temps perdu'
                    break
                }
                default: {
                    break
                }
            }
            return getInfo.getill(getInfo.SongGetId(save_background as songString))
        } catch (err) {
            logger.error(`获取背景曲绘错误`, err)
            return false
        }
    }

    /**
     * 为数字添加前导零
     * @param {number} num 原数字
     * @param {number} cover 总位数
     * @returns 前导零数字
     */
    static ped(num: number, cover: number) {
        return String("0".repeat(cover) + num).slice(-cover)
    }

    /**
     * 标准化分数
     * @param {number} score 分数
     * @returns 标准化的分数 0'000'000
     */
    static std_score(score: number) {
        let s1 = Math.floor(score / 1e6)
        let s2 = Math.floor(score / 1e3) % 1e3
        let s3 = score % 1e3
        return `${s1}'${this.ped(s2, 3)}'${this.ped(s3, 3)}`
    }

    /**
     * 随机数，包含上下界
     * @param {number} min 最小值
     * @param {number} max 最大值
     * @returns 随机数
     */
    static randBetween(min: number, max: number) {
        return Math.floor(Math.random() * (max - min + 1) + min)
    }

    /**
     * 随机打乱数组
     * @param {Array} arr 原数组
     * @returns 随机打乱的数组
     */
    static randArray(arr: Array<any>) {
        let newArr = []
        while (arr.length > 0) {
            newArr.push(arr.splice(Math.floor(Math.random() * arr.length), 1)[0])
        }
        return newArr
    }

    /**
     * 转换时间格式
     * @param {Date|string} date 时间
     * @returns 2020/10/8 10:08:08
     */
    static formatDate(date: Date | string) {
        date = new Date(date)
        return `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()} ${date.toString().match(/([0-9])+:([0-9])+:([0-9])+/)[0]}`
    }

    /**
     * 转换unity富文本
     * @param {string} richText 
     * @param {boolean} [onlyText=false] 是否只返回文本
     * @returns 
     */
    static convertRichText(richText: string, onlyText: boolean = false) {
        if (!richText) {
            return richText
        }
        richText = richText.replace(/</g, '&lt;').replace(/>/g, '&gt;');
        let reg = [/&lt;color\s*=\s*.*?&gt;(.*?)&lt;\/color&gt;/, /&lt;size\s*=\s*.*?&gt;(.*?)&lt;\/size&gt;/, /&lt;i&gt;(.*?)&lt;\/i&gt;/, /&lt;b&gt;(.*?)&lt;\/b&gt;/]
        while (1) {
            if (richText.match(reg[0])) {
                let txt = richText.match(reg[0])[1]
                let color = richText.match(reg[0])[0].match(/&lt;color\s*=\s*(.*?)&gt;/)[1].replace(/[\s\"]/g, '')
                richText = richText.replace(reg[0], onlyText ? txt : `<span style="color:${color}">${txt}</span>`)
                continue
            }

            if (richText.match(reg[2])) {
                let txt = richText.match(reg[2])[1]
                richText = richText.replace(reg[2], onlyText ? txt : `<i>${txt}</i>`)
                continue
            }

            if (richText.match(reg[3])) {
                let txt = richText.match(reg[3])[1]
                richText = richText.replace(reg[3], onlyText ? txt : `<b>${txt}</b>`)
                continue
            }
            // if (richText.match(reg[1])) {
            //     let txt = richText.match(reg[1])[1]
            //     let size = richText.match(reg[1])[0].match(/size\s*=[^>]*?([^>]*)/)[1]o
            //     return this.convertRichText(richText.replace(reg[1], `<span style="font-size:${size}px">${txt}</span>`))
            // }
            if (richText.match(/\n\r?/)) {
                richText.replace(/\n\r?/g, '<br>')
            }
            break
        }
        if (onlyText) {
            richText = richText.replace(/&lt;/g, '<').replace(/&gt;/g, '>');
        }
        return richText
    }

    /**是否是管理员 */
    static authority(session: Session) {
        let sessionRoles = session?.event?.member?.roles
        return sessionRoles && (sessionRoles.includes('admin') || sessionRoles.includes('owner'))
    }

    /**
     * 捕获消息中的范围
     * @param {string} msg 消息字符串
     * @param {Array} range 范围数组
     * @param {number} [max=MAX_DIFFICULTY] 最大值
     * @param {number} [min=0] 最小值
     */
    static match_range(msg: string, range: Array<any>, max: number = MAX_DIFFICULTY, min: number = 0) {
        range[0] = min
        range[1] = max
        if (msg.match(/[0-9]+(.[0-9]+)?\s*[-～~]\s*[0-9]+(.[0-9]+)?/g)) {
            /**0-16.9 */
            msg = msg.match(/[0-9]+(.[0-9]+)?\s*[-～~]\s*[0-9]+(.[0-9]+)?/g)[0]
            let result = msg.split(/\s*[-～~]\s*/g)
            range[0] = Number(result[0])
            range[1] = Number(result[1])
            if (range[0] > range[1]) {
                let tem = range[1]
                range[1] = range[0]
                range[0] = tem
            }
            if (range[1] % 1 == 0 && !result.includes(".0")) range[1] += 0.9
        } else if (msg.match(/[0-9]+(.[0-9]+)?\s*[-+]/g)) {
            /**16.9- 15+ */
            msg = msg.match(/[0-9]+(.[0-9]+)?\s*[-+]/g)[0]
            let result = msg.replace(/\s*[-+]/g, '')
            if (msg.includes('+')) {
                range[0] = Number(result)
            } else {
                range[1] = Number(result)
                if (range[1] % 1 == 0 && !result.includes(".0")) range[1] += 0.9
            }
        } else if (msg.match(/[0-9]+(.[0-9]+)?/g)) {
            /**15 */
            msg = msg.match(/[0-9]+(.[0-9]+)?/g)[0]
            range[0] = range[1] = Number(msg)
            if (!msg.includes('.')) {
                range[1] += 0.9
            }
        }

    }

    /**
     * 匹配消息中对成绩的筛选
     * @param {string} msg 
     * @param {number} [max=MAX_DIFFICULTY] 范围最大值
     * @param {number} [min=0] 范围最小值
     * @returns 
     */
    static match_request(msg: string = "", max: number = MAX_DIFFICULTY, min: number = 0) {
        let range = [min, max]

        /**EZ HD IN AT */
        let isask = [true, true, true, true]

        msg = msg.toUpperCase()

        if (msg.includes('EZ') || msg.includes('HD') || msg.includes('IN') || msg.includes('AT')) {
            isask = [false, false, false, false]
            if (msg.includes('EZ')) { isask[0] = true }
            if (msg.includes('HD')) { isask[1] = true }
            if (msg.includes('IN')) { isask[2] = true }
            if (msg.includes('AT')) { isask[3] = true }
        }
        msg = msg.replace(/(list|AT|IN|HD|EZ)*/g, "")

        let scoreAsk = { NEW: true, F: true, C: true, B: true, A: true, S: true, V: true, FC: true, PHI: true }

        if (msg.includes(' NEW') || msg.includes(' F') || msg.includes(' C') || msg.includes(' B') || msg.includes(' A') || msg.includes(' S') || msg.includes(' V') || msg.includes(' FC') || msg.includes(' PHI')) {
            scoreAsk = { NEW: false, F: false, C: false, B: false, A: false, S: false, V: false, FC: false, PHI: false }
            let rating = ['NEW', 'F', 'C', 'B', 'A', 'S', 'V', 'FC', 'PHI']
            for (let i in rating) {
                if (msg.includes(` ${rating[i]}`)) { scoreAsk[rating[i]] = true }
            }
        }
        if (msg.includes(` AP`)) { scoreAsk.PHI = true }
        msg = msg.replace(/(NEW|F|C|B|A|S|V|FC|PHI|AP)*/g, "")

        this.match_range(msg, range, max, min)
        return { range, isask, scoreAsk }
    }

    static async recallMsg(session: Session, messageId: string) {
        return await session.bot.deleteMessage(session.channelId, messageId)
    }

    static async sleep(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms))
    }


    /**
     * 转换时间格式
     * @param {Date|string} date 时间
     * @returns 2020/10/8 10:08:08
     */
    static date_to_string(date: Date | string | number): string {
        if (!date) return undefined
        date = new Date(date)

        let month = (date.getMonth() + 1) < 10 ? `0${date.getMonth() + 1}` : date.getMonth() + 1
        let day = date.getDate() < 10 ? `0${date.getDate()}` : date.getDate()

        return `${date.getFullYear()}/${month}/${day} ${date.toString().match(/([0-9])+:([0-9])+:([0-9])+/)[0]}`
    }


    // 定义一个函数，不接受参数，返回一个随机的背景色
    static getRandomBgColor() {
        // 生成三个 0 到 200 之间的随机整数，分别代表红、绿、蓝分量
        let red = Math.floor(Math.random() * 201);
        let green = Math.floor(Math.random() * 201);
        let blue = Math.floor(Math.random() * 201);
        // 将三个分量转换为十六进制形式，然后拼接成一个 RGB 颜色代码
        let hexColor = "#" + this.toHex(red) + this.toHex(green) + this.toHex(blue);
        // 返回生成的颜色代码
        return hexColor;
    }

    // 定义一个函数，接受一个整数参数，返回它的十六进制形式
    static toHex(num: number) {
        // 如果数字小于 16，就在前面补一个 0
        if (num < 16) {
            return "0" + num.toString(16);
        } else {
            return num.toString(16);
        }
    }


    /**
     * 
     * @param {number} real_score 真实成绩
     * @param {number} tot_score 总成绩
     * @param {boolean} fc 是否fc
     * @returns 
     */
    static rate(real_score: number, tot_score: number, fc: boolean) {

        if (!real_score) {
            return 'F'
        } else if (real_score == tot_score) {
            return 'phi'
        } else if (fc) {
            return 'FC'
        } else if (real_score >= tot_score * 0.96) {
            return 'V'
        } else if (real_score >= tot_score * 0.92) {
            return 'S'
        } else if (real_score >= tot_score * 0.88) {
            return 'A'
        } else if (real_score >= tot_score * 0.82) {
            return 'B'
        } else if (real_score >= tot_score * 0.70) {
            return 'C'
        } else {
            return 'F'
        }
    }

    /**
     * 计算百分比
     * @param {Number} value 值
     * @param {Array} range 区间数组 (0,..,1)
     * @returns 百分数，单位%
     */
    static percentage(value: number, range: number[]): number {
        if (range[0] == range[range.length - 1]) {
            return 50
        } else {
            return (value - range[0]) / (range[range.length - 1] - range[0]) * 100
        }
    }

}
import { Keys } from "koishi"
import fCompute from "../fCompute"
import getInfo from "../getInfo"
import { idString, levelKind } from "../type/type"

export default class scoreHistory {

    /**
     * 生成成绩记录数组
     * @param {number} acc 
     * @param {number} score 
     * @param {Date} date
     * @param {boolean} fc 
     * @returns []
     */
    static create(acc: number, score: number, date: Date, fc: boolean) {
        return [acc.toFixed(4), score, date, fc]
    }

    /**
     * 扩充信息
     * @param id 曲目id
     * @param level 难度
     * @param now 
     * @param old 
     */
    static extend(id: idString, level: levelKind, now: [number, number, Date, boolean], old?: [number, number, Date, boolean]) {
        now[0] = Number(now[0])
        now[1] = Number(now[1])
        if (old) {
            old[0] = Number(old[0])
            old[1] = Number(old[1])
        }
        if (getInfo.info(id)?.chart[level]?.difficulty) {
            /**有难度信息 */
            return {
                song: getInfo.idgetsong(id) || id,
                rank: level,
                illustration: getInfo.getill(id),
                Rating: Rating(now[1], now[3]),
                rks_new: fCompute.rks(now[0], getInfo.info(id).chart[level].difficulty),
                rks_old: old ? fCompute.rks(old[0], getInfo.info(id).chart[level].difficulty) : undefined,
                acc_new: now[0],
                acc_old: old ? old[0] : undefined,
                score_new: now[1],
                score_old: old ? old[1] : undefined,
                date_new: new Date(now[2]),
                date_old: old ? new Date(old[2]) : undefined
            }
        } else {
            /**无难度信息 */
            return {
                song: getInfo.idgetsong(id) || id,
                rank: level,
                illustration: getInfo.getill(id),
                Rating: Rating(now[1], now[3]),
                acc_new: now[0],
                acc_old: old ? old[0] : undefined,
                score_new: now[1],
                score_old: old ? old[1] : undefined,
                date_new: new Date(now[2]),
                date_old: old ? new Date(old[2]) : undefined
            }
        }
    }

    /**
     * 展开信息
     * @param {Array} data 历史成绩
     */
    static open(data: [number, number, Date, boolean]) {
        return {
            acc: data[0],
            score: data[1],
            date: new Date(data[2]),
            fc: data[3]
        }
    }

    /**
     * 获取该成绩记录的日期
     * @param {Array} data 成绩记录
     * @returns {Date} 该成绩的日期
     */
    static date(data: [number, number, Date, boolean]): Date {
        return new Date(data[2])
    }
}


function Rating(score, fc) {
    if (score >= 1000000)
        return 'phi'
    else if (fc)
        return 'FC'
    else if (score < 700000)
        return 'F'
    else if (score < 820000)
        return 'C'
    else if (score < 880000)
        return 'B'
    else if (score < 920000)
        return 'A'
    else if (score < 960000)
        return 'S'
    else
        return 'V'
}
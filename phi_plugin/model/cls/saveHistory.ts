import { Level } from "../constNum"
import LevelRecordInfo from "./LevelRecordInfo";
import Save from "./Save"
import { idString, levelKind } from "../type/type";
import { fCompute } from "..";

export default interface saveHistory {
    /**data货币变更记录 */
    data: { date: Date, value: number[] }[],
    /**rks变更记录 */
    rks: { date: Date, value: number }[],
    /**历史成绩 */
    scoreHistory: { [key: idString]: { [key in levelKind]?: [number, number, Date, boolean][] } },
    /**民间考核 */
    dan: any[],
    version: number
}

export default class saveHistory {

    /**
     * 
     * @param {saveHistory} data 
     */
    constructor(data: saveHistory) {

        for (let key in data?.data) {
            data.data[key].date = new Date(data.data[key].date)
        }
        this.data = data?.data || [];

        for (let key in data.rks) {
            data.rks[key].date = new Date(data.rks[key].date)
        }
        this.rks = data?.rks || [];

        this.scoreHistory = {}
        for (let key in data.scoreHistory) {
            let id = key.replace(/\.0$/, '')
            this.scoreHistory[id] = data.scoreHistory[key]
        }

        this.dan = data?.dan || [];
        /**v1.0,取消对当次更新内容的存储，取消对task的记录，更正scoreHistory */
        /**v1.1,更正scoreHistory */
        /**v1.2,由于曲名错误，删除所有记录，曲名使用id记录 */
        /**历史记录版本号 */
        this.version = data?.version

        /**检查版本 */
        if (!this.version || this.version < 2) {
            if (this.scoreHistory) {
                for (let i in this.scoreHistory) {
                    if (!i.includes('.0')) {
                        this.scoreHistory = {}
                    }
                    break
                }
            }
            this.version = 2
        }

    }

    /**
     * 合并记录
     * @param {saveHistory} data 另一个 History 存档
     */
    add(data: saveHistory) {
        this.data = merge(this.data, data.data)
        this.rks = merge(this.rks, data.rks)
        for (let song in data.scoreHistory) {
            if (!this.scoreHistory[song]) this.scoreHistory[song] = {}
            for (let dif in data.scoreHistory[song]) {
                if (this.scoreHistory[song] && this.scoreHistory[song][dif]) {
                    this.scoreHistory[song][dif] = this.scoreHistory[song][dif].concat(data.scoreHistory[song][dif])
                    this.scoreHistory[song][dif].sort((a, b) => {
                        return openHistory(a).date.getTime() - openHistory(b).date.getTime()
                    })
                } else {
                    this.scoreHistory[song][dif] = data.scoreHistory[song][dif]
                }
                let i = 1
                while (i < this.scoreHistory[song][dif].length) {
                    let last = openHistory(this.scoreHistory[song][dif][i - 1])
                    let now = openHistory(this.scoreHistory[song][dif][i])
                    if (last.score == now.score && last.acc == now.acc && last.fc == now.fc) {
                        // console.info(last.date.toISOString(), now.date.toISOString())
                        this.scoreHistory[song][dif].splice(i, 1)
                    } else {
                        ++i
                    }
                }
            }
        }
    }

    /**
     * 检查新存档中的变更并记录
     * @param {Save} save 新存档
     */
    update(save: Save) {
        // console.info(save)
        /**更新单曲成绩 */
        for (let id in save.gameRecord) {
            if (!this.scoreHistory[id]) this.scoreHistory[id] = {}
            for (let i in save.gameRecord[id]) {
                /**难度映射 */
                let level = Level[i]
                /**提取成绩 */
                let now: { score: number, acc: number, fc: boolean, date?: Date } = save.gameRecord[id][i]
                now.date = new Date(save.modifiedAt)
                /**本地无记录 */
                if (!this.scoreHistory[id][level] || !this.scoreHistory[id][level].length) {
                    this.scoreHistory[id][level] = [createHistory(now.acc, now.score, save.saveInfo.modifiedAt.iso, now.fc)];
                    continue
                }
                /**新存档该难度无成绩 */
                if (!save.gameRecord[id][i]) continue
                /**本地记录日期为递增 */
                for (let i = this.scoreHistory[id][level].length - 1; i >= 0; --i) {
                    /**第i项记录 */
                    let old = openHistory(this.scoreHistory[id][level][i])
                    // console.info(old.date.toISOString(), new Date(now.date).toISOString(), old.date.toISOString() == new Date(now.date).toISOString())
                    /**日期完全相同则认为已存储 */
                    if (old.score == now.score && old.acc == now.acc && old.fc == now.fc) {
                        /**标记已处理 */
                        now = null
                        break
                    }
                    /**找到第一个日期小于新成绩的日期 */
                    if (old.date < new Date(now.date)) {
                        /**历史记录acc仅保存4位，检查是否与第一个小于该日期的记录一致 */
                        if (old.acc.toString() != now.acc.toFixed(4) || old.score != now.score || old.fc != now.fc) {
                            /**不一致在第i项插入 */
                            this.scoreHistory[id][level].splice(i, 0, createHistory(now.acc, now.score, save.saveInfo.modifiedAt.iso, now.fc))
                        }
                        /**标记已处理 */
                        now = null
                        break
                    }
                }
                /**未被处理，有该难度记录，说明日期早于本地记录 */
                if (now) {
                    // console.info(11)
                    this.scoreHistory[id][level].unshift(createHistory(now.acc, now.score, save.saveInfo.modifiedAt.iso, now.fc))
                }
                /**查重 */
                let j = 1
                while (j < this.scoreHistory[id][level].length) {
                    let last = openHistory(this.scoreHistory[id][level][j - 1])
                    let now = openHistory(this.scoreHistory[id][level][j])
                    if (last.score == now.score && last.acc == now.acc && last.fc == now.fc) {
                        // console.info(last.date.toISOString(), now.date.toISOString())
                        this.scoreHistory[id][level].splice(j, 1)
                    } else {
                        ++j
                    }
                }
            }
        }
        /**更新rks记录 */
        for (let i = this.rks.length - 1; i >= 0; i--) {
            if (new Date(save.modifiedAt) > new Date(this.rks[i].date)) {
                if (!this.rks[i + 1] || (this.rks[i].value != save.saveInfo.summary.rankingScore || this.rks[i + 1]?.value != save.saveInfo.summary.rankingScore)) {
                    this.rks.splice(i + 1, 0, {
                        date: new Date(save.modifiedAt),
                        value: save.saveInfo.summary.rankingScore
                    })
                }
                break
            }
        }
        if (!this.rks.length) {
            this.rks.push({
                date: new Date(save.modifiedAt),
                value: save.saveInfo.summary.rankingScore
            })
        }
        /**更新data记录 */
        for (let i = this.data.length - 1; i >= 0; i--) {
            if (new Date(save.modifiedAt) > new Date(this.data[i].date)) {
                if (!this.data[i + 1] || (checkValue(this.data[i].value, save.gameProgress.money) && checkValue(this.data[i + 1]?.value, save.gameProgress.money))) {
                    this.data.splice(i + 1, 0, {
                        date: new Date(save.modifiedAt),
                        value: save.gameProgress.money
                    })
                }
                break
            }
        }
        if (!this.data.length) {
            this.data.push({
                date: new Date(save.modifiedAt),
                value: save.gameProgress.money
            })
        }

    }

    /**
     * 获取歌曲最新的历史记录
     * @param id 曲目id
     * @returns 
     */
    async getSongsLastRecord(id: idString) {
        let score = { ...this.scoreHistory[id] }
        let ans: { acc: number, score: number, date?: Date, fc: boolean }[] = []
        for (let i in score) {
            let level = Number(i)
            ans[level] = score[level] ? openHistory(score[level].at(-1)) : null
            if (!ans[level]) continue
            let date = ans[level].date
            ans[level] = new LevelRecordInfo(ans[level], id, level)
            ans[level].date = date
        }
        return ans
    }

    getRksAndDataLine() {

        let rks_history_ = []
        let data_history_ = []
        let user_rks_data = this.rks
        let user_data_data = this.data
        let rks_range = [17, 0]
        let data_range = [1e9, 0]
        let rks_date = [new Date(user_rks_data[0].date).getTime(), 0]
        let data_date = [new Date(user_data_data[0].date).getTime(), 0]

        for (let i in user_rks_data) {
            user_rks_data[i].date = new Date(user_rks_data[i].date)
            if (i as any <= 1 || user_rks_data[i].value != rks_history_[rks_history_.length - 2].value) {
                rks_history_.push(user_rks_data[i])
                rks_range[0] = Math.min(rks_range[0], user_rks_data[i].value)
                rks_range[1] = Math.max(rks_range[1], user_rks_data[i].value)
            } else {
                rks_history_[rks_history_.length - 1].date = user_rks_data[i].date
            }
            rks_date[1] = user_rks_data[i].date.getTime()
        }


        for (let i in user_data_data) {
            let value = user_data_data[i].value
            let valueNum = (((value[4] * 1024 + value[3]) * 1024 + value[2]) * 1024 + value[1]) * 1024 + value[0]
            user_data_data[i].date = new Date(user_data_data[i].date)
            if (i as any <= 1 || user_data_data[i].value != data_history_[data_history_.length - 2].value) {
                data_history_.push(user_data_data[i])
                data_range[0] = Math.min(data_range[0], valueNum)
                data_range[1] = Math.max(data_range[1], valueNum)
            } else {
                data_history_[data_history_.length - 1].date = user_data_data[i].date
            }
            data_date[1] = user_data_data[i].date.getTime()
        }

        let rks_history = []
        let data_history = []

        for (let i in rks_history_) {

            let ni = Number(i)

            if (!rks_history_[i + 1]) break
            let x1 = fCompute.percentage(rks_history_[ni].date, rks_date)
            let y1 = fCompute.percentage(rks_history_[ni].value, rks_range)
            let x2 = fCompute.percentage(rks_history_[ni + 1].date, rks_date)
            let y2 = fCompute.percentage(rks_history_[ni + 1].value, rks_range)
            rks_history.push([x1, y1, x2, y2])
        }

        for (let i in data_history_) {

            let ni = Number(i)

            if (!data_history_[ni + 1]) break
            let x1 = fCompute.percentage(data_history_[ni].date, data_date)
            let y1 = fCompute.percentage(data_history_[ni].value, data_range)
            let x2 = fCompute.percentage(data_history_[ni + 1].date, data_date)
            let y2 = fCompute.percentage(data_history_[ni + 1].value, data_range)
            data_history.push([x1, y1, x2, y2])
        }


        let unit = ["KiB", "MiB", "GiB", "TiB", "Pib"]

        for (let i in [1, 2, 3, 4]) {
            if (Math.floor(data_range[0] / (Math.pow(1024, Number(i)))) < 1024) {
                data_range[0] = `${Math.floor(data_range[0] / (Math.pow(1024, Number(i))))}${unit[i]}` as any
            }
        }

        for (let i in [1, 2, 3, 4]) {
            if (Math.floor(data_range[1] / (Math.pow(1024, Number(i)))) < 1024) {
                data_range[1] = `${Math.floor(data_range[1] / (Math.pow(1024, Number(i))))}${unit[i]}` as any
            }
        }

        return { rks_history, data_history, rks_range, data_range, rks_date, data_date }

    }

}

/**
 * 数组合并按照 date 排序并去重
 * @param m 
 * @param n 
 */
function merge(m: any[], n: any[]) {
    let t = m.concat(n)
    t.sort((a, b) => {
        return new Date(a.date).getTime() - new Date(b.date).getTime()
    })
    let i = 1
    while (i < t.length - 1) {
        /**因绘制折线图需要，需要保留同一值两端 */
        if (checkValue(t[i].value, t[i - 1].value) && checkValue(t[i].value, t[i + 1].value)) {
            t.splice(i, 1)
        } else {
            ++i
        }
    }
    return t
}
function createHistory(acc, score, date, fc) {
    return [acc.toFixed(4), score, date, fc]
}


/**
 * 展开信息
 * @param {Array} data 历史成绩
 */
function openHistory(data: any[]) {
    return {
        acc: Number(data[0]),
        score: Number(data[1]),
        date: new Date(data[2]),
        fc: Boolean(data[3])
    }
}

/**
 * 比较两个数组
 * @param {any} a 
 * @param {any} b 
 * @returns {boolean}
 */
function checkValue(a: any, b: any): boolean {
    /**非数组 */
    if (Object.prototype.toString.call(a) != '[object Array]') {
        return a == b
    }
    if (!a || !b) {
        return false
    }
    /**数组 */
    for (let i in a) {
        if (a[i] != b[i]) return false
    }
    return true
}

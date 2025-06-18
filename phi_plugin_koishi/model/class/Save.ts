import { logger } from '../../components/Logger'
import fCompute from '../fCompute'
import LevelRecordInfo from './LevelRecordInfo'
import getInfo from '../getInfo'
import PhigrosUser from '../../lib/PhigrosUser'
import { Level } from '../constNum'
import { idString } from '../type/type'

export default interface Save {
    sessionToken: string,
    /**存档上传时间 "2023-10-06T03:46:33.000Z" */
    modifiedAt: string,
    saveInfo: {
        /**账户创建时间 2022-09-03T10:21:48.613Z */
        createdAt: string,
        gameFile: {
            /**存档创建时间 2023-10-05T07:41:24.503Z */
            createdAt: string,
            /**gamesaves/{32}/.save */
            key: string,
            /**存档id {24} */
            objectId: string,
            /**存档更新时间 2023-10-05T07:41:24.503Z */
            updatedAt: string,
            /**https://rak3ffdi.tds1.tapfiles.cn/gamesaves/{32}/.save */
            url: string
        },
        /**存档上传时间 {__type："Date", "iso": "2023-10-06T03:46:33.000Z"} */
        modifiedAt: { "__type": "Date", "iso": string },
        /**用户id {24} 与 gameFile 中的不同 */
        objectId: string,
        summary: {
            /**插件获取存档时间 2023 Oct.06 11:46:33 */
            updatedAt: string,
            /**存档版本 */
            saveVersion: number,
            /**课题分 */
            challengeModeRank: number,
            /**rks */
            rankingScore: number,
            /**客户端版本号 */
            gameVersion: number,
            /**头像 */
            avatar: string,
            /**完成曲目数量 */
            cleared: [number, number, number, number],
            /**FC曲目数量 */
            fullCombo: [number, number, number, number],
            /**AP曲目数量 */
            phi: [number, number, number, number]
        },
        /**存档上传时间 2023 Oct.06 11:46:33 */
        updatedAt: string,
        /**用户信息 */
        user: { __type: "Pointer", className: "_User", objectId: string },
        /**用户名 */
        PlayerId: string
    },
    /**存档url */
    saveUrl: string,
    /**官方存档版本号 */
    Recordver: number,
    gameProgress: {
        /**首次运行 */
        isFirstRun: boolean,
        /**过去的章节已完成 */
        legacyChapterFinished: boolean,
        /**已展示收藏品Tip */
        alreadyShowCollectionTip: boolean,
        /**已展示自动解锁IN Tip */
        alreadyShowAutoUnlockINTip: boolean,
        /**剧情完成(显示全部歌曲和课题模式入口) */
        completed: string,
        /**？？？ */
        songUpdateInfo: number,
        /**课题分 */
        challengeModeRank: number,
        /**data货币 */
        money: number[],
        /**痉挛解锁 */
        unlockFlagOfSpasmodic: number,
        /**Igallta解锁 */
        unlockFlagOfIgallta: number,
        /**Rrhar'il解锁 */
        unlockFlagOfRrharil: number,
        /**IN达到S(倒霉蛋,船,Shadow,心之所向,inferior,DESTRUCTION 3,2,1,Distorted Fate) */
        flagOfSongRecordKey: number,
        /**Random切片解锁 */
        randomVersionUnlocked: number,
        /**第八章入场 */
        chapter8UnlockBegin: boolean,
        /**第八章第二阶段 */
        chapter8UnlockSecondPhase: boolean,
        /**第八章通过 */
        chapter8Passed: boolean,
        /**第八章各曲目解锁 */
        chapter8SongUnlocked: number
    },
    gameuser?: {
        /**user */
        name: string,
        /**版本 */
        version: number,
        /**是否展示Id */
        showPlayerId: boolean,
        /**简介 */
        selfIntro: string,
        /**头像 */
        avatar: string,
        /**背景 */
        background: string,
    },
    gameRecord?: { [key: idString]: LevelRecordInfo[] }
}

export default class Save {

    /**
     * @param {Save} data 
     * @param {boolean} ignore 跳过存档检查
     */
    constructor(data: Save | PhigrosUser, ignore: boolean = false) {
        this.sessionToken = data.sessionToken || (data as any).session
        this.modifiedAt = data.saveInfo.modifiedAt.iso
        this.saveInfo = data.saveInfo
        this.saveUrl = data.saveUrl + ''
        this.Recordver = data.Recordver
        this.gameProgress = data.gameProgress
        this.gameuser = data.gameuser
        this.gameRecord = {}
        for (let id in data.gameRecord) {
            let nid = id.replace(/\.0$/, '') as idString
            this.gameRecord[nid] = []
            for (let i in data.gameRecord[id]) {
                let level = Number(i)
                if (!data.gameRecord[id][level]) {
                    this.gameRecord[nid][level] = null
                    continue
                }
                this.gameRecord[nid][level] = new LevelRecordInfo(data.gameRecord[id][level], nid, level)
                if (ignore) continue
                if (data.gameRecord[id][level].acc > 100) {
                    logger.error(`acc > 100 ${this.sessionToken}`)
                }
            }
        }
    }

    /**按照 rks 排序的数组 */
    sortedRecord: LevelRecordInfo[]

    /**
     * 获取存档
     * @returns 按照 rks 排序的数组W
     */
    getRecord() {
        if (this.sortedRecord) {
            return this.sortedRecord
        }
        let sortedRecord = []
        for (let id in this.gameRecord) {
            for (let level in this.gameRecord[id]) {
                if (Number(level) == 4) break
                let tem = this.gameRecord[id][level]
                if (!tem?.score) continue
                sortedRecord.push(tem)
            }
        }

        sortedRecord.sort((a, b) => { return b.rks - a.rks })
        this.sortedRecord = sortedRecord
        return sortedRecord
    }

    /**
     * 筛选满足ACC条件的成绩
     * @param {number} acc ≥acc
     * @param {boolean} [same=false] 是否筛选最高rks
     * @returns 按照rks排序的数组
     */
    findAccRecord(acc: number, same: boolean = false):LevelRecordInfo[] {
        let record = []
        for (let id in this.gameRecord) {
            for (let level in this.gameRecord[id]) {
                /**LEGACY */
                if (Number(level) == 4) break
                let tem = this.gameRecord[id][level]
                if (!tem) continue
                if (tem.acc >= acc) {
                    record.push(tem)
                }
            }
        }
        record.sort((a, b) => { return b.rks - a.rks })
        if (same) {
            for (let i = 0; i < record.length - 1; i++) {
                if (record[i].rks != record[i + 1]?.rks) {
                    return record.slice(0, i + 1)
                }
            }
        }
        return record
    }

    /**计算rks+0.01的最低所需要提升的rks */
    minUpRks() {
        /**考虑屁股肉四舍五入原则 */
        let minuprks = Math.floor(this.saveInfo.summary.rankingScore * 100) / 100 + 0.005 - this.saveInfo.summary.rankingScore
        return minuprks < 0 ? minuprks + 0.01 : minuprks
    }

    /**简单检查存档是否存在问题 */
    checkRecord() {
        let error = ``
        const Level = ['EZ', 'HD', 'IN', 'AT', 'LEGACY']
        for (let i in this.gameRecord) {
            for (let j in this.gameRecord[i]) {
                let score = this.gameRecord[i][j]
                if (score.acc > 100 || score.acc < 0 || score.score > 1000000 || score.score < 0) {
                    error += `\n${i} ${Level[j]} ${score.fc} ${score.acc} ${score.score} 非法的成绩`
                }
                // if (!score.fc && (score.score >= 1000000 || score.acc >= 100)) {
                //     error += `\n${i} ${Level[j]} ${score.fc} ${score.acc} ${score.score} 不符合预期的值`
                // }
                if ((score.score >= 1000000 && score.acc < 100) || (score.score < 1000000 && score.acc >= 100)) {
                    error += `\n${i} ${Level[j]} ${score.fc} ${score.acc} ${score.score} 成绩不自洽`
                }
            }
        }
        return error
    }

    /**
     * 
     * @param {string} id 曲目id
     */
    getSongsRecord(id: string): LevelRecordInfo[] {
        if (!this.gameRecord[id]) {
            return []
        }
        return [...this.gameRecord[id]]
    }

    /**phi 和 b19 */
    B19List: { phi: LevelRecordInfo[], b19_list: LevelRecordInfo[], com_rks: number }
    /**b0 rks */
    b0_rks: number
    /**b19 rks */
    b19_rks: number

    /**
     * 
     * @param {number} num B几
     * @returns phi, b19_list
     */
    async getB19(num: number) {
        if (this.B19List) {
            return this.B19List
        }
        /**计算得到的rks，仅作为测试使用 */
        let sum_rks = 0
        /**满分且 rks 最高的成绩数组 */
        let philist = this.findAccRecord(100)
        /**p3 */
        let phi = philist.splice(0, Math.min(philist.length, 3))

        // console.info(phi)
        /**处理数据 */


        for (let i = 0; i < 3; ++i) {
            if (!phi[i]) {
                phi[i] = false as any
                continue
            }
            if (phi[i]?.rks) {
                let tem = {} as any
                Object.assign(tem, phi[i])
                phi[i] = tem
                sum_rks += Number(phi[i].rks) //计算rks
                phi[i].illustration = getInfo.getill(phi[i].id)
                phi[i].suggest = "无法推分"
            }
        }

        /**所有成绩 */
        let rkslist = this.getRecord()
        /**真实 rks */
        let userrks = this.saveInfo.summary.rankingScore
        /**考虑屁股肉四舍五入原则的最小上升rks */
        let minuprks = Math.floor(userrks * 100) / 100 + 0.005 - userrks
        if (minuprks < 0) {
            minuprks += 0.01
        }

        /**bestN 列表 */
        let b19_list = []
        for (let i = 0; i < num && i < rkslist.length; ++i) {
            /**计算rks */
            if (i < 27) sum_rks += Number(rkslist[i].rks)
            /**是 Best 几 */
            rkslist[i].num = i + 1
            /**推分建议 */
            if (rkslist[i].rks < 100) {
                rkslist[i].suggest = fCompute.suggest(Number((i < 26) ? rkslist[i].rks : rkslist[26].rks) + minuprks * 30, rkslist[i].difficulty, 2)
                if (rkslist[i].suggest.includes('无') && (!phi?.[0] || (rkslist[i].rks > phi[phi.length - 1].rks)) && rkslist[i].rks < 100) {
                    rkslist[i].suggest = "100.00%"
                }
            } else {
                rkslist[i].suggest = "无法推分"
            }
            /**曲绘 */
            rkslist[i].illustration = getInfo.getill(rkslist[i].id, 'common')
            /**b19列表 */
            b19_list.push(rkslist[i])
            if (!rkslist[i].rks) {
                console.info(rkslist[i])
            }
        }

        let com_rks = sum_rks / 30

        this.B19List = { phi, b19_list, com_rks }
        this.b19_rks = b19_list[Math.min(b19_list.length - 1, 26)].rks
        return { phi, b19_list, com_rks }
    }

    /**
     * 
     * @param {string} id 
     * @param {number} lv 
     * @param {number} count 保留位数
     * @param {number} difficulty 
     * @returns 
     */
    getSuggest(id: idString, lv: number, count: number) {
        let difficulty = getInfo.info(id).chart[Level[lv]].difficulty
        if (!this.b19_rks) {
            let record = this.getRecord()
            this.b19_rks = record.length > 26 ? record[26].rks : 0
            this.b0_rks = this.findAccRecord(100, true)[0]?.rks || 0
        }
        // console.info(this.b19_rks, this.gameRecord[id][lv]?.rks ? this.gameRecord[id][lv].rks : 0, this.gameRecord[id])
        let suggest = fCompute.suggest(Math.max(this.b19_rks, this.gameRecord[id][lv]?.rks ? this.gameRecord[id][lv].rks : 0) + this.minUpRks() * 30, difficulty, count) + ''
        return suggest.includes('无') ? (difficulty > this.b0_rks ? Number(100).toFixed(count) + '%' : suggest) : suggest
    }

    /**
     * 获取存档RKS
     * @returns {number}
     */
    getRks(): number {
        return Number(this.saveInfo.summary.rankingScore)
    }

    /**
     * 获取存档sessionToken
     */
    getSessionToken(): string {
        return this.sessionToken
    }
    
    /**
     * 获取存档成绩总览
     * @returns 
     */
    async getStats() {
        /**'EZ', 'HD', 'IN', 'AT' */
        let tot = [0, 0, 0, 0]
        
        let Record = this.gameRecord
        let Level = getInfo.Level

        let stats_ = {
            title: '',
            Rating: '',
            unlock: 0,
            tot: 0,
            cleared: 0,
            fc: 0,
            phi: 0,
            real_score: 0,
            tot_score: 0,
            highest: 0,
            lowest: 18,
        }

        let stats = [{ ...stats_ }, { ...stats_ }, { ...stats_ }, { ...stats_ }]

        for (let song in getInfo.ori_info) {
            let info = getInfo.ori_info[song]
            if (info.chart['AT'] && Number(info.chart['AT'].difficulty)) {
                ++tot[3]
            }
            if (info.chart['IN'] && Number(info.chart['IN'].difficulty)) {
                ++tot[2]
            }
            if (info.chart['HD'] && Number(info.chart['HD'].difficulty)) {
                ++tot[1]
            }
            if (info.chart['EZ'] && Number(info.chart['EZ'].difficulty)) {
                ++tot[0]
            }
        }

        stats[0].tot = tot[0]
        stats[0].title = Level[0]

        stats[1].tot = tot[1]
        stats[1].title = Level[1]

        stats[2].tot = tot[2]
        stats[2].title = Level[2]

        stats[3].tot = tot[3]
        stats[3].title = Level[3]

        for (let id in Record) {
            if (!getInfo.idgetsong(id as any)) {
                continue
            }
            let record = Record[id]
            for (let lv in [0, 1, 2, 3]) {
                if (!record[lv]) continue

                ++stats[lv].unlock

                if (record[lv].score >= 700000) {
                    ++stats[lv].cleared
                }
                if (record[lv].fc || record[lv].score == 1000000) {
                    ++stats[lv].fc
                }
                if (record[lv].score == 1000000) {
                    ++stats[lv].phi
                }


                stats[lv].real_score += record[lv].score
                stats[lv].tot_score += 1000000

                stats[lv].highest = Math.max(record[lv].rks, stats[lv].highest)
                stats[lv].lowest = Math.min(record[lv].rks, stats[lv].lowest)
            }
        }

        for (let lv in [0, 1, 2, 3]) {
            stats[lv].Rating = fCompute.rate(stats[lv].real_score, stats[lv].tot_score, stats[lv].fc == stats[lv].unlock)
            if (stats[lv].lowest == 18) {
                stats[lv].lowest = 0
            }
        }

        return stats
    }
}

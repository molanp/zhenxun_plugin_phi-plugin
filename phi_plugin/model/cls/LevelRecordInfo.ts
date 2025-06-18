import fCompute from '../fCompute';
import getInfo from '../getInfo';
import { idString } from '../type/type';

export default interface LevelRecordInfo {
    id: idString
    fc: boolean
    score: number
    acc: number
    rank: string
    song: string
    illustration: string
    Rating: string
    difficulty: number
    rks: number
    suggest?: string
}

export default class LevelRecordInfo {


    /**
     * @param data 原始数据
     * @param id 曲目id
     * @param rank 难度
     */
    constructor(data: { fc: boolean; score: number; acc: number; }, id: idString, rank: number) {


        this.fc = data.fc;
        this.score = data.score;
        this.acc = data.acc;
        this.id = id as idString

        let info = getInfo.info(id)

        if (!info) {
            return
        }

        this.rank = getInfo.Level[rank] //AT IN HD EZ LEGACY 
        this.song = info.song //曲名
        this.illustration = getInfo.getill(id) //曲绘链接
        this.Rating = Rating(this.score, this.fc) //V S A 


        if (info.chart && info.chart[this.rank]?.difficulty) {
            this.difficulty = Number(info.chart[this.rank]['difficulty']) //难度
            this.rks = fCompute.rks(this.acc, this.difficulty) //等效rks
        } else {
            this.difficulty = 0
            this.rks = 0
        }


    }
}

function Rating(score, fc) {
    if (score >= 1000000)
        return 'phi'
    else if (fc)
        return 'FC'
    else if (!score)
        return 'NEW'
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

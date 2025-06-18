import LevelRecord from './LevelRecord'
import ByteReader from './ByteReader';
import Util from './Util'
import getInfo from '../model/getInfo'
import { idString } from '../model/type/type';

export default interface GameRecord {
    name: string;
    version: number;
    data: ByteReader;
    Record: any;
    songsnum: number;
    init(err: Array<string>): any;
}

export default class GameRecord {
    static name = "gameRecord";
    static version = 1;
    constructor(data: string) {
        this.name = "gameRecord";
        this.version = 1;
        this.data = new ByteReader(data)
        this.Record = {}
        this.songsnum = 0
    }

    /**
     * 
     * @param {Array} err 错误消息
     */
    async init(err: string[]) {
        this.songsnum = this.data.getVarInt()
        while (this.data.remaining() > 0) {
            let key = this.data.getString().replace(/\.0$/, '') as idString;
            this.data.skipVarInt()
            let length = this.data.getByte();
            let fc = this.data.getByte();
            let song = [];


            for (let level = 0; level < 5; level++) {
                if (Util.getBit(length, level)) {
                    song[level] = new LevelRecord();
                    song[level].score = this.data.getInt();
                    song[level].acc = this.data.getFloat();
                    song[level].fc = (song[level].score == 1000000 && song[level].acc == 100) ? true : Util.getBit(fc, level);

                }
            }
            if (!getInfo.idgetsong(key)) {
                err.push(key)
            }
            this.Record[key] = song
        }
    }
}




import ByteReader from './ByteReader';
import Util from './Util'

export default interface GameProgress {
    isFirstRun: boolean;
    legacyChapterFinished: boolean;
    alreadyShowCollectionTip: boolean;
    alreadyShowAutoUnlockINTip: boolean;
    completed: string;
    songUpdateInfo: number;
    challengeModeRank: number;
    money: number[];
    unlockFlagOfSpasmodic: number;
    unlockFlagOfIgallta: number;
    unlockFlagOfRrharil: number;
    flagOfSongRecordKey: number;
    randomVersionUnlocked: number;
    chapter8UnlockBegin: boolean;
    chapter8UnlockSecondPhase: boolean;
    chapter8Passed: boolean;
    chapter8SongUnlocked: number;
}

export default class GameProgress {
    constructor(data: any) {
        let Reader = new ByteReader(data)
        let tem = Reader.getByte()
        this.isFirstRun = Util.getBit(tem, 0)
        this.legacyChapterFinished = Util.getBit(tem, 1)
        this.alreadyShowCollectionTip = Util.getBit(tem, 2)
        this.alreadyShowAutoUnlockINTip = Util.getBit(tem, 3)
        this.completed = Reader.getString()
        this.songUpdateInfo = Reader.getVarInt()
        this.challengeModeRank = Reader.getShort()
        this.money = [0, 0, 0, 0, 0];
        this.money[0] = Reader.getVarInt()
        this.money[1] = Reader.getVarInt()
        this.money[2] = Reader.getVarInt()
        this.money[3] = Reader.getVarInt()
        this.money[4] = Reader.getVarInt()
        this.unlockFlagOfSpasmodic = Reader.getByte()
        this.unlockFlagOfIgallta = Reader.getByte()
        this.unlockFlagOfRrharil = Reader.getByte()
        this.flagOfSongRecordKey = Reader.getByte()
        this.randomVersionUnlocked = Reader.getByte()
        tem = Reader.getByte()
        this.chapter8UnlockBegin = Util.getBit(tem, 0)
        this.chapter8UnlockSecondPhase = Util.getBit(tem, 1)
        this.chapter8Passed = Util.getBit(tem, 2)
        this.chapter8SongUnlocked = Reader.getByte()
    }
}

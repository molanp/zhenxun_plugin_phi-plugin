import ByteReader from './ByteReader';
import Util from './Util';

export default interface GameUser {
    name: string;
    version: number;
    showPlayerId: boolean;
    selfIntro: string;
    avatar: string;
    background: string;
}

export default class GameUser {
    constructor(data: string) {
        this.name = "user";
        this.version = 1;
        let Reader = new ByteReader(data)
        this.showPlayerId = Util.getBit(Reader.getByte(), 0);
        this.selfIntro = Reader.getString();
        this.avatar = Reader.getString();
        this.background = Reader.getString();
    }
}
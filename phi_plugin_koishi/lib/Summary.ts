// Assuming ByteReader is a class defined elsewhere
// Assuming Instant is a class imported from date-fns
// Assuming Base64 is an object imported from js-base64
import ByteReader from './ByteReader'
import Base64 from './Base64';


interface Summary {
    updatedAt: string;
    saveVersion: number;
    challengeModeRank: number;
    rankingScore: number;
    gameVersion: number;
    avatar: string;
    cleared: number[];
    fullCombo: number[];
    phi: number[];
}

class Summary {
    constructor(summary) {
        let now = Date().toString()
        let time = now.split(' ')
        this.updatedAt = `${time[3]} ${time[1]}.${time[2]} ${time[4]}`
        this.saveVersion = 0;
        this.challengeModeRank = 0;
        this.rankingScore = 0;
        this.gameVersion = 0;
        this.avatar = '';

        this.cleared = [];
        this.fullCombo = [];
        this.phi = [];

        const reader = new ByteReader(Base64.decode(summary));
        this.saveVersion = reader.getByte();
        this.challengeModeRank = reader.getShort();
        this.rankingScore = reader.getFloat();
        this.gameVersion = reader.getByte();
        this.avatar = reader.getString();
        this.cleared = [];
        this.fullCombo = [];
        this.phi = [];
        for (let level = 0; level < 4; level++) {
            this.cleared[level] = reader.getShort();
            this.fullCombo[level] = reader.getShort();
            this.phi[level] = reader.getShort();
        }
    }
}

export default Summary;
import { idString } from "../type/type";

export default class Chart {

    id?: idString;
    rank?: string;
    charter: string;
    difficulty: number;
    tap: number;
    drag: number;
    hold: number;
    flicke: number;
    combo: number;

    constructor(data: any) {
        this.id = data?.id
        this.rank = data?.rank
        this.charter = data.charter
        this.difficulty = Number(data.difficulty)
        this.tap = Number(data.tap)
        this.drag = Number(data.drag)
        this.hold = Number(data.hold)
        this.flicke = Number(data.flicke)
        this.combo = Number(data.combo)
    }
}
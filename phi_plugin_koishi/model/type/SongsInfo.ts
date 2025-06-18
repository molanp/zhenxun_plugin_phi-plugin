import { idString, songString } from "./type"
import Chart from "../class/Chart"


export default interface SongsInfo {
    id: idString
    song: songString
    illustration: string
    illustration_big: string
    can_t_be_letter: boolean
    can_t_be_guessill: boolean
    chapter: string
    bpm: string
    composer: string
    length: string
    illustrator: string
    spinfo: string
    chart: { [key: string]: Chart }
}
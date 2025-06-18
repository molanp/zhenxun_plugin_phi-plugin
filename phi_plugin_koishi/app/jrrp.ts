import { Context } from "koishi";
import { Config } from "..";
import { fCompute, getFile, getInfo, render, send } from "../model";
import { infoPath } from "../components/pluginPath";
import path from "path";
import { redis } from "../components/redis";
import { idString } from "../model/type/type";

/**一言 */
let sentence = getFile.FileReader(path.join(infoPath, 'sentences.json'))


export default class phiJrrp {
    constructor(ctx: Context, config: Config) {
        ctx.command('phi.jrrp', '今日人品').action(async ({ session }) => {

            if (await send.isBan(session, 'jrrp')) {
                return;
            }


            let jrrp: any[] = (await redis.get('phigrosJrrp', { userId: session.userId }, ['value']))[0]?.value as any

            jrrp = jrrp ? JSON.parse(jrrp as any) : null


            if (!jrrp || is_not_same_day(jrrp[10], Date.now())) {
                jrrp = [Math.round(easeOutCubic(Math.random()) * 100), Math.floor(Math.random() * sentence.length)]
                let good = [...getInfo.word.good]
                let bad = [...getInfo.word.bad]
                let common = [...getInfo.word.common]
                for (let i = 0; i < 4; i++) {
                    let id = Math.floor(Math.random() * (good.length + common.length))
                    if (id < good.length) {
                        jrrp.push(good[id])
                        good.splice(id, 1)
                    } else {
                        jrrp.push(common[id - good.length])
                        common.splice(id - good.length, 1)
                    }
                }
                for (let i = 0; i < 4; i++) {
                    let id = Math.floor(Math.random() * (bad.length + common.length))
                    if (id < bad.length) {
                        jrrp.push(bad[id])
                        bad.splice(id, 1)
                    } else {
                        jrrp.push(common[id - bad.length])
                        common.splice(id - bad.length, 1)
                    }
                }
                /**记录现在时间，有效期为当天 */
                jrrp.push(fCompute.date_to_string(Date.now()))

                await redis.upsert('phigrosJrrp', [{ userId: session.userId, value: JSON.stringify(jrrp) }], 'userId')
            }
            let data = {
                bkg: getInfo.getill("ShineAfter.ADeanJocularACE" as idString),
                lucky: jrrp[0],
                luckRank: jrrp[0] == 100 ? 5 : (jrrp[0] >= 80 ? 4 : (jrrp[0] >= 60 ? 3 : (jrrp[0] >= 40 ? 2 : (jrrp[0] >= 20 ? 1 : 0)))),
                year: new Date().getFullYear(),
                month: fCompute.ped(new Date().getMonth() + 1, 2),
                day: fCompute.ped(new Date().getDate(), 2),
                sentence: sentence[jrrp[1]],
                good: jrrp.slice(2, 6),
                bad: jrrp.slice(6, 10),
            }
            send.send_with_At(session, await render(ctx, 'jrrp', data))
        })
    }
}

/**
 * 
 * @param {number} x 
 * @returns {number}
 */
function easeOutCubic(x: number): number {
    return 1 - Math.pow(1 - x, 3);
}


function is_not_same_day(date1: any, date2: any): boolean {
    let d1 = new Date(date1)
    let d2 = new Date(date2)
    return d1.getFullYear() != d2.getFullYear() || d1.getMonth() != d2.getMonth() || d1.getDate() != d2.getDate()
}
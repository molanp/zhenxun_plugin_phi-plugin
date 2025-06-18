import { Context } from "koishi";

let Logger: Context['logger']

export class logger {
    static info(...msg: any[]) {
        Logger.info(msg.join('\n'))
    }
    static error(...msg: any[]) {
        Logger.error(msg.join('\n'))
    }
    static warn(...msg: any[]) {
        Logger.warn(msg.join('\n'))
    }
}

export function apply(ctx: Context) {
    Logger = ctx.logger
}
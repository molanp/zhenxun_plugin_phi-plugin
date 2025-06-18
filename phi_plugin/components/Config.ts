import { Context } from "koishi"
import { Config } from ".."

export let config: Config

export function apply(ctx: Context, cfg: Config) {
    config = cfg
}
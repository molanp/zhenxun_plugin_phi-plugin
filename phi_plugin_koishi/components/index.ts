import { Context } from 'koishi'
import Version from './Version'
import { Config } from '..'
import * as pluginPath from './pluginPath'
import * as logger from './Logger'
import * as config from './Config'
import * as redis from './redis'
import * as i18n from './i18n'


const Display_Plugin_Name = 'Phi-Plugin'
const Plugin_Name = 'phi-plugin'


export { Version, Plugin_Name, Display_Plugin_Name }


export function apply(ctx: Context, cfg: Config) {
    ctx.plugin(logger)
    ctx.plugin(config, cfg)
    ctx.plugin(pluginPath)
    ctx.plugin(redis)
    ctx.plugin(i18n)
}
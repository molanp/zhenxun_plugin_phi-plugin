import { Context } from "koishi"
import { Config } from ".."
import { fCompute, getBackup, send } from "../model"
import fs from "fs"
import { backupPath } from "../components/pluginPath"
import path from "path"
import { redis } from "../components/redis"
import { logger } from "../components/Logger"

let banSetting = ["help", "bind", "b19", "wb19", "song", "ranklist", "fnc", "tipgame", "guessgame", "ltrgame", "sign", "setting", "dan"]

export default class phiManage {
    constructor(ctx: Context, config: Config) {
        ctx.command('phi.backup', '备份数据', { authority: 4 }).option('back', '-b 是否返回zip文件').action(async ({ session, options }) => {
            try {
                let zip = await getBackup.backup()
                send.send_with_At(session, `${zip.zipName.replace(".zip", '')} 成功备份到 ./backup 目录下`)
                if (options.back) {
                    fCompute.sendFile(session, await zip.zip.generateAsync({ type: 'nodebuffer' }), zip.zipName)
                }
            } catch (err) {
                logger.error(err)
                send.send_with_At(session, err)
            }
        })

        ctx.command('phi.restore', '恢复数据', { authority: 4 }).action(async ({ session, options }) => {
            try {
                let msg = ''
                for (let i in fs.readdirSync(backupPath)) {
                    msg += `[${i}]${fs.readdirSync(backupPath).reverse()[i]}\n`
                }
                send.send_with_At(session, '请选择需要恢复的备份文件：\n' + msg)
                let index = await session.prompt(30000)
                try {
                    let fileName = fs.readdirSync(backupPath).reverse()[Number(index.replace(/\s*/g, ''))]
                    let filePath = path.join(backupPath, fileName)
                    await getBackup.restore(filePath)
                    send.send_with_At(session, `[${index}] ${fs.readdirSync(backupPath).reverse()[index.replace(/\s*/g, '')]} 恢复成功`)
                } catch (err) {
                    logger.info(err)
                    send.send_with_At(session, [`第[${index}]项不存在QAQ！`, err])
                }
            } catch (err) {
                logger.info(err)
                send.send_with_At(session, err)
            }
        })

        ctx.command('phi.ban <string>', '禁用功能', { authority: 4 }).action(async ({ session }, arg) => {
            if (!session.guildId) {
                send.send_with_At(session, '请在群聊中使用嗷！')
                return;
            }

            switch (arg) {
                case 'all': {
                    for (let i in banSetting) {
                        await redis.upsert('phigrosBanGroup', [{ groupId: session.guildId, [banSetting[i]]: true }], 'groupId');
                    }
                    break
                }
                default: {
                    for (let i in banSetting) {
                        if (banSetting[i] == arg) {
                            await redis.upsert('phigrosBanGroup', [{ groupId: session.guildId, [banSetting[i]]: true }], 'groupId');
                            break
                        }
                    }
                    break
                }
            }
            // console.info(await redis.keys(`${redisPath}:banGroup:*`))

            let res = (await redis.get('phigrosBanGroup', { groupId: session.guildId }))[0];
            let resMsg = ''
            if (res) {
                for (let i in banSetting) {
                    if (res[banSetting[i]]) {
                        resMsg += `${banSetting[i]}\n`
                    }
                }
            }

            send.send_with_At(session, `当前: ${session.guildId}\n已禁用:\n${resMsg}`)
        })

        ctx.command('phi.unban <string>', '解禁功能', { authority: 4 }).action(async ({ session }, arg) => {
            if (!session.guildId) {
                send.send_with_At(session, '请在群聊中使用嗷！')
                return;
            }

            switch (arg) {
                case 'all': {
                    for (let i in banSetting) {
                        await redis.upsert('phigrosBanGroup', [{ groupId: session.guildId, [banSetting[i]]: false }], 'groupId');
                    }
                    break
                }
                default: {
                    for (let i in banSetting) {
                        if (banSetting[i] == arg) {
                            await redis.upsert('phigrosBanGroup', [{ groupId: session.guildId, [banSetting[i]]: false }], 'groupId');
                            break
                        }
                    }
                    break
                }
            }
            // console.info(await redis.keys(`${redisPath}:banGroup:*`))

            let res = (await redis.get('phigrosBanGroup', { groupId: session.guildId }))[0];
            let resMsg = ''
            if (res) {
                for (let i in banSetting) {
                    if (res[banSetting[i]]) {
                        resMsg += `${banSetting[i]}\n`
                    }
                }
            }

            send.send_with_At(session, `当前: ${session.guildId}\n已禁用:\n${resMsg}`)
        })
    }
}
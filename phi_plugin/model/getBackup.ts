import JSZip from "jszip";
import fs from 'node:fs';
import path from "node:path";
import getFile from "./getFile";
import { backupPath, pluginDataPath, savePath } from "../components/pluginPath";
import { logger } from "../components/Logger";
import saveHistory from "./class/saveHistory";
import { redis } from "../components/redis";
import Save from "./class/Save";

export default class getBackup {

    /**备份 */
    static async backup() {
        let zip = new JSZip()
        /**data目录下存档 */
        fs.readdirSync(savePath).forEach((folderName) => {
            let folderPath = path.join(savePath, folderName)
            fs.readdirSync(folderPath).forEach((fileName) => { //遍历检测目录中的文件
                let filePath = path.join(folderPath, fileName);
                let file = fs.statSync(filePath); //获取一个文件
                if (file.isDirectory()) {
                    logger.error(filePath, '[phi-plugin] 备份错误：意料之外的文件夹');
                } else {
                    zip.folder('saveData').folder(folderName).file(fileName, fs.readFileSync(filePath)); //压缩目录添加文件
                }
            });
        });
        /**data目录下plugin数据 */
        fs.readdirSync(pluginDataPath).forEach((fileName) => { //遍历检测目录中的文件
            let filePath = path.join(pluginDataPath, fileName);
            let file = fs.statSync(filePath); //获取一个文件
            if (file.isDirectory()) {
                logger.error(filePath, '[phi-plugin] 备份错误：意料之外的文件夹');
            } else {
                zip.folder('pluginData').file(fileName, fs.readFileSync(filePath)); //压缩目录添加文件
            }
        });
        /**提取redis中user_id数据 */
        let user_token = {}
        let keys = await redis.get('phigrosUserToken', {})
        for (let key of keys) {
            let user_id = key.userId
            user_token[user_id] = key.token
        }
        // console.info(user_token)
        zip.file('user_token.json', JSON.stringify(user_token))
        /**压缩 */
        let zipName = `${(new Date()).toISOString().replace(/[\:\.]/g, '-')}.zip`
        if (!fs.existsSync(backupPath)) {
            // 递归创建目录
            fs.mkdirSync(backupPath, { recursive: true });
        }
        fs.writeFileSync(path.join(backupPath, zipName), await zip.generateAsync({
            type: 'nodebuffer',
            /**压缩算法 */
            compression: "DEFLATE",
            /**压缩等级 */
            compressionOptions: {
                level: 9
            }
        }));
        logger.info(path.join(backupPath, zipName), '[phi-plugin]备份完成')
        return { zipName: zipName, zip: zip }
    }

    /**
     * 从zip中恢复
     * @param {path} zipPath 
     */
    static async restore(zipPath: string) {
        let zip = await JSZip.loadAsync(fs.readFileSync(zipPath))
        try {
            /**存档相关 */
            zip.folder('saveData').forEach((session) => {
                /**阻止遍历文件夹 */
                if (!session.includes('.json')) {
                    /**history */
                    let oldHistory = getFile.FileReader(path.join(savePath, session, 'history.json'))
                    zip.folder('saveData').folder(session).file('history.json').async('string').then((history) => {
                        /**格式化为 JSON */
                        let now = new saveHistory(JSON.parse(history))
                        /**有本地记录，合并；无本地记录，直接覆盖 */
                        now.add(new saveHistory(oldHistory))
                        getFile.SetFile(path.join(savePath, session, 'history.json'), now)
                    })

                    /**save */
                    let oldSave = getFile.FileReader(path.join(savePath, session, 'save.json'))
                    zip.folder('saveData').folder(session).file('save.json').async('string').then((save: string) => {
                        /**格式化为 JSON */
                        let now: Save = new Save(JSON.parse(save))
                        /**有本地记录，保留最新记录；无本地记录，直接覆盖 */
                        if (oldSave?.saveInfo?.modifiedAt?.iso && new Date(oldSave?.saveInfo?.modifiedAt?.iso) > new Date(now?.saveInfo?.modifiedAt?.iso)) { now = oldSave }
                        getFile.SetFile(path.join(savePath, session, 'save.json'), now)

                    })
                }

            });
        } catch (e) {
            logger.error(e)
        }
        try {
            /**插件数据相关 */
            zip.folder('pluginData').forEach((fileName, file) => {
                file.async('string').then((data) => {
                    getFile.SetFile(path.join(pluginDataPath, fileName), JSON.parse(data))
                })
            })
        } catch (e) {
            logger.error(e)
        }
        try {
            /**user_id->tk */
            zip.file('user_token.json').async('string').then((data) => {
                let now: { [key: string]: string } = JSON.parse(data)
                for (let key in now) {
                    redis.upsert('phigrosUserToken', [{ userId: key, token: now[key] }], 'userId')
                }
            })
        } catch (e) {
            logger.error(e)
        }
    }
}
import getFile from './getFile'
import path from 'path'
import { pluginDataPath } from '../components/pluginPath'
import pluginData from './class/pluginData'
export default class getPluginData {

    /**
     * 获取并初始化用户数据
     * @param {string} user_id 
     * @returns {{plugin_data:{money:number,sign_in:string,task_time:string,task:Array<object>,theme:string}}}
     */
    static get(user_id: string): pluginData {
        let data = getFile.FileReader(path.join(pluginDataPath, `${user_id}_.json`))
        if (!data || !data.plugin_data) {
            data = {
                plugin_data: {
                    money: 0,
                    sign_in: "Wed Apr 03 2024 23:03:52 GMT+0800 (中国标准时间)",
                    task_time: "Wed Apr 03 2024 23:03:52 GMT+0800 (中国标准时间)",
                    task: [],
                    theme: "star"
                }
            }
        }
        return data
    }

    static async put(user_id: string, data: any) {
        return getFile.SetFile(path.join(pluginDataPath, `${user_id}_.json`), data)
    }

    static async del(user_id: string) {
        return getFile.DelFile(path.join(pluginDataPath, `${user_id}_.json`))
    }

}

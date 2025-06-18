import get from "./getdata";

export default new class money {
    async getNoteNum(user_id) {
        return (await get.getpluginData(user_id))
    }
}()
import LCHelper from "./TapTap/LCHelper";
import TapTapHelper from "./TapTap/TapTapHelper";
import QRCode from 'qrcode'

export default new class getQRcode {
    /**
     * 获取登录二维码url
     */
    async getRequest() {
        return await TapTapHelper.requestLoginQrCode()
    }

    /**
     * 生成url二维码
     * @param {string} url 链接
     * @returns 二维码
     */
    async getQRcode(url): Promise<Buffer> {
        return await QRCode.toBuffer(url, { scale: 10 })
    }

    /**
     * 检查二维码扫描结果
     * @returns authorization_pending authorization_waiting
     */
    async checkQRCodeResult(request) {
        return await TapTapHelper.checkQRCodeResult(request)
    }

    /**
     * 获取sessionToken
     * @param {any} result 
     * @returns token
     */
    async getSessionToken(result) {
        let profile = await TapTapHelper.getProfile(result.data)
        return (await LCHelper.loginAndGetToken({ ...profile.data, ...result.data })).sessionToken
    }
}()

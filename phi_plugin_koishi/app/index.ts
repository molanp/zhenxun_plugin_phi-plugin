import { Context } from "koishi"
import { Config } from ".."
import phiB19 from "./b19"
import phiHelp from "./help"
import phiSstk from "./session"
import phiSong from "./song"
import phiJrrp from "./jrrp"
import phiGames from "./phiGame"
import phiManage from "./manage"
import phiDownload from "./download"
import phiUserInfo from "./userInfo"

export function apply(ctx: Context, cfg: Config) {
    ctx.plugin(phiB19, cfg)
    ctx.plugin(phiSstk, cfg)
    ctx.plugin(phiHelp, cfg)
    ctx.plugin(phiSong, cfg)
    ctx.plugin(phiJrrp, cfg)
    ctx.plugin(phiGames, cfg)
    ctx.plugin(phiManage, cfg)
    ctx.plugin(phiDownload, cfg)
    ctx.plugin(phiUserInfo, cfg)
    
}
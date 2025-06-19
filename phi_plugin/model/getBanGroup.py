from ..models import phigrosBanGroup
from .cls.type import allFnc


class getBanGroup:
    @staticmethod
    async def get(group: str | None, fnc: allFnc) -> bool:
        if not group:
            return False
        match fnc:
            case "help" | "tkhelp":
                return await phigrosBanGroup.getStatus(group, "help")
            case "bind" | "unbind":
                return await phigrosBanGroup.getStatus(group, "bind")
            case (
                "b19"
                | "arcgrosB19"
                | "update"
                | "info"
                | "list"
                | "singlescore"
                | "lvscore"
                | "chap"
                | "suggest"
            ):
                return await phigrosBanGroup.getStatus(group, "b19")
            case "bestn" | "data":
                return await phigrosBanGroup.getStatus(group, "wb19")
            case "song" | "ill" | "search" | "alias" | "randmic":
                return await phigrosBanGroup.getStatus(group, "song")
            case "rankList" | "godList":
                return await phigrosBanGroup.getStatus(group, "ranklist")
            case "comrks" | "tips" | "lmtAcc" | "randClg":
                return await phigrosBanGroup.getStatus(group, "fnc")
            case "tipgame":
                return await phigrosBanGroup.getStatus(group, "tipgame")
            case "guessgame":
                return await phigrosBanGroup.getStatus(group, "guessgame")
            case "ltrgame":
                return await phigrosBanGroup.getStatus(group, "ltrgame")
            case "sign" | "send" | "tasks" | "retask" | "jrrp":
                return await phigrosBanGroup.getStatus(group, "sign")
            case "theme":
                return await phigrosBanGroup.getStatus(group, "setting")
            case "dan" | "danupdate":
                return await phigrosBanGroup.getStatus(group, "dan")
            case _:
                return False

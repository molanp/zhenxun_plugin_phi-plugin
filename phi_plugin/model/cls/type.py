from typing import Literal, NewType

idString = NewType("idString", str)
songString = NewType("songString", str)

levelKind = Literal["EZ", "HD", "IN", "AT", "LEGACY"]
noteKind = Literal["tap", "drag", "hold", "flick"]

tplName = Literal[
    "arcgrosB19",
    "song",
    "b19",
    "chap",
    "clg",
    "guess",
    "help",
    "ill",
    "jrrp",
    "list",
    "lvsco",
    "rand",
    "rankingList",
    "score",
    "setting",
    "tasks",
    "update",
    "userinfo",
]

allFnc = Literal[
    "help",
    "tkhelp",
    "bind",
    "unbind",
    "b19",
    "arcgrosB19",
    "update",
    "info",
    "list",
    "singlescore",
    "lvscore",
    "chap",
    "suggest",
    "bestn",
    "data",
    "song",
    "ill",
    "search",
    "alias",
    "randmic",
    "rankList",
    "godList",
    "randClg",
    "comrks",
    "tips",
    "lmtAcc",
    "new",
    "tipgame",
    "guessgame",
    "ltrgame",
    "sign",
    "send",
    "tasks",
    "retask",
    "jrrp",
    "theme",
    "dan",
    "danupdate",
]

import { Context } from 'koishi'

export let redis: Context['database']

declare module 'koishi' {
    interface Tables {
        phigrosBanGroup: phigrosBanGroup,
        phigrosUserToken: phigrosUserToken,
        phigrosBanSessionToken: phigrosBanSessionToken,
        phigrosUserRks: phigrosUserRks,
        phigrosJrrp: phigrosJrrp,
    }
}

// 这里是新增表的接口类型
export interface phigrosBanGroup {
    id: number;
    groupId: string;
    help: boolean;
    bind: boolean;
    b19: boolean;
    wb19: boolean;
    song: boolean;
    ranklist: boolean;
    fnc: boolean;
    tipgame: boolean;
    guessgame: boolean;
    ltrgame: boolean;
    sign: boolean;
    setting: boolean;
    dan: boolean;
}

export const banGroupId = {
    id: 'id',
    groupId: 'groupId',
    help: 'help',
    bind: 'bind',
    b19: 'b19',
    wb19: 'wb19',
    song: 'song',
    ranklist: 'ranklist',
    fnc: 'fnc',
    tipgame: 'tipgame',
    guessgame: 'guessgame',
    ltrgame: 'ltrgame',
    sign: 'sign',
    setting: 'setting',
    dan: 'dan',
}

export interface phigrosUserToken {
    id: number
    userId: string
    token: string
}

export const phigrosUserTokenId = {
    id: 'id',
    userId: 'userId',
    token: 'token',
}

export interface phigrosBanSessionToken {
    id: number;
    sessionToken: string;
}

export const phigrosBanSessionTokenId = {
    id: 'id',
    sessionToken: 'sessionToken',
}

export interface phigrosUserRks {
    id: number;
    token: string;
    rks: number;
}

export const phigrosUserRksId = {
    id: 'id',
    token: 'token',
    rks: 'rks',
}

export interface phigrosJrrp {
    id: number;
    userId: string;
    value: string;
}

export const phigrosJrrpId = {
    id: 'id',
    userId: 'userId',
    value: 'value',
}

export function apply(ctx: Context) {
    redis = ctx.database

    ctx.model.extend('phigrosBanGroup', {
        // 各字段的类型声明
        id: 'unsigned',
        groupId: 'string',
        help: 'boolean',
        bind: 'boolean',
        b19: 'boolean',
        wb19: 'boolean',
        song: 'boolean',
        ranklist: 'boolean',
        fnc: 'boolean',
        tipgame: 'boolean',
        guessgame: 'boolean',
        ltrgame: 'boolean',
        sign: 'boolean',
        setting: 'boolean',
        dan: 'boolean',
    })

    ctx.model.extend('phigrosUserToken', {
        id: 'unsigned',
        userId: 'string',
        token: 'string',
    })

    ctx.model.extend('phigrosBanSessionToken', {
        id: 'unsigned',
        sessionToken: 'string'
    })

    ctx.model.extend('phigrosUserRks', {
        id: 'unsigned',
        token: 'string',
        rks: 'double'
    })

    ctx.model.extend('phigrosJrrp', {
        id: 'unsigned',
        userId: 'string',
        value: 'string'
    })
}

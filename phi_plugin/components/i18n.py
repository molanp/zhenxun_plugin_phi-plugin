class common:
    beGroupBan = "这里被管理员禁止使用这个功能了呐QAQ！"
    haveToBind = (
        "请先绑定sessionToken哦！\n"
        "如果不知道自己的sessionToken可以尝试扫码绑定嗷！\n"
        "获取二维码：{prefix} bind qrcode\n帮助：{prefix} tk help\n"
        "格式：{prefix} bind <sessionToken>"
    )
    haveToUpdate = "请先更新数据哦！\n格式：{prefix} update"
    notFoundSong = "没有找到{0}的有关信息QAQ！"
    renderingImg = "正在生成图片，请稍等一下哦！\n//·/w\\·\\\\"
    listToLong = "谱面数量过多({0})大于设置的最大值({1})，只显示前{1}条！"
    turnToPrivate = "请私聊使用嗷"
    haveToInputName = "请指定曲名哦！\n格式：{prefix} {cmd} <曲名>"
    plusAndRange = "含有 " + " 的难度不支持指定范围哦！"
    notNum = "0} 不是一个数字哦\n"


class bind:
    haveToInputToken = (
        "*喂喂喂！你还没输入sessionToken呐！\n"
        "扫码绑定：{prefix} bind qrcode\n"
        "普通绑定：{prefix} bind <sessionToken>"
    )
    errToken = (
        "绑定sessionToken错误QAQ!\n错误的tk:{0}\n"
        "扫码绑定：{prefix} bind qrcode\n普通绑定：{prefix} bind <sessionToken>"
    )
    QRCode = (
        "\n请点击链接或扫码进行登录嗷！请勿使用他人的链接。"
        "请注意，登录TapTap可能造成账号及财产损失，请在信任Bot来源的情况下扫码登录。"
    )
    QRCodeBeUsed = "登录二维码已扫描，请确认登录"
    QRCodeTimeout = "操作超时，请重试！"
    QRCodeFail = (
        "获取sessionToken失败QAQ！请确认您的Phigros已登录TapTap账号！\n错误信息：{0}"
    )
    tipProtectToken = (
        "请注意保护好自己的sessionToken呐！"
        "如果需要获取已绑定的sessionToken可以私聊发送 {prefix} sessionToken 哦！"
    )
    ing = "正在绑定中，请稍等一下哦！\n >_<"
    failed = "更新失败，请检查你的sessionToken是否正确！\n错误信息：{0}"
    unbind = "解绑会导致历史数据全部清空呐QAQ！真的要这么做吗？（确认/取消）"
    unbindKeyWord = "确认"
    unbindSuccess = "解绑成功"
    unbindCancel = "已取消"
    clear = "请注意，本操作将会删除Phi-Plugin关于您的所有信息QAQ！（确认/取消）"
    updated = "更新了{0}份成绩"
    noUpdate = "未收集到新成绩"
    newToken = (
        "检测到新的sessionToken，将自动更换绑定。"
        "如果需要删除统计记录请 {prefix} unbind 进行解绑哦！"
    )
    noInfo = "以下曲目无信息，可能导致b19显示错误\n"
    downloadError = "绑定失败！QAQ\n"
    saveError = "保存存档失败！\n"


class game:
    haveAnotherGame = (
        "当前存在其他未结束的游戏嗷！"
        "如果想要开启新游戏请 {prefix} ans 结束进行的游戏嗷！"
    )


class letter:
    haveAnotherGame = (
        "已经在玩开字母啦！如果想要重新开始请先{prefix} ans结束本局游戏哦！"
    )
    notFoundGame = '现在还没有进行的开字母捏，快输入"{prefix} letter"开始一局吧！'
    notFoundSong = "没有找到对应的曲库嗷！"
    start = "出你字母已开始！"
    gameOver = "出你字母已结束！"
    body = "当前考试范围：{0}\n已翻开字母：{1}\n{2}"
    onlyCanOpenOne = "每次只能翻开一个字母哦！"
    haveBeOpened = "这个字母已经被翻开了哦！"
    notHaveThisLetter = "未猜测的曲目里没有这个字母嗷！"
    open = "已翻开字母{0} "
    guessMsgNoNum = "请输入一个数字哦！\n例：{prefix} n.1 df"
    guessNumIg = "没有第{0}首歌啦！"
    guessFalse = "第{0}首歌不是{1}嗷！"
    guessTrue = "恭喜你答对了！第{0}首歌是{1}！"
    getTip = "已经帮你随机翻开一个字符[ {0} ]了捏 ♪（＾∀＾●）ﾉ"


class b19:
    notFoundSong = "没有找到{0}的有关信息QAQ！"
    songNoScore = (
        "我不知道你关于[{name}]的成绩哦！可以试试更新成绩哦！\n格式：{prefix} update"
    )


class download:
    another = "已经有一个更新任务在进行中了哦！请稍后再试！"
    finish = "更新完毕！"
    illBegin = "开始下载曲绘文件"
    illFail = "曲绘文件更新失败QAQ!"
    alreadyNew = "曲绘文件已经是最新版本\n最后更新时间：{0}"
    illNew = "phi-plugin-ill\n最后更新时间：{0}"
    illFailFetch = "连接失败：{0}"


class song:
    notFoundRange = "未找到 {0} - {1} 的 {2}谱面QAQ!"
    notFoundClg = "未找到符合条件的谱面QAQ！"
    comRult = "dif={0} acc={1}\n计算结果：{2}"
    comErr = "格式错误QAQ！\n格式：{prefix} com <定数> <acc>"
    new1 = "新曲速递：\n"
    new2 = "定数&谱面修改：\n"
    newToLong = "新曲速递内容过长，请试图查阅其他途径！"


class userinfo:
    data = "您的data数为："


class i18nList:
    common = common
    bind = bind
    game = game
    letter = letter
    b19 = b19
    download = download
    song = song
    userinfo = userinfo

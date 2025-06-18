import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';
let fa = path.join("C:/Users/就是不会告诉你/Documents/WPSDrive/1441555076/WPS云盘/340708/第三次作业收集")
let flies = fs.readdirSync(fa)
console.info(flies)
for (let i of flies) {
    let f = path.join(fa, i)
    let part = i.split(".")
    let ans = `240708-${part[0]}-第03次作业.${part[1]}`
    console.info(ans)
    fs.renameSync(f, path.join(fa, ans))
}
flies = fs.readdirSync(fa)
console.info(flies)







// let url = "https://discord.com/api/v10/applications/1208030599592550511/commands"

// // # This is an example CHAT_INPUT or Slash Command, with a type of 1
// let json = {
//     "name": "bind",
//     "type": 1,
//     "description": "Bind sessionToken",
//     "options": [
//         {
//             "name": "qrcode",
//             "description": "Bind by qrcode",
//             "type": 1,
//             "required": true,
//             "value": "/bind qrcode"
//         },
//         {
//             "name": "only_smol",
//             "description": "Bind by sessionToken",
//             "type": 1,
//             "required": true,
//             "value": "/bind"
//         }
//     ]
// }

// // # For authorization, you can use either your bot token
// let headers = {
//     "Authorization": "Bot MTIwODAzMDU5OTU5MjU1MDUxMQ.G1hS6-.djwqplCp6QVFnuO-wDX_WKiewhpiLCCc_dwfqc"
// }


// console.info(await fetch(url, { headers: headers, method: "PUT", body: json }))



class Base64 {
    static decode(data) {
        let result = Buffer.from(data,'base64');
        return result.toString('hex');
    }

    // static encode(data) {
    //     let result = Buffer.from(data,'hex');
    //     return result.toString('base64');
    // }
}


export default Base64

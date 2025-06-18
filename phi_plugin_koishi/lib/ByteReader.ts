
interface ByteReader {
    data: Buffer;
    position: number;
    remaining(): number;
    getByte(): number;
    putByte(num: number): void;
    getAllByte(): string;
    getShort(): number;
    putShort(num: number): void;
    getInt(): number;
    putInt(num: number): void;
    getFloat(): number;
    putFloat(num: number): void;
    getVarInt(): number;
    skipVarInt(num: number): void;
    getBytes(): Uint8Array;
    getString(): string;
    putString(s: string): void;
    skipString(): void;
    insertBytes(bytes: Uint8Array): void;
    replaceBytes(length: number, bytes: Uint8Array): void;
}

class ByteReader {
    constructor(data, position = 0) {
        this.data = Buffer.from(data, 'hex');
        this.position = position;
    }

    /**返回剩余的字节数 */
    remaining() {
        return this.data.length - this.position
    }

    getByte() {
        return this.data[this.position++];
    }

    putByte(num) {
        this.data[this.position++] = num;
    }

    /**
     * 
     * @returns {*} base64
     */
    getAllByte() {
        return this.data.toString('base64', this.position)
    }

    getShort() {
        this.position += 2;
        return (this.data[this.position - 1] << 8) ^ (this.data[this.position - 2] & 0xff);
    }

    putShort(num: number) {
        this.data[this.position++] = num & 0xff;
        this.data[this.position++] = (num >>> 8) & 0xff;
    }

    getInt() {
        this.position += 4;
        return (
            (this.data[this.position - 1] << 24) ^
            ((this.data[this.position - 2] & 0xff) << 16) ^
            ((this.data[this.position - 3] & 0xff) << 8) ^
            (this.data[this.position - 4] & 0xff)
        );
    }

    putInt(num: number) {
        this.data[this.position] = num & 0xff;
        this.data[this.position + 1] = (num >>> 8) & 0xff;
        this.data[this.position + 2] = (num >>> 16) & 0xff;
        this.data[this.position + 3] = (num >>> 24) & 0xff;
        this.position += 4;
    }

    getFloat() {
        this.position += 4;
        return this.data.readFloatLE(this.position - 4)
    }

    putFloat(num: number) {
        this.data.writeFloatLE(num, this.position)
        this.position += 4;
    }

    getVarInt() {
        if (this.data[this.position] > 127) {
            this.position += 2;
            return Number(0b01111111 & this.data[this.position - 2]) ^ (this.data[this.position - 1] << 7);
        } else return this.data[this.position++];
    }

    skipVarInt(num?: any) {
        if (num) {
            for (; num > 0; num--) {
                this.skipVarInt();
            }
        } else {
            if (this.data[this.position] < 0) this.position += 2;
            else this.position++;
        }
    }


    getBytes() {
        let length = this.getByte();
        this.position += length;
        return this.data.subarray(this.position - length, this.position);
    }

    getString() {
        let length = this.getVarInt();

        // console.info(length)
        this.position += length;
        // return this.data.toString('hex', this.position - length, this.position - 1)
        return this.data.toString('utf-8', this.position - length, this.position)
    }

    putString(s: string) {
        let b = s.split("");
        let c = [];
        for (let i = 0; i < b.length; i++) {
            c[i] = b[i].charCodeAt(0);
        }
        this.data[this.position++] = b.length;
        this.data.set(c, this.position);
        this.position += b.length;
    }

    skipString() {
        this.position += this.getByte() + 1;
    }

    insertBytes(bytes) {
        let result = new Uint8Array(this.data.length + bytes.length);
        result.set(this.data.subarray(0, this.position), 0);
        result.set(bytes, this.position);
        result.set(this.data.subarray(this.position), this.position + bytes.length);
        this.data = Buffer.from(result);
    }

    replaceBytes(length, bytes) {
        if (bytes.length == length) {
            this.data.set(bytes, this.position);
            return;
        }
        let result = new Uint8Array(this.data.length + bytes.length - length);
        result.set(this.data.subarray(0, this.position), 0);
        result.set(bytes, this.position);
        result.set(
            this.data.subarray(this.position + length),
            this.position + bytes.length
        );
        this.data = Buffer.from(result);
    }
}
export default ByteReader;
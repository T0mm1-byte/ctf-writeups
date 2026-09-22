import json
from random import randrange
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

SBOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

RCON = [1, 2, 4, 8, 16, 32, 64, 128, 0x1B, 0x36]

def HW(x):
    res = 0
    while x > 0:
        x &= x-1
        res += 1
    return res

def multByX(x):
    return ((x << 1) & 0xFF) ^ ((256 - (x >> 7)) & 0x1b)

def mult(a,b):
    res = 0
    for i in range(7, -1, -1):
        res = multByX(res)
        if (b >> i) & 1:
            res ^= a
    return res

def addRoundKey(state, key):
    for i in range(16):
        state[i] ^= key[i]

def subBytes(state):
    for i in range(16):
        state[i] = SBOX[state[i]]

def shiftRows(state):
    tmp = state[1]
    state[1] = state[5]
    state[5] = state[9]
    state[9] = state[13]
    state[13] = tmp

    state[2] ^= state[10]
    state[10] ^= state[2]
    state[2] ^= state[10]
    state[6] ^= state[14]
    state[14] ^= state[6]
    state[6] ^= state[14]

    tmp = state[15]
    state[15] = state[11]
    state[11] = state[7]
    state[7] = state[3]
    state[3] = tmp

def mixColumns(state):
    for i in range(4):
        c0 = state[0 + 4 * i]
        c1 = state[1 + 4 * i]
        c2 = state[2 + 4 * i]
        c3 = state[3 + 4 * i]

        c01 = c0 ^ c1
        c12 = c1 ^ c2
        c23 = c2 ^ c3
        c30 = c3 ^ c0

        state[0 + 4 * i] = mult(c01, 2) ^ c12 ^ c3
        state[1 + 4 * i] = mult(c12, 2) ^ c23 ^ c0
        state[2 + 4 * i] = mult(c23, 2) ^ c30 ^ c1
        state[3 + 4 * i] = mult(c30, 2) ^ c01 ^ c2

def leakage(state):
    l = []
    for i in range(16):
        l.append(HW(state[i]))
    return l

def display(state):
    for i in range(16):
        print(f"{state[i]:02x}", end = " ")
    print()

def aesKeySchedule128(key):
    keys = [ [0] * 16 for _ in range(11) ]

    for i in range(15, -1, -1):
        keys[0][i] = key & 255
        key >>= 8

    for k in range(1,11):
        keys[k][0] = SBOX[keys[k - 1][13]] ^ keys[k - 1][0] ^ RCON[k - 1]
        keys[k][1] = SBOX[keys[k - 1][14]] ^ keys[k - 1][1]
        keys[k][2] = SBOX[keys[k - 1][15]] ^ keys[k - 1][2]
        keys[k][3] = SBOX[keys[k - 1][12]] ^ keys[k - 1][3]

        for i in range(4, 16):
            keys[k][i] = keys[k][i - 4] ^ keys[k - 1][i]

    return keys

def aesKeySchedule192(key):
    keys = [ [0] * 24 for _ in range(9) ]

    for i in range(23, -1, -1):
        keys[0][i] = key & 255
        key >>= 8

    for k in range(1, 9):
        keys[k][0] = SBOX[keys[k - 1][13+8]] ^ keys[k - 1][0] ^ RCON[k - 1]
        keys[k][1] = SBOX[keys[k - 1][14+8]] ^ keys[k - 1][1]
        keys[k][2] = SBOX[keys[k - 1][15+8]] ^ keys[k - 1][2]
        keys[k][3] = SBOX[keys[k - 1][12+8]] ^ keys[k - 1][3]

        for i in range(4, 24):
            keys[k][i] = keys[k][i - 4] ^ keys[k - 1][i]

    res = [ [0] * 16 for _ in range(13) ]
    for i in range(16 * 13):
        res[i >> 4][i & 15] = keys[i // 24][i % 24]

    return res

def aesKeySchedule256(key):
    keys = [ [0] * 32 for _ in range(8) ]

    for i in range(31, -1, -1):
        keys[0][i] = key & 255
        key >>= 8

    for k in range(1, 8):
        keys[k][0] = SBOX[keys[k - 1][13 + 16]] ^ keys[k - 1][0] ^ RCON[k - 1]
        keys[k][1] = SBOX[keys[k - 1][14 + 16]] ^ keys[k - 1][1]
        keys[k][2] = SBOX[keys[k - 1][15 + 16]] ^ keys[k - 1][2]
        keys[k][3] = SBOX[keys[k - 1][12 + 16]] ^ keys[k - 1][3]

        for i in range(4, 16):
            keys[k][i] = keys[k][i-4] ^ keys[k - 1][i]

        keys[k][0+16] = SBOX[keys[k][0 + 12]] ^ keys[k - 1][0+16]
        keys[k][1+16] = SBOX[keys[k][1 + 12]] ^ keys[k - 1][1+16]
        keys[k][2+16] = SBOX[keys[k][2 + 12]] ^ keys[k - 1][2+16]
        keys[k][3+16] = SBOX[keys[k][3 + 12]] ^ keys[k - 1][3+16]

        for i in range(20, 32):
            keys[k][i] = keys[k][i - 4] ^ keys[k - 1][i]

    res = [ [0] * 16 for _ in range(15) ]
    for i in range(16 * 15):
        res[i >> 4][i & 15] = keys[i >> 5][i & 31]

    return res

def aesKeySchedule(key):
    key_length = 128
    if key >= (1 << key_length):
        key_length += 64
    if key >= (1 << key_length):
        key_length += 64

    if key_length == 128:
        return aesKeySchedule128(key)
    elif key_length == 192:
        return aesKeySchedule192(key)
    elif key_length == 256:
        return aesKeySchedule256(key)

def AES_ENC(block, key):

    keys = aesKeySchedule(key)
    state = block.copy()
    addRoundKey(state, keys[0])
    subBytes(state)
    l=leakage(state)
    for k in keys[1:-1]:
        shiftRows(state)
        mixColumns(state)
        addRoundKey(state, k)
        subBytes(state)
    shiftRows(state)
    addRoundKey(state, keys[-1])
    return state, l

if __name__=="__main__":

    key_size = 128
    secret_key = randrange(1 << key_size)
    l = []
    m = []
    for _ in range(10):
        block = [ randrange(256) for _ in range(16) ]
        res = AES_ENC(block, secret_key)
        l.append(format(int.from_bytes(res[1], "big"), "032x"))
        m.append(format(int.from_bytes(block, "big"), "032x"))

    key = secret_key.to_bytes(16, byteorder = "big")

    flag = open("flag.txt", "rb").read().strip()

    iv = b"\x00" * 16
    c = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(flag, 16))

    data = {
        "encrypted_flag": c.hex(),
        "messages": m,
        "leakages": l
    }

    with open("scator.json", "w") as f:
        json.dump(data, f, indent = 4)

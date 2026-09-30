# --- Tabel standar DES (angka = posisi bit, 1-indexed) ---
IP = [58,50,42,34,26,18,10,2, 60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6, 64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1, 59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5, 63,55,47,39,31,23,15,7]
FP = [40,8,48,16,56,24,64,32, 39,7,47,15,55,23,63,31,
      38,6,46,14,54,22,62,30, 37,5,45,13,53,21,61,29,
      36,4,44,12,52,20,60,28, 35,3,43,11,51,19,59,27,
      34,2,42,10,50,18,58,26, 33,1,41,9,49,17,57,25]
E = [32,1,2,3,4,5, 4,5,6,7,8,9, 8,9,10,11,12,13,
     12,13,14,15,16,17, 16,17,18,19,20,21, 20,21,22,23,24,25,
     24,25,26,27,28,29, 28,29,30,31,32,1]
P = [16,7,20,21, 29,12,28,17, 1,15,23,26, 5,18,31,10,
     2,8,24,14, 32,27,3,9, 19,13,30,6, 22,11,4,25]
PC1 = [57,49,41,33,25,17,9, 1,58,50,42,34,26,18,
       10,2,59,51,43,35,27, 19,11,3,60,52,44,36,
       63,55,47,39,31,23,15, 7,62,54,46,38,30,22,
       14,6,61,53,45,37,29, 21,13,5,28,20,12,4]
PC2 = [14,17,11,24,1,5, 3,28,15,6,21,10, 23,19,12,4,
       26,8,16,7,27,20,13,2, 41,52,31,37,47,55,
       30,40,51,45,33,48, 44,49,39,56,34,53, 46,42,50,36,29,32]
SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
# 8 S-box, tiap box berisi 64 angka (input 6 bit -> output 4 bit)
SBOX = [
 [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7, 0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
  4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0, 15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
 [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10, 3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
  0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15, 13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
 [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8, 13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
  13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7, 1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
 [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15, 13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
  10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4, 3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
 [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9, 14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
  4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14, 11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
 [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11, 10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
  9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6, 4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
 [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1, 13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
  1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2, 6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
 [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7, 1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
  7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8, 2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11],
]

def _permute(bits, table):
    # Permutasi: ambil bit sesuai tabel (1-indexed). Inti dari IP/FP/E/P/PC1/PC2.
    return [bits[i - 1] for i in table]

def _bytes_to_bits(b):
    # Tiap byte -> 8 bit (MSB dulu), jadi 8 byte = 64 bit.
    return [(byte >> (7 - i)) & 1 for byte in b for i in range(8)]

def _bits_to_bytes(bits):
    # Kebalikan di atas: 8 bit -> 1 byte.
    out = bytearray()
    for i in range(0, len(bits), 8):
        v = 0
        for bit in bits[i:i + 8]:
            v = (v << 1) | bit
        out.append(v)
    return bytes(out)

def _xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

def _rotl(bits, n):
    return bits[n:] + bits[:n]

def generate_subkeys(key: bytes):
    """Key schedule: key 8 byte -> 16 subkey @48 bit."""
    assert len(key) == 8, "Key harus 8 byte"
    k56 = _permute(_bytes_to_bits(key), PC1)  # 64 -> 56 bit (buang parity)
    c, d = k56[:28], k56[28:]
    subs = []
    for shift in SHIFTS:  # 16 ronde, geser kiri lalu PC-2 -> 48 bit
        c, d = _rotl(c, shift), _rotl(d, shift)
        subs.append(_permute(c + d, PC2))
    return subs

def _feistel(r32, subkey):
    # Fungsi F: expand 32->48, XOR subkey, 8x S-box 6->4 bit, P-box 32 bit.
    e48 = _permute(r32, E)
    x = _xor(e48, subkey)
    s32 = []
    for i in range(8):  # tiap blok 6 bit: bit luar = baris, bit tengah = kolom
        b = x[i * 6:(i + 1) * 6]
        row = (b[0] << 1) | b[5]
        col = (b[1] << 3) | (b[2] << 2) | (b[3] << 1) | b[4]
        v = SBOX[i][row * 16 + col]
        s32 += [(v >> 3) & 1, (v >> 2) & 1, (v >> 1) & 1, v & 1]
    return _permute(s32, P)

def encrypt_block(block: bytes, subkeys):
    """Enkripsi 1 blok 8 byte (Feistel 16 ronde)."""
    assert len(block) == 8
    lr = _permute(_bytes_to_bits(block), IP)
    l, r = lr[:32], lr[32:]
    for i in range(16):  # L'=R, R'=L xor F(R,Ki)
        l, r = r, _xor(l, _feistel(r, subkeys[i]))
    return _bits_to_bytes(_permute(r + l, FP))  # swap akhir R+L lalu FP

def decrypt_block(block: bytes, subkeys):
    """Dekripsi = enkripsi dengan urutan subkey dibalik."""
    assert len(block) == 8
    lr = _permute(_bytes_to_bits(block), IP)
    l, r = lr[:32], lr[32:]
    for i in range(15, -1, -1):
        l, r = r, _xor(l, _feistel(r, subkeys[i]))
    return _bits_to_bytes(_permute(r + l, FP))

def _pad(data: bytes) -> bytes:
    # tambah N byte bernilai N agar panjang kelipatan 8.
    n = 8 - (len(data) % 8)
    return data + bytes([n]) * n

def _unpad(data: bytes) -> bytes:
    n = data[-1]  # baca byte terakhir, potong sebanyak itu
    if not 1 <= n <= 8 or data[-n:] != bytes([n]) * n:
        raise ValueError("Padding rusak / key salah")
    return data[:-n]

def encrypt_ecb(plain: bytes, key: bytes) -> bytes:
    # ECB: pad lalu tiap blok 8 byte di-DES mandiri.
    subs = generate_subkeys(key)
    data = _pad(plain)
    return b"".join(encrypt_block(data[i:i + 8], subs) for i in range(0, len(data), 8))

def decrypt_ecb(cipher: bytes, key: bytes) -> bytes:
    """ECB decrypt: tiap blok di-DES-decrypt lalu unpad."""
    assert len(cipher) % 8 == 0
    subs = generate_subkeys(key)
    return _unpad(b"".join(decrypt_block(cipher[i:i + 8], subs) for i in range(0, len(cipher), 8)))

def key_from_string(s: str) -> bytes:
    """Key 8 karakter -> 8 byte. Kurang dari 8 di-nol-pad, lebih dipotong."""
    b = s.encode()[:8]
    return b + b"\x00" * (8 - len(b))

if __name__ == "__main__":
    # Test vector resmi DES: Key=133457799BBCDFF1 Plain=0123456789ABCDEF -> 85E813540F0AB405
    k = bytes.fromhex("133457799BBCDFF1")
    p = bytes.fromhex("0123456789ABCDEF")
    subs = generate_subkeys(k)
    c = encrypt_block(p, subs)
    assert c.hex().upper() == "85E813540F0AB405", c.hex()
    assert decrypt_block(c, subs) == p
    assert decrypt_ecb(encrypt_ecb(b"Halo DES!", k), k) == b"Halo DES!"
    print("DES OK: test vector + ECB round-trip lolos")

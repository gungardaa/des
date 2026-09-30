import os, socket, struct, threading, time
from des import encrypt_ecb, decrypt_ecb, key_from_string

HOST = os.environ.get("SENDER_HOST", "127.0.0.1")
PORT = int(os.environ.get("DES_PORT", "5050"))

def recv_all(conn, n):
    buf = b""  # kumpulkan sampai n byte karena batas recv TCP tidak pasti
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf

def listen_loop(conn, key):
    try: 
        while True: 
            hdr = recv_all(conn, 4)
            if not hdr:
                print("\n[sender terputus] ketik exit + Enter untuk keluar"); break
            (ln,) = struct.unpack("!I", hdr)
            cipher = recv_all(conn, ln)
            if not cipher or len(cipher) % 8:  # lawan tutup di tengah pesan / data korup
                print("\n[sender terputus] ketik exit + Enter untuk keluar"); break
            print(f"\n[RECV ciphertext: {cipher.hex()}]")
            try:
                print(f"[RECV plaintext : {decrypt_ecb(cipher, key).decode()}]")
            except Exception as e:
                print(f"[gagal dekripsi: {e}]")
            print("> ", end="", flush=True)
    except (ConnectionResetError, ConnectionAbortedError):  # FIN paksa Windows
        print("\n[sender terputus] ketik exit + Enter untuk keluar")

def main():
    key = key_from_string(os.environ.get("DES_KEY") or input("Key bersama (harus SAMA dgn sender): ") or "RAHASIA1")
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:  # retry sampai sender sudah listen
        try:
            conn.connect((HOST, PORT)); break
        except ConnectionRefusedError:
            print("[receiver] menunggu sender..."); time.sleep(1)
    print("[receiver] terhubung. Bisa chat bolak-balik. Ketik 'exit' untuk keluar.")
    threading.Thread(target=listen_loop, args=(conn, key), daemon=True).start()
    try:  # Ctrl+C saat input() di Windows baru diproses setelah Enter
        while True:  # loop pengirim: enkripsi DES lalu kirim
            msg = input("> ")
            if msg.strip().lower() == "exit":
                break
            cipher = encrypt_ecb(msg.encode(), key)
            print(f"[SEND ciphertext: {cipher.hex()}]")
            conn.sendall(struct.pack("!I", len(cipher)) + cipher)
    except KeyboardInterrupt:
        print("\n[keluar]")
    conn.close() 

if __name__ == "__main__":
    main()

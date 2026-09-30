import os, socket, struct, threading
from des import encrypt_ecb, decrypt_ecb, key_from_string

BIND_HOST = os.environ.get("BIND_HOST", "0.0.0.0")
PORT = int(os.environ.get("DES_PORT", "5050"))

def recv_all(conn, n):
    buf = b""  # TCP itu stream, recv belum tentu sekali utuh -> loop sampai n byte
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf

def listen_loop(conn, key):
    try:  # putus paksa di Windows melempar ConnectionResetError, bukan return kosong
        while True:  
            hdr = recv_all(conn, 4)
            if not hdr:
                print("\n[receiver terputus] ketik exit + Enter untuk keluar"); break
            (ln,) = struct.unpack("!I", hdr)
            cipher = recv_all(conn, ln)
            if not cipher or len(cipher) % 8:  # lawan tutup di tengah pesan / data korup
                print("\n[receiver terputus] ketik exit + Enter untuk keluar"); break
            print(f"\n[RECV ciphertext: {cipher.hex()}]")
            try:
                print(f"[RECV plaintext : {decrypt_ecb(cipher, key).decode()}]")
            except Exception as e:
                print(f"[gagal dekripsi: {e}]")
            print("> ", end="", flush=True)
    except (ConnectionResetError, ConnectionAbortedError):  # FIN paksa Windows
        print("\n[receiver terputus] ketik exit + Enter untuk keluar")

def main():
    key = key_from_string(os.environ.get("DES_KEY") or input("Key bersama (8 karakter, mis. RAHASIA1): ") or "RAHASIA1")
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((BIND_HOST, PORT)); srv.listen(1)
    print(f"[sender] listen {BIND_HOST}:{PORT}, menunggu receiver...")
    conn, addr = srv.accept()
    print(f"[sender] terhubung {addr}. Silakan kirim pesan. Ketik 'exit' untuk keluar.")
    threading.Thread(target=listen_loop, args=(conn, key), daemon=True).start()
    try:  # Ctrl+C saat input() di Windows baru diproses setelah Enter
        while True:  # loop pengirim: plaintext -> DES encrypt -> kirim ciphertext
            msg = input("> ")
            if msg.strip().lower() == "exit":
                break
            cipher = encrypt_ecb(msg.encode(), key)
            print(f"[SEND ciphertext: {cipher.hex()}]")
            conn.sendall(struct.pack("!I", len(cipher)) + cipher)
    except KeyboardInterrupt:
        print("\n[keluar]")
    conn.close(); srv.close()  # 1 koneksi + chat plain tanpa auth/TLS

if __name__ == "__main__":
    main()

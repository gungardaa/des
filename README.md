# Chat Terenkripsi DES (Dua Arah)

Nama: Anak Agung Putu Arda Nareswara <br>
NRP: 50250241074 <br>
Kelas: B

 Dua program saling berkirim pesan terenkripsi lewat jaringan. Enkripsi memakai DES yang ditulis manual tanpa library crypto.

## Isi folder

- `des.py` berisi algoritma DES dan fungsi bantu key. File ini tidak menyentuh jaringan sama sekali.
- `sender.py` adalah pihak pertama. Berperan sebagai server yang menunggu koneksi.
- `receiver.py` adalah pihak kedua. Berperan sebagai client yang menghubungi sender.
- `Dockerfile` dan `compose.yaml` untuk menjalankan keduanya sebagai container dengan IP berbeda.

## Cara kerja singkat

Pesan diketik sebagai teks biasa lalu diubah ke bytes UTF-8. Karena DES hanya memproses 8 byte sekali jalan, pesan diberi padding supaya panjangnya tepat kelipatan 8. Tiap blok 8 byte masuk ke 16 ronde Feistel dengan 16 subkey hasil key schedule lalu keluar sebagai ciphertext. Mode yang dipakai adalah ECB, artinya tiap blok dienkripsi sendiri-sendiri. Ciphertext dikirim lewat TCP dengan awalan 4 byte yang menyatakan panjangnya. Sisi penerima membaca panjang itu dulu baru membaca ciphertextnya lalu mendekripsinya kembali ke teks.

Key sudah diatur sebelum program jalan dan tidak pernah dikirim lewat jaringan. Key berupa 8 karakter, misalnya `RAHASIA1`. Kalau kurang dari 8 maka diisi nol, kalau lebih maka dipotong. Kedua sisi wajib memakai key yang sama, kalau beda maka hasil dekripsi gagal.

## Menjalankan di 1 laptop (2 terminal)

Terminal pertama:

```
python sender.py
```

Terminal kedua:

```
python receiver.py
```

Masukkan key yang sama di keduanya. Setelah terhubung, tiap sisi bisa mengetik pesan dan dibalas dari sisi lain. Ketik `exit` untuk keluar. Kalau salah satu sisi menutup program, sisi satunya menampilkan pesan terputus.

## Menjalankan dengan Docker (2 IP berbeda)

Pastikan Docker sudah terpasang, lalu dari dalam folder ini:

```
docker compose up --build -d
```

Buka chatnya dari 2 terminal:

```
docker attach des-sender
docker attach des-receiver
```

Key sudah diisi otomatis dari `compose.yaml`, jadi tidak perlu mengetik key lagi. Untuk melepas terminal tanpa mematikan container, tekan `Ctrl+P` lalu `Ctrl+Q`. Untuk berhenti total, ketik `exit` di kedua sisi lalu `docker compose down`.

Untuk membuktikan IP-nya beda, jalankan:

```
docker exec des-sender hostname -i
docker exec des-receiver hostname -i
```
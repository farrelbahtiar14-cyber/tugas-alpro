# SirkuitLab — versi Python + Dark Mode

Website pembelajaran rangkaian listrik dengan antarmuka HTML/CSS/JavaScript dan backend Python menggunakan Flask.

## Cara menjalankan

1. Pastikan Python 3.10+ sudah terpasang.
2. Ekstrak ZIP ini.
3. Buka terminal/Command Prompt di folder `sirkuitlab_python`.
4. (Opsional, disarankan) Buat virtual environment:
   - Windows: `py -m venv .venv`
   - Aktifkan: `.venv\\Scripts\\activate`
5. Pasang dependensi: `py -m pip install -r requirements.txt`
6. Jalankan: `py app.py`
7. Buka browser ke `http://127.0.0.1:5000`.

Jika perintah `py` tidak tersedia, coba ganti `py` dengan `python`.

## Bagian yang memakai Python

- `app.py` menjalankan server Flask.
- Endpoint `/api/simulate` menghitung resistansi ekuivalen, arus, tegangan resistor, dan daya untuk rangkaian DC seri/paralel.
- Endpoint `/api/ohm` menghitung nilai yang belum diketahui dari Hukum Ohm.
- Halaman web memanggil endpoint tersebut melalui `fetch()`.

## Dark mode

Klik tombol `🌙 Mode gelap` di bagian atas. Pilihan tema disimpan di browser sehingga tetap dipakai saat dibuka lagi.

Catatan: gunakan server Flask, jangan membuka `index.html` dengan klik dua kali, karena fitur perhitungan Python memerlukan server.

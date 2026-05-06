# 🚀 NixMix Omni-Bot (Blockchain & Task Tracker)

Bot Telegram pintar berbasis Python yang dirancang untuk membantu para pemburu airdrop dan developer dalam mengelola link garapan, memantau transaksi blockchain, dan mengatur deadline secara otomatis.

## 🌟 Fitur Utama

- **Auto-Sortir Deadline**: Menampilkan daftar garapan dari yang paling mendekati waktu berakhir (Urutan Berdasarkan Waktu).
- **Anti-Duplikat**: Sistem secara otomatis menolak input link yang sudah terdaftar dalam database.
- **Auto-Clean Expired**: Secara otomatis membersihkan link yang sudah melewati batas waktu saat menampilkan daftar.
- **Silent Message Cleaner**: Perintah `/clear` untuk membersihkan chat log secara instan tanpa meninggalkan pesan notifikasi yang menumpuk.
- **Multi-Chain Support**: Terintegrasi dengan network BSC, Polygon, Ethereum, dan Base (NixMix Omni-Bot Core).

## 🛠️ Teknologi yang Digunakan

- [Python 3.10+](https://www.python.org/)
- [Telebot (pyTelegramBotAPI)](https://github.com/eternnoir/pyTelegramBotAPI)
- [Termux](https://termux.dev/) (Mobile Environment)

## 📦 Instalasi & Penggunaan

1. **Clone Repository**
   ```bash
   git clone [https://github.com/nixmixdev/nixmixbot.git](https://github.com/nixmixdev/nixmixbot.git)
   cd nixmixbot
2. **Install Dependensi**
   ```bash 
   pip install pyTelegramBotAPI

3. **Konfigurasi**
   Buka file nixmix_bot.py dan masukkan Token bot Telegram Anda:
   ```bash 
   TOKEN = 'YOUR_BOT_TOKEN_HERE'
   ADMIN_IDS = [YOUR_ID_HERE]

4. **Jalankan Bot**
   ```bash
   python nixmix_bot.py


## 📝 Perintah Bot

* **/add [link] | [YYYY-MM-DD HH:MM]** - Tambah garapan baru.
* **/list** - Lihat daftar garapan aktif (Terurut berdasarkan deadline).
* **/clear** - Membersihkan history chat bot secara instan.

---
Developed with ❤️ by **[NixMix](https://github.com/nixmixdev)**

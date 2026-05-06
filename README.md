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

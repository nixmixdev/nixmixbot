import telebot
import os
import time
import threading
from datetime import datetime
from telebot import types

# --- KONFIGURASI ---
# Bagian Token dan Admin ID
TOKEN = 'ISI_TOKEN_BOT_KAMU_DI_SINI' 
ADMIN_IDS = [12345678] # Ganti dengan ID kamu
DB_PATH = os.path.expanduser('~/daftar_garapan.txt')
bot = telebot.TeleBot(TOKEN)

# --- FUNGSI PROTEKSI ---
def is_admin(user_id):
    return user_id in ADMIN_IDS

# --- FUNGSI AUTO-DELETE PESAN ---
def hapus_nanti(chat_id, message_id, delay=60):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

# --- FUNGSI SORTIR & BERSIHKAN (LOGIKA UTAMA) ---
def dapatkan_list_terurut():
    # Proteksi jika file tidak ada atau kosong
    if not os.path.exists(DB_PATH) or os.stat(DB_PATH).st_size == 0:
        return "Daftar garapan kosong, NixMix!", []

    try:
        with open(DB_PATH, 'r') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]

        data_list = []
        aktif_lines_file = []
        sekarang = datetime.now()

        for line in lines:
            if '|' not in line: continue
            parts = line.split('|')
            link = parts[0].strip()
            deadline_str = parts[1].strip()

            try:
                deadline_dt = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
                sisa_detik = int((deadline_dt - sekarang).total_seconds())

                if sisa_detik > 0:
                    data_list.append({'link': link, 'detik': sisa_detik})
                    aktif_lines_file.append(line + '\n')
            except:
                continue

        # Tulis ulang file agar yang expired hilang
        with open(DB_PATH, 'w') as f:
            f.writelines(aktif_lines_file)

        if not data_list:
            return "Semua garapan sudah expired!", []

        # Urutkan berdasarkan detik (paling mepet di atas)
        data_terurut = sorted(data_list, key=lambda x: x['detik'])

        pesan = "🔔 <b>DAFTAR GARAPAN AKTIF</b>\n\n"
        for item in data_terurut:
            detik = item['detik']
            hari = detik // 86400
            jam = (detik % 86400) // 3600
            menit = (detik % 3600) // 60

            if hari > 0:
                status = f"⏳ {hari} hari {jam} jam lagi"
            else:
                status = f"⏳ {jam} jam {menit} menit lagi"

            pesan += f"🔗 {item['link']}\n└ {status}\n\n"

        # WAJIB: Selalu kembalikan dua nilai
        return pesan, data_terurut

    except Exception as e:
        print(f"Error di fungsi sortir: {e}")
        return "Terjadi kesalahan saat memproses daftar.", []


# --- MENU TOMBOL ---
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_list = types.InlineKeyboardButton("📋 Cek List", callback_data="cek_list")
    btn_add = types.InlineKeyboardButton("➕ Cara Add", callback_data="cara_add")
    markup.add(btn_list, btn_add)
    return markup

# --- HANDLERS ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, f"❌ Akses Ditolak!\nID: {message.from_user.id}")
        return
    bot.send_message(message.chat.id, "🤖 <b>Bot Privat NixMix Aktif</b>\n\nGunakan tombol di bawah untuk navigasi.", parse_mode='HTML', reply_markup=main_menu())

@bot.message_handler(commands=['add'])
def handle_add(message):
    if not is_admin(message.from_user.id): return

    try:
        input_user = message.text.replace('/add', '').strip()
        parts = input_user.split(' ')

        if len(parts) < 3:
            bot.send_message(message.chat.id, "❌ <b>Format Salah!</b>\nGunakan: <code>/add [link] [YYYY-MM-DD] [HH:MM]</code>", parse_mode='HTML')
            return

        link_baru = parts[0].strip()
        tanggal = parts[1]
        jam = parts[2]
        deadline = f"{tanggal} {jam}"

        # --- PROTEKSI DUPLIKAT ---
        if os.path.exists(DB_PATH):
            with open(DB_PATH, 'r') as f:
                isi_file = f.read()
                if link_baru in isi_file:
                    bot.send_message(message.chat.id, f"⚠️ <b>Link Duplikat!</b>\nLink ini sudah ada di daftar garapan aktif kamu.", parse_mode='HTML')
                    return
        # -------------------------

        # Jika tidak duplikat, simpan ke file
        with open(DB_PATH, 'a') as f:
            f.write(f"{link_baru} | {deadline}\n")

        bot.send_message(message.chat.id, f"✅ <b>Tersimpan!</b>\n🔗 {link_baru}\n ⏳ Deadline: {deadline}", parse_mode='HTML', reply_markup=main_menu())

    except Exception as e:
        bot.reply_to(message, f"⚠️ Terjadi error: {e}")

@bot.message_handler(commands=['clear'])
def handle_clear(message):
    if not is_admin(message.from_user.id): return

    chat_id = message.chat.id
    last_msg_id = message.message_id

    # Langsung eksekusi hapus tanpa kirim pesan "sedang membersihkan"
    # agar proses terasa lebih sat-set
    count = 0
    for i in range(100):
        try:
            bot.delete_message(chat_id, last_msg_id - i)
            count += 1
        except:
            continue

    # Begitu selesai (Done), langsung kirim notif singkat
    notif = bot.send_message(chat_id, f"🧹 {count} Pesan telah dibersihkan!")

    # Gunakan delay sangat singkat (misal 3-5 detik) lalu hapus notifnya
    threading.Thread(target=hapus_nanti, args=(chat_id, notif.message_id, 3)).start()


@bot.message_handler(commands=['list'])
def handle_list(message):
    if not is_admin(message.from_user.id): return
    teks, _ = dapatkan_list_terurut()
    bot.send_message(message.chat.id, teks, parse_mode='HTML', disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Akses ditolak!")
        return

    if call.data == "cek_list":
        teks, _ = dapatkan_list_terurut()
        msg = bot.send_message(call.message.chat.id, teks, parse_mode='HTML', disable_web_page_preview=True)
        # Hapus pesan list otomatis setelah 60 detik agar grup/chat tetap bersih
        threading.Thread(target=hapus_nanti, args=(call.message.chat.id, msg.message_id, 60)).start()
        bot.answer_callback_query(call.id, "Daftar Terupdate!")

    elif call.data == "cara_add":
        bot.send_message(call.message.chat.id, "<b>Format Tambah:</b>\n<code>/add https://link.com 2026-05-30 18:00</code>", parse_mode='HTML')
        bot.answer_callback_query(call.id)

print("Bot NixMix Aktif...")
bot.polling()

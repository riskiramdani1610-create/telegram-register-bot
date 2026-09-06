# 🤖 Telegram Bot - Registrasi Akun Pangtiger

Bot Telegram otomatis untuk memudahkan proses registrasi akun Pangtiger dengan verifikasi OTP dan bind custom account.

## 📋 Fitur

- ✅ Registrasi nomor HP
- ✅ Verifikasi OTP (dengan limit percobaan)
- ✅ Membuat custom account
- ✅ Validasi password yang kuat
- ✅ Database user dalam format TXT
- ✅ Tracking session registrasi
- ✅ Cek status registrasi

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Telegram Bot Token (dari BotFather)
- Akses ke API Pangtiger

### Instalasi

1. **Clone repository**
```bash
git clone https://github.com/riskiramdani1610-create/telegram-register-bot.git
cd telegram-register-bot
```

2. **Setup virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
```

Edit `.env` dan masukkan:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
API_BASE_URL=https://api.pangtiger.com
```

5. **Jalankan bot**
```bash
python bot.py
```

## 📱 Cara Menggunakan

### Perintah Bot

| Perintah | Deskripsi |
|----------|----------|
| `/start` | Mulai proses registrasi |
| `/status` | Cek status registrasi Anda |
| `/help` | Tampilkan bantuan |
| `/cancel` | Batalkan registrasi |

### Proses Registrasi

1. **Ketik `/start`** untuk memulai
2. **Masukkan nomor HP** dengan format `62XXXXXXXXXX`
3. **Verifikasi OTP** yang diterima melalui SMS/WhatsApp
4. **Buat username** untuk custom account
5. **Buat password** (minimal 8 karakter, kombinasi huruf besar, kecil, dan angka)
6. **Konfirmasi** data registrasi
7. **Selesai!** ✅

## 📂 Struktur Proyek

```
telegram-register-bot/
├── bot.py              # Main bot application
├── database.py         # Database management (TXT)
├── api_client.py       # API client untuk Pangtiger
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore rules
├── users.txt          # Database user (auto-created)
├── sessions.txt       # Database session (auto-created)
└── README.md          # Dokumentasi
```

## 🗄️ Database Format

### users.txt
Menyimpan data user dalam format JSON per baris:
```json
{"user_id": 123456789, "phone": "628123456789", "name": "John", "status": "verified", "created_at": "2024-01-15T10:30:00", "updated_at": "2024-01-15T10:35:00"}
```

### sessions.txt
Menyimpan session registrasi dalam format JSON per baris:
```json
{"session_id": "session_123456789_1234567890", "user_id": 123456789, "phone": "628123456789", "step": "completed", "otp_code": "123456", "verification_attempts": 1, "created_at": "2024-01-15T10:30:00", "updated_at": "2024-01-15T10:35:00"}
```

## 🔌 API Endpoints yang Digunakan

### 1. Register Phone
```
POST /api/user/phone_register
Content-Type: application/json

{
  "phone": "628123456789"
}
```

### 2. Verify OTP
```
POST /userverse/api/v1/verify-code/user/phone
Content-Type: application/json

{
  "phone": "628123456789",
  "code": "123456"
}
```

### 3. Bind Custom Account
```
POST /hall/userverse/api/v1/bind/custom-account
Content-Type: application/json

{
  "user_id": "123456789",
  "custom_account": "username",
  "password": "SecurePass123"
}
```

## 🛡️ Validasi

### Nomor HP
- Harus dimulai dengan `62`
- Minimal 10 digit

### Custom Account (Username)
- Minimal 3 karakter
- Hanya huruf, angka, underscore (_), dan dash (-)

### Password
- Minimal 8 karakter
- Mengandung huruf besar dan kecil
- Mengandung angka

### OTP
- 4-6 digit angka
- Maksimal 3 percobaan salah

## ⚙️ Konfigurasi

### Timeout Request
Default: 10 detik (bisa diubah di `api_client.py`)

### Max OTP Attempts
Default: 3 kali (bisa diubah di `bot.py`)

### Database File
Bisa diubah saat inisialisasi:
```python
user_db = UserDatabase("nama_file_custom.txt")
session_db = SessionDatabase("nama_file_session_custom.txt")
```

## 🐛 Troubleshooting

### Bot tidak merespons
- Pastikan TELEGRAM_BOT_TOKEN benar
- Cek koneksi internet
- Lihat log untuk error messages

### Error "Connection error"
- Pastikan API_BASE_URL benar
- Cek koneksi ke server Pangtiger
- Gunakan VPN jika diperlukan

### Database error
- Pastikan folder project writable
- Cek permission file `users.txt` dan `sessions.txt`
- Delete dan biarkan bot membuat ulang

## 📊 Logging

Bot menggunakan Python logging. Log ditampilkan di console dengan format:
```
2024-01-15 10:30:45,123 - bot - INFO - User 123456789 berhasil registrasi dengan nomor 628123456789
```

## 📝 License

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan.

## 📞 Support

Jika ada masalah atau pertanyaan, silakan:
1. Buat issue di GitHub
2. Hubungi developer
3. Cek dokumentasi API Pangtiger

## 🔄 Update Log

### v1.0.0 (2024-01-15)
- Initial release
- Fitur registrasi, OTP verification, dan bind custom account
- Database TXT implementation
- Validation dan error handling

---

**Happy registering!** 🎉
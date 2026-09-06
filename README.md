# 🤖 Telegram Registration Bot

Bot Telegram untuk registrasi otomatis di h5.bigwinner10.com

## ✨ Fitur

- ✅ Bind custom account dengan nomor acak
- ✅ Verifikasi dengan nomor telepon asli
- ✅ Otomatis input OTP dari SMS
- ✅ User-friendly conversation flow

## 🚀 Setup

### 1. Clone Repository

```bash
cd ~/telegram-register-bot
git pull
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment

```bash
cp .env.example .env
# Edit .env dan masukkan TELEGRAM_TOKEN Anda
nano .env
```

### 4. Jalankan Bot

```bash
python3 main.py
```

## 📋 Flow Registrasi

```
1. /start
   ↓
2. Masukkan nomor acak untuk BIND
   ↓
3. Masukkan password
   ↓
4. Konfirmasi data
   ↓
5. [BIND ACCOUNT EXECUTION]
   ↓
6. Masukkan nomor telepon ASLI
   ↓
7. Konfirmasi kirim OTP
   ↓
8. [REQUEST OTP EXECUTION]
   ↓
9. Cek SMS, masukkan OTP
   ↓
10. [VERIFY OTP EXECUTION]
    ↓
11. ✅ REGISTRASI SELESAI
```

## ⚠️ TODO

- [ ] Find algoritma generate `sign` parameter
- [ ] Implement actual API calls (bind_custom_account, request_otp, verify_otp)
- [ ] Add error handling & retry logic
- [ ] Add database untuk tracking registrations
- [ ] Add admin panel untuk monitoring

## 🔍 Sign Parameter

Sekarang sedang reverse-engineer cara generate `sign` parameter.

**Status:** Pending - cari pattern-nya

**Butuh dari Anda:**
- 3-5 contoh payload + sign
- atau File JavaScript dari h5.bigwinner10.com
- atau Info tentang algoritma sign-nya

## 📝 Struktur Kode

```
telegram-register-bot/
├── main.py                 # Entry point
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── handlers/
│   └── user_handler.py   # Bot logic
├── utils/
│   ├── api_client.py     # API communication
│   └── sign_generator.py # Sign generation
└── README.md
```

## 🆘 Troubleshooting

### Bot tidak merespons

```bash
# Check TELEGRAM_TOKEN di .env
nano .env

# Pastikan token benar
python3 -c "from config import TELEGRAM_TOKEN; print(f'Token length: {len(TELEGRAM_TOKEN)}')"
```

### Error connection API

```bash
# Test koneksi
curl -s https://api.pangtiger.com/hall/userverse/api/v1/ 
```

## 📞 Support

Kalau ada error atau pertanyaan, dm via Telegram! 😉

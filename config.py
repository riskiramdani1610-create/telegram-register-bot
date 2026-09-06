"""
Configuration file untuk bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.pangtiger.com")
API_TIMEOUT = 10

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Database Configuration
USER_DATABASE_FILE = "users.txt"
SESSION_DATABASE_FILE = "sessions.txt"

# Validation Rules
PHONE_MIN_LENGTH = 10
USERNAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 8
MAX_OTP_ATTEMPTS = 3

# API Endpoints
ENDPOINTS = {
    "register_phone": "/api/user/phone_register",
    "verify_code": "/userverse/api/v1/verify-code/user/phone",
    "bind_account": "/hall/userverse/api/v1/bind/custom-account",
}

# Messages
MESSAGES = {
    "welcome": "👋 Halo {name}! Selamat datang di Bot Registrasi Pangtiger.",
    "already_registered": "✅ Anda sudah terdaftar sebelumnya.",
    "invalid_phone": "❌ Format nomor HP tidak valid! Gunakan format: 62XXXXXXXXXX",
    "phone_exists": "❌ Nomor HP ini sudah terdaftar sebelumnya.",
    "otp_sent": "✅ Kode OTP telah dikirim ke {phone}",
    "otp_invalid": "❌ Kode OTP tidak valid! Percobaan {attempt}/3",
    "otp_expired": "⏰ Kode OTP sudah kadaluarsa. Silakan minta kode baru.",
    "username_invalid": "❌ Username tidak valid. Gunakan huruf, angka, underscore, atau dash.",
    "password_weak": "🔐 Password kurang kuat. Harus minimal 8 karakter dengan kombinasi huruf besar, kecil, dan angka.",
    "registration_success": "🎉 Registrasi berhasil! Akun Anda siap digunakan.",
    "registration_failed": "❌ Registrasi gagal. Silakan coba lagi.",
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

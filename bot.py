"""
Telegram Bot untuk Registrasi Akun Pangtiger
"""
import os
import logging
import random
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from database import UserDatabase, SessionDatabase
from api_client import PangtierAPIClient

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database dan API client
user_db = UserDatabase("users.txt")
session_db = SessionDatabase("sessions.txt")
api_client = PangtierAPIClient(os.getenv("API_BASE_URL", "https://api.pangtiger.com"))

# Conversation states
PHONE, OTP, CUSTOM_ACCOUNT, PASSWORD, CONFIRM = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Command /start - Mulai registrasi"""
    user = update.effective_user
    
    # Cek apakah user sudah terdaftar
    existing_user = user_db.get_user(user.id)
    if existing_user and existing_user.get("status") == "verified":
        await update.message.reply_text(
            f"👋 Halo {user.first_name}! Anda sudah terdaftar.\n\n"
            f"Nomor HP: {existing_user.get('phone')}\n"
            f"Status: ✅ Terverifikasi\n\n"
            f"Gunakan /help untuk melihat perintah lainnya."
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        f"👋 Halo {user.first_name}! Selamat datang di Bot Registrasi Pangtiger.\n\n"
        f"Saya akan membantu Anda mendaftar akun. Mari kita mulai!\n\n"
        f"📱 Silakan masukkan nomor HP Anda (format: 62XXXXXXXXXX)"
    )
    
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menerima nomor HP dari user"""
    user = update.effective_user
    phone = update.message.text.strip()
    
    # Validasi nomor HP
    if not phone.startswith('62'):
        await update.message.reply_text(
            "❌ Format nomor HP salah!\n\n"
            "Gunakan format: 62XXXXXXXXXX\n"
            "Contoh: 628123456789"
        )
        return PHONE
    
    if len(phone) < 10:
        await update.message.reply_text(
            "❌ Nomor HP terlalu pendek!\n"
            "Minimal 10 digit setelah kode negara."
        )
        return PHONE
    
    # Cek apakah nomor HP sudah terdaftar
    existing = user_db.get_user_by_phone(phone)
    if existing:
        await update.message.reply_text(
            f"❌ Nomor HP ini sudah terdaftar sebelumnya.\n\n"
            f"Silakan gunakan nomor HP lain atau hubungi support."
        )
        return PHONE
    
    # Simpan ke context
    context.user_data['phone'] = phone
    context.user_data['user_id'] = user.id
    
    # Cek koneksi API
    if not api_client.health_check():
        await update.message.reply_text(
            "⚠️ Server sedang mengalami gangguan. Silakan coba lagi nanti."
        )
        return ConversationHandler.END
    
    # Kirim ke API untuk registrasi
    result = api_client.register_phone(phone)
    
    if not result.get('success'):
        await update.message.reply_text(
            f"❌ Gagal mendaftar nomor HP.\n\n"
            f"Error: {result.get('error')}\n\n"
            f"Silakan coba lagi atau hubungi support."
        )
        return PHONE
    
    # Simpan user ke database dengan status pending
    user_db.add_user(user.id, phone, user.first_name, "pending")
    
    # Buat session
    session_id = session_db.create_session(user.id, phone, "phone_registered")
    context.user_data['session_id'] = session_id
    
    await update.message.reply_text(
        f"✅ Nomor HP berhasil didaftarkan!\n\n"
        f"📱 {phone}\n\n"
        f"Silakan cek pesan masuk Anda untuk kode OTP.\n"
        f"Masukkan kode OTP (4-6 digit):"
    )
    
    return OTP


async def get_otp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menerima kode OTP dari user"""
    otp_code = update.message.text.strip()
    phone = context.user_data.get('phone')
    session_id = context.user_data.get('session_id')
    
    # Validasi kode OTP
    if not otp_code.isdigit() or len(otp_code) < 4:
        await update.message.reply_text(
            "❌ Kode OTP tidak valid!\n\n"
            "Kode OTP harus berupa angka, minimal 4 digit."
        )
        return OTP
    
    # Verifikasi OTP melalui API
    result = api_client.verify_code(phone, otp_code)
    
    if not result.get('success'):
        # Increment percobaan
        session = session_db.get_session(session_id)
        attempts = session.get('verification_attempts', 0) if session else 0
        attempts += 1
        
        if attempts >= 3:
            await update.message.reply_text(
                "❌ Percobaan verifikasi gagal lebih dari 3 kali.\n\n"
                "Silakan mulai ulang dengan /start"
            )
            session_db.delete_session(session_id)
            return ConversationHandler.END
        
        session_db.update_session(session_id, verification_attempts=attempts)
        
        await update.message.reply_text(
            f"❌ Kode OTP salah! Percobaan {attempts}/3\n\n"
            f"Silakan coba lagi:"
        )
        return OTP
    
    # Update session dan user
    session_db.update_session(session_id, step="otp_verified", otp_code=otp_code)
    user_db.update_user(context.user_data['user_id'], status="otp_verified")
    
    await update.message.reply_text(
        "✅ Kode OTP berhasil diverifikasi!\n\n"
        "Sekarang saatnya membuat custom account.\n\n"
        "Masukkan username untuk custom account Anda:"
    )
    
    return CUSTOM_ACCOUNT


async def get_custom_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menerima custom account dari user"""
    custom_account = update.message.text.strip()
    
    # Validasi custom account
    if len(custom_account) < 3:
        await update.message.reply_text(
            "❌ Username harus minimal 3 karakter!\n"
            "Silakan coba lagi:"
        )
        return CUSTOM_ACCOUNT
    
    if not custom_account.replace('_', '').replace('-', '').isalnum():
        await update.message.reply_text(
            "❌ Username hanya boleh mengandung huruf, angka, underscore (_) dan dash (-)!\n"
            "Silakan coba lagi:"
        )
        return CUSTOM_ACCOUNT
    
    context.user_data['custom_account'] = custom_account
    
    await update.message.reply_text(
        "🔐 Sekarang buat password untuk akun Anda.\n\n"
        "Password harus mengandung:\n"
        "• Minimal 8 karakter\n"
        "• Huruf besar dan kecil\n"
        "• Angka\n\n"
        "Masukkan password:"
    )
    
    return PASSWORD


async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menerima password dari user"""
    password = update.message.text.strip()
    
    # Validasi password
    if len(password) < 8:
        await update.message.reply_text(
            "❌ Password minimal 8 karakter!\n"
            "Silakan coba lagi:"
        )
        return PASSWORD
    
    if not any(c.isupper() for c in password):
        await update.message.reply_text(
            "❌ Password harus mengandung huruf besar!\n"
            "Silakan coba lagi:"
        )
        return PASSWORD
    
    if not any(c.islower() for c in password):
        await update.message.reply_text(
            "❌ Password harus mengandung huruf kecil!\n"
            "Silakan coba lagi:"
        )
        return PASSWORD
    
    if not any(c.isdigit() for c in password):
        await update.message.reply_text(
            "❌ Password harus mengandung angka!\n"
            "Silakan coba lagi:"
        )
        return PASSWORD
    
    context.user_data['password'] = password
    
    # Tampilkan konfirmasi
    summary = (
        "📋 Konfirmasi Data Registrasi\n\n"
        f"📱 Nomor HP: {context.user_data.get('phone')}\n"
        f"👤 Username: {context.user_data.get('custom_account')}\n"
        f"🔐 Password: {'*' * len(password)}\n\n"
        "Data sudah benar? Ketik 'ya' untuk melanjutkan atau 'tidak' untuk membatalkan:"
    )
    
    await update.message.reply_text(summary)
    
    return CONFIRM


async def confirm_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Konfirmasi dan proses registrasi akhir"""
    confirmation = update.message.text.strip().lower()
    
    if confirmation not in ['ya', 'yes', 'y']:
        if confirmation in ['tidak', 'no', 'n']:
            await update.message.reply_text(
                "Registrasi dibatalkan. Gunakan /start untuk memulai dari awal."
            )
            return ConversationHandler.END
        else:
            await update.message.reply_text(
                "Silakan ketik 'ya' untuk melanjutkan atau 'tidak' untuk membatalkan:"
            )
            return CONFIRM
    
    # Bind custom account melalui API
    user_id = str(context.user_data.get('user_id'))
    custom_account = context.user_data.get('custom_account')
    password = context.user_data.get('password')
    phone = context.user_data.get('phone')
    session_id = context.user_data.get('session_id')
    
    result = api_client.bind_custom_account(user_id, custom_account, password)
    
    if not result.get('success'):
        await update.message.reply_text(
            f"❌ Gagal membuat custom account.\n\n"
            f"Error: {result.get('error')}\n\n"
            f"Silakan coba lagi dengan /start"
        )
        return ConversationHandler.END
    
    # Update user status menjadi verified
    user_db.update_user(context.user_data['user_id'], status="verified")
    session_db.update_session(session_id, step="completed")
    
    await update.message.reply_text(
        "🎉 Selamat! Registrasi berhasil!\n\n"
        f"✅ Akun Anda telah berhasil dibuat.\n\n"
        f"📱 Nomor HP: {phone}\n"
        f"👤 Username: {custom_account}\n\n"
        f"Anda sekarang bisa login menggunakan username dan password tersebut.\n\n"
        f"Gunakan /help untuk melihat perintah lainnya.",
        reply_markup=ReplyKeyboardRemove()
    )
    
    logger.info(f"User {context.user_data['user_id']} berhasil registrasi dengan nomor {phone}")
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel registrasi"""
    session_id = context.user_data.get('session_id')
    if session_id:
        session_db.delete_session(session_id)
    
    await update.message.reply_text(
        "Registrasi dibatalkan. Gunakan /start untuk memulai lagi.",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command /help"""
    await update.message.reply_text(
        "📖 Daftar Perintah:\n\n"
        "/start - Mulai proses registrasi\n"
        "/status - Cek status registrasi Anda\n"
        "/help - Tampilkan bantuan ini\n\n"
        "Jika ada masalah, hubungi support kami."
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command /status - Cek status user"""
    user = update.effective_user
    user_data = user_db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text(
            "ℹ️ Anda belum terdaftar. Gunakan /start untuk memulai registrasi."
        )
        return
    
    status_emoji = {
        "pending": "⏳",
        "otp_verified": "📱",
        "verified": "✅"
    }
    
    status_text = {
        "pending": "Menunggu verifikasi OTP",
        "otp_verified": "OTP Terverifikasi",
        "verified": "Akun Terverifikasi"
    }
    
    status = user_data.get("status", "unknown")
    
    await update.message.reply_text(
        f"📊 Status Registrasi Anda:\n\n"
        f"{status_emoji.get(status, '❓')} {status_text.get(status, 'Tidak diketahui')}\n\n"
        f"Nomor HP: {user_data.get('phone')}\n"
        f"Terdaftar: {user_data.get('created_at', 'N/A')}"
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")


def main() -> None:
    """Start the bot"""
    
    # Get token dari environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di .env")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Setup conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            OTP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_otp)],
            CUSTOM_ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_custom_account)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_registration)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_error_handler(error_handler)
    
    # Start bot
    logger.info("Bot sedang berjalan...")
    application.run_polling()


if __name__ == '__main__':
    main()
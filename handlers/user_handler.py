# User Handler - Main bot logic
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from utils.api_client import APIClient

# Conversation states
START, BIND_PHONE, BIND_PASSWORD, REAL_PHONE, OTP_CODE, CONFIRM = range(6)

class UserHandler:
    def __init__(self):
        self.user_sessions = {}  # {user_id: {session_data}}
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Command /start - mulai registrasi"""
        user_id = update.effective_user.id
        
        keyboard = [
            ['🚀 Mulai Registrasi', '❌ Batal']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        
        await update.message.reply_text(
            "👋 Selamat datang di Registration Bot!\n\n"
            "Bot ini akan membantu Anda registrasi otomatis di h5.bigwinner10.com\n\n"
            "Proses:\n"
            "1️⃣ Bind akun dengan nomor acak\n"
            "2️⃣ Verifikasi dengan nomor asli\n"
            "3️⃣ Input OTP dari SMS\n\n"
            "Mulai? 🚀",
            reply_markup=reply_markup
        )
        
        return START
    
    async def confirm_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle konfirmasi mulai"""
        if '🚀' in update.message.text:
            user_id = update.effective_user.id
            self.user_sessions[user_id] = {
                'api_client': APIClient(),
                'step': 'bind_phone'
            }
            
            await update.message.reply_text(
                "📱 Masukkan nomor telepon acak untuk BIND ACCOUNT\n"
                "(Nomor ini bisa apa saja, tidak perlu nyata)\n\n"
                "Contoh: 08123456789 atau 123456789",
                reply_markup=ReplyKeyboardRemove()
            )
            return BIND_PHONE
        else:
            await update.message.reply_text("❌ Registrasi dibatalkan")
            return ConversationHandler.END
    
    async def handle_bind_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle input nomor untuk bind"""
        user_id = update.effective_user.id
        phone = update.message.text.strip()
        
        if not phone.replace('+', '').replace('-', '').isdigit():
            await update.message.reply_text(
                "❌ Format nomor tidak valid!\n"
                "Gunakan format: 08123456789 atau +628123456789"
            )
            return BIND_PHONE
        
        self.user_sessions[user_id]['bind_phone'] = phone
        
        await update.message.reply_text(
            "🔐 Masukkan PASSWORD untuk bind account\n"
            "(Password apapun, minimal 6 karakter)"
        )
        return BIND_PASSWORD
    
    async def handle_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle input password"""
        user_id = update.effective_user.id
        password = update.message.text.strip()
        
        if len(password) < 6:
            await update.message.reply_text(
                "❌ Password terlalu pendek!\n"
                "Minimal 6 karakter"
            )
            return BIND_PASSWORD
        
        self.user_sessions[user_id]['password'] = password
        
        # Show preview
        bind_phone = self.user_sessions[user_id]['bind_phone']
        
        keyboard = [['✅ Benar', '❌ Ubah']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        
        await update.message.reply_text(
            f"📋 Konfirmasi data BIND:\n\n"
            f"📱 Nomor: {bind_phone}\n"
            f"🔐 Password: {'*' * len(password)}\n\n"
            f"Lanjut? (Tunggu... saya masih perlu find sign parameter)",
            reply_markup=reply_markup
        )
        return CONFIRM
    
    async def confirm_bind(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle konfirmasi bind"""
        user_id = update.effective_user.id
        
        if '✅' in update.message.text:
            await update.message.reply_text(
                "⏳ Processing bind account...\n\n"
                "⚠️ CATATAN: Sign parameter masih belum bisa di-generate otomatis\n"
                "Tunggu saya finish reverse-engineer algoritma sign-nya!",
                reply_markup=ReplyKeyboardRemove()
            )
            
            # TODO: Execute bind_custom_account dengan sign parameter
            # Untuk sekarang cuma placeholder
            
            await update.message.reply_text(
                "✅ (Simulasi) Bind account berhasil!\n\n"
                "Sekarang masukkan nomor telepon ASLI untuk verifikasi OTP"
            )
            return REAL_PHONE
        else:
            await update.message.reply_text("📝 Silakan input ulang")
            return BIND_PASSWORD
    
    async def handle_real_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle input nomor asli"""
        user_id = update.effective_user.id
        phone = update.message.text.strip()
        
        if not phone.startswith('+'):
            phone = '+62' + phone.lstrip('0')
        
        self.user_sessions[user_id]['real_phone'] = phone
        
        keyboard = [['✅ Kirim OTP', '❌ Ubah']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        
        await update.message.reply_text(
            f"📱 Nomor verifikasi: {phone}\n\n"
            f"Kirim OTP ke nomor ini?",
            reply_markup=reply_markup
        )
        return OTP_CODE
    
    async def send_otp(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle send OTP"""
        user_id = update.effective_user.id
        
        if '✅' in update.message.text:
            await update.message.reply_text(
                "⏳ Mengirim OTP...\n\n"
                "⚠️ CATATAN: Fitur send OTP juga masih pending sign parameter",
                reply_markup=ReplyKeyboardRemove()
            )
            
            # TODO: Execute request_otp dengan sign parameter
            
            await update.message.reply_text(
                "✅ OTP telah dikirim ke nomor Anda!\n\n"
                "📱 Cek SMS Anda dan masukkan kode OTP (6 digit)"
            )
            return OTP_CODE
        else:
            await update.message.reply_text("📝 Masukkan nomor lagi")
            return REAL_PHONE
    
    async def handle_otp(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle input OTP"""
        user_id = update.effective_user.id
        otp = update.message.text.strip()
        
        if not otp.isdigit() or len(otp) != 6:
            await update.message.reply_text(
                "❌ OTP harus 6 digit angka!\n\n"
                "Coba lagi:"
            )
            return OTP_CODE
        
        self.user_sessions[user_id]['otp'] = otp
        
        await update.message.reply_text(
            f"⏳ Verifikasi OTP: {otp}...\n\n"
            f"⚠️ CATATAN: Verify OTP juga pending sign parameter"
        )
        
        # TODO: Execute verify_otp dengan sign parameter
        
        await update.message.reply_text(
            "✅ REGISTRASI BERHASIL!\n\n"
            "🎉 Akun Anda sudah fully registered\n\n"
            "Username: [akan ditampilkan]"
        )
        
        return ConversationHandler.END
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle cancel"""
        await update.message.reply_text(
            "❌ Registrasi dibatalkan",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

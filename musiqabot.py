import os
import uuid
import telebot
from yt_dlp import YoutubeDL

# --- Sozlamalar ---
# DIQQAT: Tokeningizni xavfsiz joyda saqlang!
BOT_TOKEN = "7999488160:AAELMfAdCoKAuXl3WSbXRL64lBDYGo1q_CU"
bot = telebot.TeleBot(BOT_TOKEN)

CHANNEL_USERNAME = "@aclubnc"
AD_TEXT = "📥 @NMusiqaBot orqali yuklab olindi"

# --- Obuna tekshirish ---
def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["creator", "administrator", "member"]
    except:
        return True

@bot.message_handler(commands=["start"])
def start(message):
    if not check_sub(message.from_user.id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📢 Kanalga obuna bo‘ling", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}"))
        markup.add(telebot.types.InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_sub"))
        bot.send_message(message.chat.id, f"❗ Botdan foydalanish uchun kanalga obuna bo‘ling: {CHANNEL_USERNAME}", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Xush kelibsiz! 🚀\n\nYouTube yoki Instagram havolasini yuboring, men uni video shaklida yuklab beraman.")

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    if not check_sub(message.from_user.id): 
        return start(message)
    
    text = message.text.strip()
    
    if "instagram.com" in text or "youtube.com" in text or "youtu.be" in text:
        download_video(message)
    else:
        bot.send_message(message.chat.id, "❌ Iltimos, faqat YouTube yoki Instagram havolasini yuboring.")

def download_video(message):
    status = bot.send_message(message.chat.id, "⏳ Video tayyorlanmoqda...")
    filename = f"downloads/{uuid.uuid4()}.mp4"
    
    # Yuklash sozlamalari (Faqat video)
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": filename,
        "quiet": True,
        "extractor_args": {"youtube": ["player_client=default"]}
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        
        with open(filename, "rb") as video:
            bot.send_video(message.chat.id, video, caption=AD_TEXT)
        
        bot.delete_message(message.chat.id, status.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xatolik yuz berdi: Havola noto'g'ri yoki video juda katta.", message.chat.id, status.message_id)
    
    finally:
        if os.path.exists(filename):
            os.remove(filename)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(call):
    if check_sub(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Rahmat! Endi havolani yuborishingiz mumkin. ✅")
    else:
        bot.answer_callback_query(call.id, "Hali obuna bo'lmagansiz! ❌", show_alert=True)

if __name__ == "__main__":
    if not os.path.exists("downloads"): 
        os.makedirs("downloads")
    
    print("🚀 Bot faqat VIDEO yuklash rejimida ishga tushdi...")
    bot.remove_webhook()
    bot.infinity_polling()
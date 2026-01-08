import os
import uuid
import telebot
from yt_dlp import YoutubeDL

# --- Sozlamalar ---
BOT_TOKEN = "7999488160:AAELMfAdCoKAuXl3WSbXRL64lBDYGo1q_CU"
bot = telebot.TeleBot(BOT_TOKEN)

AD_TEXT = "📥 @NMusiqaBot orqali yuklab olindi"

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Xush kelibsiz! 🚀\n\nYouTube yoki Instagram havolasini yuboring, men uni video formatida yuklab beraman."
    )

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    text = message.text.strip()
    
    # Havolani tekshirish
    if "instagram.com" in text or "youtube.com" in text or "youtu.be" in text:
        download_video(message)
    else:
        bot.send_message(message.chat.id, "❌ Iltimos, faqat YouTube yoki Instagram havolasini yuboring.")

def download_video(message):
    status = bot.send_message(message.chat.id, "⏳ Video tayyorlanmoqda...")
    
    # Fayl uchun takrorlanmas nom va yo'l
    filename = f"downloads/{uuid.uuid4()}.mp4"
    
    # Yuklash sozlamalari
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": filename,
        "quiet": True,
        "extractor_args": {"youtube": ["player_client=default"]}
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        
        # Videoni yuborish
        with open(filename, "rb") as video:
            bot.send_video(message.chat.id, video, caption=AD_TEXT)
        
        bot.delete_message(message.chat.id, status.message_id)
        
    except Exception as e:
        bot.edit_message_text(
            "❌ Xatolik yuz berdi: Havola noto'g'ri, video o'chirilgan yoki juda katta (50MB+).", 
            message.chat.id, 
            status.message_id
        )
    
    finally:
        # Faylni serverdan o'chirish (joy tejash uchun)
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    # Yuklanadigan fayllar uchun papka yaratish
    if not os.path.exists("downloads"): 
        os.makedirs("downloads")
    
    print("🚀 Bot ishga tushdi (Faqat Video rejimida, obuna talab qilinmaydi)...")
    bot.remove_webhook()
    bot.infinity_polling()
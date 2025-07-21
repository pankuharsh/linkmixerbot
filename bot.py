from telegram.ext import Application, CommandHandler, MessageHandler, Filters
from telegram import Update
import os

# BotFather से मिला टोकन (Heroku से लिया जाएगा)
TOKEN = os.environ.get('TOKEN')  # Heroku से टोकन लेगा
PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')

# /start कमांड
async def start(update: Update, context):
    await update.message.reply_text(
        "हाय! मैं आपका Link Mixer Bot हूँ। मुझे एक लिंक और इमेज/वीडियो भेजें, मैं उसे आकर्षक पोस्ट में बदल दूंगा! 😎\n"
        "जानकारी के लिए /help टाइप करें।"
    )

# /help कमांड
async def help_command(update: Update, context):
    await update.message.reply_text(
        "🔥 बॉट का उपयोग कैसे करें:\n"
        "1. मुझे एक लिंक (URL) भेजें。\n"
        "2. उसी मैसेज में एक इमेज या वीडियो अटैच करें。\n"
        "3. मैं आपके लिंक और अटैचमेंट को इस फॉर्मेट में पोस्ट करूंगा:\n\n"
        "👀 watch & play 👇\n"
        "📥 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤𝐬/👀𝐖𝐚𝐭𝐚𝐭𝐜𝐡 𝐎𝐧𝐥𝐢𝐧𝐞 🥵\n\n"
        "👇👇 𝑽𝑰𝑫𝑬𝑶 👇👇\n"
        "[आपका लिंक]\n\n"
        "Injoy full video ❤️❤️❤️🥵\n"
        "Check ✅ now 🥰👆\n\n"
        "ग्रुप में उपयोग के लिए मुझे एडमिन बनाएं।"
    )

# लिंक और अटैचमेंट हैंडल करें
async def handle_message(update: Update, context):
    message = update.message
    chat_id = message.chat_id
    link = None
    media = None

    if message.text:
        link = message.text.strip()
    if message.photo:
        media = message.photo[-1].file_id
    elif message.video:
        media = message.video.file_id

    if link and media:
        formatted_message = (
            "👀 watch & play 👇\n"
            "📥 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤𝐬/👀𝐖𝐚𝐭𝐚𝐭𝐜𝐡 𝐎𝐧𝐥𝐢𝐧𝐞 🥵\n\n"
            "👇👇 𝑽𝑰𝑫𝑬𝑶 👇👇\n"
            f"{link}\n\n"
            "Injoy full video ❤️❤️❤️🥵\n"
            "Check ✅ now 🥰👆"
        )
        if message.photo:
            await context.bot.send_photo(chat_id, photo=media, caption=formatted_message, parse_mode="Markdown")
        elif message.video:
            await context.bot.send_video(chat_id, video=media, caption=formatted_message, parse_mode="Markdown")
    elif message.text and not message.photo and not message.video:
        await message.reply_text("कृपया एक इमेज या वीडियो भी अटैच करें।")
    elif (message.photo or message.video) and not message.text:
        await message.reply_text("कृपया एक लिंक भी भेजें।")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.video, handle_message))
    application.run_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")

if __name__ == "__main__":
    main()
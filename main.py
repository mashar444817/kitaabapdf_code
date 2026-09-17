import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Token Bot kee
TOKEN = "8642487524:AAGUSFZGta5jUIh367PsVsCvLIQjLk3VIr0"
bot = telebot.TeleBot(TOKEN)

# Odeeffannoo Telebirr Merchant/Account
MERCHANT_NAME = "Masher Nesha Wodajo"
MERCHANT_PHONE = "+251906236951"

PRICE_10 = "$10 (Kitaaba Page 15 hanga 500 Qabu)"
PRICE_6 = "$6 (Kitaaba Page 15 Gadi)"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    
    # Button kaffaltii booda si quunnamuuf
    btn_contact = InlineKeyboardButton("💬 Kaffaluun Na Quunamaa (Screenshot Ergaa)", url=f"https://t.me/MasherNesha")
    markup.add(btn_contact)
    
    welcome_text = (
        f"Baga nagaan dhuftan! 🙏\n\n"
        f"Kitaabota PDF bituuf qophoofte:\n"
        f"1️⃣ Kitaaba Page 15 hanga 500 qabu: **{PRICE_10}**\n"
        f"2️⃣ Kitaaba Page 15 gadi: **{PRICE_6}**\n\n"
        f"📌 **Akkaataa Kaffaltii Telebirr:**\n"
        f"Qarshii barbaachisu karaa Telebirr herrega armaan gadiitti ergatanii suuraa (Screenshot) naaf ergaa:\n\n"
        f"• **Maqaa Account:** {MERCHANT_NAME}\n"
        f"• **Lakkoofsa Telebirr:** {MERCHANT_PHONE}\n\n"
        f"Kaffaltee xumuruun mirkaneessuuf Button gadii tuqaa:"
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Tajaajila argachuuf ajaja /start fayyadamaa, ykn kaffaltii raawwachuudhaan suuraa kaffaltii keessanii asumaan naaf ergaa.")

if __name__ == "__main__":
    print("Bot-ichi hojii jalqabeera...")
    bot.infinity_polling()

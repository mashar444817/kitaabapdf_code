import os
import re
import time
import threading

import requests
import telebot
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------- Qindaa'ina (Environment variables irraa) ----------
TOKEN = os.getenv("BOT_TOKEN")
CHAPA_PAYMENT_LINK = os.getenv("CHAPA_PAYMENT_LINK")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # Telegram ID kee (lakkoofsa)

if not TOKEN:
    raise SystemExit("BOT_TOKEN hin qabamne. Environment variable keessatti galchi.")

bot = telebot.TeleBot(TOKEN)

# ---------- Odeeffannoo Telebirr ----------
MERCHANT_NAME = "Masher Nesha Wodajo"
MERCHANT_PHONE = "+251906236951"
CONTACT_URL = "https://t.me/MasherNesha"

PRICE_10 = "$10 (Kitaaba Page 15 hanga 500 Qabu)"
PRICE_6 = "$6 (Kitaaba Page 15 Gadi)"


# ---------- Akka hin rafneef (Render Free) ----------
web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot hojii irra jira ✅"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


def keep_alive():
    """Daqiiqaa 10 hundaa URL Render ofii ping godha, akka hin rafneef."""
    url = os.environ.get("RENDER_EXTERNAL_URL")
    if not url:
        return
    while True:
        time.sleep(600)
        try:
            requests.get(url, timeout=15)
        except Exception:
            pass


# ---------- /start ----------
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    if CHAPA_PAYMENT_LINK:
        markup.add(InlineKeyboardButton("💳 Chapaadhaan Kaffali (Online)", url=CHAPA_PAYMENT_LINK))
    markup.add(InlineKeyboardButton("💬 Kaffaluun Na Quunnamaa", url=CONTACT_URL))

    welcome_text = (
        "Baga nagaan dhuftan! 🙏\n\n"
        "Kitaabota PDF bituuf qophoofte:\n"
        f"1️⃣ Kitaaba Page 15 hanga 500 qabu: *{PRICE_10}*\n"
        f"2️⃣ Kitaaba Page 15 gadi: *{PRICE_6}*\n\n"
        "📌 *Akkaataa Kaffaltii:*\n"
        "🔹 *Karaa Chapa (Online):* Button armaan gadii tuquun kallattiidhaan kaffaluu dandeessa.\n"
        "🔹 *Karaa Telebirr:* Qarshii herrega armaan gadiitti ergatanii suuraa (Screenshot) asuma naaf ergaa:\n\n"
        f"• *Maqaa Account:* {MERCHANT_NAME}\n"
        f"• *Lakkoofsa Telebirr:* {MERCHANT_PHONE}\n\n"
        "Suuraa kaffaltii ergitanii booda, kitaabni PDF ni ergama. ✅"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")


# ---------- Suuraa kaffaltii (Screenshot) yoo namni erge ----------
@bot.message_handler(content_types=["photo"])
def handle_payment_photo(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "(username hin qabu)"

    bot.reply_to(message, "Suuraa kaffaltii keessan argameera ✅\nDuubatti mirkaneessinee kitaabni isinii ergama. Obsaan eegaa 🙏")

    if not ADMIN_ID:
        return

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Mirkaneessi", callback_data=f"ok_{user.id}"),
        InlineKeyboardButton("❌ Didi", callback_data=f"no_{user.id}"),
    )
    caption = (
        f"💰 Kaffaltii haaraa\n"
        f"Maqaa: {user.first_name}\n"
        f"Username: {username}\n"
        f"ID: {user.id}\n\n"
        f"Mirkaneessee booda, PDF kana suuraa kanaaf Reply godhii ergi."
    )
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, reply_markup=markup)


# ---------- Admin: Mirkaneessuu ykn Didu ----------
@bot.callback_query_handler(func=lambda call: call.data.startswith(("ok_", "no_")))
def handle_decision(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Hayyama hin qabdu.")
        return

    action, user_id = call.data.split("_", 1)
    user_id = int(user_id)

    if action == "ok":
        bot.send_message(user_id, "✅ Kaffaltiin keessan mirkanaa'eera! Kitaabni PDF yeroo gabaabaa keessatti isinii ergama. Galatoomaa! 🙏")
        status = "✅ Mirkanaa'e"
    else:
        bot.send_message(user_id, "❌ Kaffaltiin hin mirkanoofne. Maaloo suuraa sirrii ergaa ykn nu quunnamaa: " + CONTACT_URL)
        status = "❌ Ni didame"

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.answer_callback_query(call.id, status)


# ---------- Admin: PDF suuraa kaffaltii irratti Reply godhee erga ----------
@bot.message_handler(content_types=["document"])
def admin_send_pdf(message):
    if message.from_user.id != ADMIN_ID:
        return

    replied = message.reply_to_message
    text = (replied.caption or replied.text or "") if replied else ""
    match = re.search(r"ID:\s*(\d+)", text)

    if not match:
        bot.reply_to(message, "PDF ergachuuf, suuraa kaffaltii irratti *Reply* godhii ergi.", parse_mode="Markdown")
        return

    buyer_id = int(match.group(1))
    bot.send_document(buyer_id, message.document.file_id, caption="📚 Kitaaba keessan. Galatoomaa! 🙏")
    bot.reply_to(message, "PDF nama sanaaf ergameera ✅")


# ---------- Ergaa kaan hundaaf ----------
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(
        message,
        "Tajaajila argachuuf ajaja /start fayyadamaa, ykn kaffaltii raawwachuudhaan suuraa kaffaltii keessanii asumaan naaf ergaa.",
    )


if __name__ == "__main__":
    print("Bot-ichi hojii jalqabeera...")
    threading.Thread(target=run_web, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    bot.infinity_polling()

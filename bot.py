import telebot

TOKEN = "8931751356:AAEgs-y1iLoOX4mKEARtsZWzw3kWb8ducfQ"

ADMIN_IDS = [856556957, 410686938]

bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Ism-familiyangizni kiriting:")

@bot.message_handler(content_types=['text'])
def text_handler(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    data = user_data[chat_id]

    if "ism" not in data:
        data["ism"] = message.text
        bot.send_message(chat_id, "Yoshingizni kiriting:")
    elif "yosh" not in data:
        data["yosh"] = message.text
        bot.send_message(chat_id, "Telefon raqamingizni kiriting:")
    elif "telefon" not in data:
        data["telefon"] = message.text
        bot.send_message(chat_id, "Manzilingizni kiriting:")
    elif "manzil" not in data:
        data["manzil"] = message.text
        bot.send_message(chat_id, "Qaysi lavozim uchun murojaat qilyapsiz?")
    elif "lavozim" not in data:
        data["lavozim"] = message.text
        bot.send_message(chat_id, "Ish tajribangizni yozing:")
    elif "tajriba" not in data:
        data["tajriba"] = message.text
        bot.send_message(chat_id, "Rasmingizni yuboring:")

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    data = user_data[chat_id]

    text = f"""
📋 Yangi anketa

👤 Ism: {data['ism']}
🎂 Yosh: {data['yosh']}
📞 Telefon: {data['telefon']}
🏠 Manzil: {data['manzil']}
💼 Lavozim: {data['lavozim']}
📄 Tajriba: {data['tajriba']}
"""

    for admin_id in ADMIN_IDS:
        bot.send_message(admin_id, text)

    photo_id = message.photo[-1].file_id

    for admin_id in ADMIN_IDS:
        bot.send_photo(admin_id, photo_id)

bot.send_message(chat_id, "Anketangiz muvaffaqiyatli qabul qilindi, tez orada siz bilan bog'lanishadi.")

del user_data[chat_id]

bot.infinity_polling()

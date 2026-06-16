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
        bot.send_message(chat_id, "Ish tajribangiz haqida ma'lumot bering (matn yoki rasm/rezyume yuborishingiz mumkin):")

    elif "tajriba" not in data:
        data["tajriba"] = message.text
        bot.send_message(chat_id, "Endi anketangiz uchun rasmingizni yuboring:")


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    data = user_data[chat_id]

    # Agar foydalanuvchi tajribasini yozmasdan turib rasm yuborgan bo'lsa, uni tajriba o'rniga qabul qilmaslik uchun tekshiramiz
    if "lavozim" not in data:
        bot.send_message(chat_id, "Iltimos, avval lavozimni kiriting.")
        return

    # Agar tajriba matni kiritilmagan bo'lsa va to'g'ridan-to'g'ri rasm yuborilsa
    if "tajriba" not in data:
        data["tajriba"] = "Rasm ko'rinishida yuborildi"

    text = f"""
📋 Yangi anketa

👤 Ism: {data.get('ism', 'Kiritilmagan')}
🎂 Yosh: {data.get('yosh', 'Kiritilmagan')}
📞 Telefon: {data.get('telefon', 'Kiritilmagan')}
🏠 Manzil: {data.get('manzil', 'Kiritilmagan')}
💼 Lavozim: {data.get('lavozim', 'Kiritilmagan')}
📄 Tajriba: {data.get('tajriba', 'Kiritilmagan')}
"""

    # Adminlarga matnli anketani yuborish
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(admin_id, text)
        except Exception as e:
            print(f"Adminga xabar yuborishda xatolik: {e}")

    # Adminlarga rasmni yuborish
    photo_id = message.photo[-1].file_id
    for admin_id in ADMIN_IDS:
        try:
            bot.send_photo(admin_id, photo_id)
        except Exception as e:
            print(f"Adminga rasm yuborishda xatolik: {e}")

    # Foydalanuvchiga muvaffaqiyatli yakunlangani haqida xabar
    bot.send_message(
        chat_id,
        "✅ Anketangiz muvaffaqiyatli yuborildi. Tez orada siz bilan bog'lanamiz."
    )

    # Foydalanuvchi ma'lumotlarini keshdan o'chirish (tozalash)
    if chat_id in user_data:
        del user_data[chat_id]


bot.infinity_polling()



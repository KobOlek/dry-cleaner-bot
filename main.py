from config import *
import telebot
from telebot import types

bot = telebot.TeleBot(TOKEN)
phone_number = ""


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Поділитись номером", request_contact=True)
    markup.add(item1)

    bot.send_message(message.chat.id,
                     f"Привіт, {message.from_user.first_name}, виберіть функцію, якою хочете скористатись",
                     reply_markup=markup)


@bot.message_handler(content_types=["contact"])
def bot_message_after_registration(message):
    global phone_number
    phone_number = message.contact.phone_number
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("⚙")
    item2 = types.KeyboardButton("ЧАТ")
    item3 = types.KeyboardButton("❤ Поділитися")
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Оберіть потрібну дію у меню, що знаходиться нижче", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def bot_message(message):
    global phone_number
    if message.text == "⚙":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Акаунт")
        item2 = types.KeyboardButton("Оновити номер")
        item3 = types.KeyboardButton("Видалити дані")
        back = types.KeyboardButton("⇐Назад")
        markup.add(item1, item2, item3)
        markup.add(back)

        bot.send_message(message.chat.id, f"Налаштування по номеру *{phone_number}*", reply_markup=markup,
                         parse_mode="Markdown")
    elif message.text == "Акаунт":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⚙")
        item2 = types.KeyboardButton("ЧАТ")
        item3 = types.KeyboardButton("❤ Поділитися")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, f"Ім'я: {message.from_user.first_name}\nНомер телефону: +{phone_number}",
                         reply_markup=markup)

    elif message.text == "Оновити номер":
        phone_number = ""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Поділитись номером", request_contact=True)
        markup.add(item1)
        bot.send_message(message.chat.id, "Надішліть свій номер", reply_markup=markup)

    elif message.text == "Видалити дані":
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Видалити дані", callback_data="delete")
        item2 = types.InlineKeyboardButton("Відмінити", callback_data="refuse")
        markup.add(item1)
        markup.add(item2)

        bot.send_message(message.chat.id, "Натисніть кнопку *Видалити*, щоб видалити дані", parse_mode="Markdown",
                         reply_markup=markup)

    elif message.text == "ЧАТ":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Гаряча лінія")
        item2 = types.KeyboardButton("Пропозиції і скарги")
        back = types.KeyboardButton("⇐Назад")
        markup.add(item1, item2)
        markup.add(back)

        bot.send_message(message.chat.id, "Виберіть категорію звернення:", reply_markup=markup)

    elif message.text == "Гаряча лінія":
        bot.send_message(message.chat.id, "Напишіть своє повідомлення на гарячу лінію")

    elif message.text == "Пропозиції і скарги":
        bot.send_message(message.chat.id, "Напишіть свої пропозиції або скарги")

    elif message.text == "❤ Поділитися":
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Головне меню", callback_data="main_menu")
        item2 = types.InlineKeyboardButton("Поділитися", switch_inline_query="http://t.me/larrary_bot")
        markup.add(item1)
        markup.add(item2)

        bot.send_message(message.chat.id, "Натисніть кнопку 'Поділитись'", reply_markup=markup)

    elif message.text == "⇐Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⚙")
        item2 = types.KeyboardButton("ЧАТ")
        item3 = types.KeyboardButton("❤ Поділитися")
        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, "Оберіть потрібну дію у меню, що знаходиться нижче", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⚙")
        item2 = types.KeyboardButton("ЧАТ")
        item3 = types.KeyboardButton("❤ Поділитися")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, "Дякую за повідомлення", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global phone_number
    if call.message:
        if call.data == "main_menu":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("⚙")
            item2 = types.KeyboardButton("ЧАТ")
            item3 = types.KeyboardButton("❤ Поділитися")
            markup.add(item1, item2, item3)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="Натисніть кнопку 'Поділитись'")
            bot.send_message(call.message.chat.id, "Оберіть потрібну дію у меню, що знаходиться нижче",
                             reply_markup=markup)
        elif call.data == "delete":
            phone_number = ""
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Поділитись номером", request_contact=True)
            markup.add(item1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Ви видалили дані")
            bot.send_message(call.message.chat.id, "Повертайтеся!", reply_markup=markup)
        elif call.data == "refuse":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("⚙")
            item2 = types.KeyboardButton("ЧАТ")
            item3 = types.KeyboardButton("❤ Поділитися")
            markup.add(item1, item2, item3)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="Ви відмінили видалення даних")
            bot.send_message(call.message.chat.id, "Дякуємо, що залишаєтесь з нами", reply_markup=markup)


bot.infinity_polling()
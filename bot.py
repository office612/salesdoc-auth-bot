import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

BOT_TOKEN = os.getenv("BOT_TOKEN", "8670581466:AAFUkWwvSK37CsGBnzBGHSpjZ_C0HVhREu8")
bot = telebot.TeleBot(BOT_TOKEN)

EMPLOYEES = [
    {"name": "Mirzahit",  "phone": "87479069426",  "login": "office@salesdoc.io", "pass": "admin"},
    {"name": "Aidos",     "phone": "870558071188", "login": "aidosh",             "pass": "1234"},
    {"name": "Yulia",     "phone": "87471203744",  "login": "yulia",              "pass": "1234"},
    {"name": "Asem",      "phone": "",             "login": "asem",               "pass": "1234"},
    {"name": "Malika",    "phone": "",             "login": "malika",             "pass": "1234"},
    {"name": "Gulshan",   "phone": "",             "login": "gulshan",            "pass": "1234"},
    {"name": "Aurika",    "phone": "",             "login": "aurika",             "pass": "1234"},
]

def normalize(phone):
    d = "".join(filter(str.isdigit, str(phone)))
    if d.startswith("8"):
        d = "7" + d[1:]
    return d

def find_emp(phone):
    n = normalize(phone)
    for e in EMPLOYEES:
        if e["phone"] and normalize(e["phone"]) == n:
            return e
    return None

def share_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Share number", request_contact=True))
    return kb

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id,
        "SalesDoc Finance Portal - password recovery.\nPress button to share your phone.",
        reply_markup=share_kb())

@bot.message_handler(content_types=["contact"])
def contact(msg):
    emp = find_emp(msg.contact.phone_number)
    if emp:
        bot.send_message(msg.chat.id,
            f"Found!\nLogin: {emp['login']}\nPassword: {emp['pass']}",
            reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(msg.chat.id,
            "Not found. Contact: @Salesdockzkg",
            reply_markup=ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: True)
def fallback(msg):
    bot.send_message(msg.chat.id, "Press button below", reply_markup=share_kb())

bot.polling(none_stop=True)

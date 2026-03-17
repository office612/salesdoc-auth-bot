import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8670581466:AAFUkWwvSK37CsGBnzBGHSpjZ_C0HVhREu8")

EMPLOYEES = [
    {"name": "Mirzahit",  "phone": "87479069426",  "login": "office@salesdoc.io", "pass": "admin"},
    {"name": "Aidos",     "phone": "870558071188", "login": "aidosh",             "pass": "1234"},
    {"name": "Yulia",     "phone": "87471203744",  "login": "yulia",              "pass": "1234"},
    {"name": "Asem",      "phone": "",             "login": "asem",               "pass": "1234"},
    {"name": "Malika",    "phone": "",             "login": "malika",             "pass": "1234"},
    {"name": "Gulshan",   "phone": "",             "login": "gulshan",            "pass": "1234"},
    {"name": "Aurika",    "phone": "",             "login": "aurika",             "pass": "1234"},
]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def normalize_phone(phone):
    digits = "".join(filter(str.isdigit, phone))
    if digits.startswith("8"):
        digits = "7" + digits[1:]
    return digits

def find_employee(phone):
    normalized = normalize_phone(phone)
    for emp in EMPLOYEES:
        if emp["phone"] and normalize_phone(emp["phone"]) == normalized:
            return emp
    return None

@dp.message(CommandStart())
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Share number", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer("SalesDoc Finance Portal - password recovery.\nPress button to share your phone.", reply_markup=kb)

@dp.message(F.contact)
async def handle_contact(message: Message):
    emp = find_employee(message.contact.phone_number)
    if emp:
        await message.answer(f"Found!\nLogin: {emp['login']}\nPassword: {emp['pass']}", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Not found. Contact: @Salesdockzkg", reply_markup=ReplyKeyboardRemove())

@dp.message()
async def fallback(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Share number", request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Press button below", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

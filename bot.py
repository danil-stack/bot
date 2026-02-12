from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8338259169:AAFc0ZZcAZKHWjk0cnPLc4h_2JB1C4olmg0"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

WEB_APP_URL = "https://15woazc.atoms.world"
CHANNEL_URL = ""  # ← сюда вставишь ссылку на канал позже

PAYMENT_LINKS = {
    "500": "https://t.me/send?start=IVvxKYz3hEe3",
    "800": "https://t.me/send?start=IVhDv1s3oofZ",
    "1000": "https://t.me/send?start=IV2Vhhv0F2aK",
    "1500": "https://t.me/send?start=IV3bNfCxepP0",
    "2000": "https://t.me/send?start=IVBVAx5dKNsB",
    "3000": "https://t.me/send?start=IVulBbsZndnZ",
}

def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💳 Пополнить депозит", callback_data="deposit"),
        InlineKeyboardButton(
            "📱 Открыть Web App",
            web_app=WebAppInfo(url=WEB_APP_URL)
        ),
        InlineKeyboardButton("📢 Канал", url=CHANNEL_URL or "#")
    )
    return kb

def deposit_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    for amount in PAYMENT_LINKS.keys():
        kb.insert(
            InlineKeyboardButton(f"💵 {amount} USD", callback_data=f"pay_{amount}")
        )
    kb.add(InlineKeyboardButton("◀️ Назад", callback_data="back"))
    return kb

def back_button():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("◀️ Назад", callback_data="back"))
    return kb

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать 👋\nВыберите действие:",
        reply_markup=main_menu()
    )

@dp.callback_query_handler(lambda c: c.data == "deposit")
async def deposit(call: types.CallbackQuery):
    await call.message.edit_text(
        "Выберите сумму для пополнения страхового депозита:",
        reply_markup=deposit_menu()
    )

@dp.callback_query_handler(lambda c: c.data.startswith("pay_"))
async def pay(call: types.CallbackQuery):
    amount = call.data.split("_")[1]
    link = PAYMENT_LINKS.get(amount)

    text = (
        f"Для оплаты {amount} USD перейдите по ссылке:\n"
        f"{link}\n\n"
        "После успешной оплаты ваш депозит будет активирован автоматически.\n\n"
        "ℹ️ Если вам нужна сумма больше предложенных вариантов, "
        "пополните доступными вариантами несколько раз."
    )

    await call.message.edit_text(text, reply_markup=back_button())

@dp.callback_query_handler(lambda c: c.data == "back")
async def back(call: types.CallbackQuery):
    await call.message.edit_text(
        "Главное меню:",
        reply_markup=main_menu()
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

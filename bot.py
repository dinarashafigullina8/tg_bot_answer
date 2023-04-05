import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import IsReplyFilter

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1)
    await bot.send_message(message.chat.id,
                           text="Здравствуйте, {0.first_name}! Цифровые Виртульные Ассистенты приветствуют вас.Чем мы "
                                "можем вам помочь?".format(message.from_user), reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def ask_question(message: types.Message):
    global help_user_id
    help_user_id = message.from_user.id
    if message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        await bot.send_message(message.chat.id, text="Задайте свой вопрос", reply_markup=markup)
    else:
        await bot.send_message(-1001813610045, message.text)


# @dp.message_handler(IsReplyFilter(is_reply=True))
# async def handle_text(message: types.Message):
#     if message.chat.id == -1001813610045:
#         await bot.send_message(help_user_id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

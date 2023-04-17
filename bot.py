import os
from dotenv import load_dotenv, find_dotenv
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import IsReplyFilter
import send_mail
load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('token'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1)
    await bot.send_message(message.chat.id,
                           text="Здравствуйте, {0.first_name}! Цифровые Виртуальные Ассистенты приветствуют вас.Чем мы "
                                "можем вам помочь?".format(message.from_user), reply_markup=markup)


@dp.message_handler(IsReplyFilter(is_reply=True))
async def handle_text(message: types.Message):
    if message.chat.id == int(os.getenv('chat_id_operators')):
        await bot.send_message(help_user_id, message.text)


@dp.message_handler(content_types=['text'])
async def ask_question(message: types.Message):
    global help_user_id
    help_user_id = message.from_user.id
    if message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        await bot.send_message(message.chat.id, text="Задайте свой вопрос", reply_markup=markup)
    elif message.chat.id != int(os.getenv('chat_id_operators')):
        send_mail.main()
        await bot.send_message(message.chat.id, text="Ваш вопрос обрабатывается оператором. Ожидайте ответа")
        await bot.send_message(int(os.getenv('chat_id_operators')), text='Пришел новый вопрос от '
                                                    'пользователя {0.first_name}:'.format(message.from_user) + '\n\n'
                                                    + message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

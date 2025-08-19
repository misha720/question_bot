# from loguru import logger
import DataBase

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

# AIOGRAM
BOT_TOKEN = "8375169798:AAFfjT5_xf2OWuBxVQOFWx9xjmiTvwFlDzs"
ADMIN = [1020432840]  # Список админов
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# DataBase
db = DataBase.DataBase()



# Обработка Старта Бота
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    # Индификация пользователя
    for user_lot in db.users:
        # проверяем есть ли совпадение
        if user_lot["id"] == message.chat.id:
            if "recipient" in user_lot:
                db.users[db.get_index_user(message.chat.id)].pop('recipient',None)
                db.save_base()
            break
    else:
        # Пользователь не найден
        db.create_user(int(message.chat.id))

    # Захват ключа
    args = message.text.split()
    if len(args) == 2:
        # Ключ получен

        # Поиск ключа по базе
        if db.get_index_user(args[1]) != None:
            # Ключ получателя найден
            await bot.send_message(
                message.from_user.id,
                text="🚀 Здесь можно отправить анонимное сообщение человеку, который опубликовал эту ссылку\n\n🖊 Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше сообщение, но не будет знать от кого")

            # Даём пользователю индекс получателя
            db.users[db.get_index_user(message.chat.id)]['recipient'] = int(args[1])
            db.save_base()
        else:
            await bot.send_message(
                message.from_user.id,
                text="Возможно ссылка повреждена, попробуйте её справить")



# Обработка команды /get_url
@dp.message(F.text == "/get_url")
async def get_url(message: types.Message):

    sender_url = "http://t.me/ultra_anonim_question_bot?start=" + str(message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        text="Вот Ваша ссылка для получения анонимных сообщений:\n\n" + sender_url + "\n\nМожете её разместить в своей истории, Telegram-канале и тд.")


# Получение сообщения для получателя
@dp.message()
async def send_sms_user(message: types.Message):
    recipient_user = db.users[db.get_index_user(message.from_user.id)]['recipient']

    # Провека на существование получателя
    if recipient_user is not None:
        # добавляем сообщение в базу получателя
        new_question = {
            "sender":message.from_user.id,
            "text":message.text
        }
        db.users[db.get_index_user(recipient_user)]['question'].append(new_question)
        db.save_base()

        # Отчёт о отправке сообщения отправлителю
        await bot.send_message(
            message.from_user.id,
            text="Сообщение отправленно!\n\nЕсли хотите, можете продолжить писать следующие сообщения выбранному пользователю\n\nЧто бы сбросить выбранного собеседника, перезапустите бота командой '/start'")

        # Отчёт о полученом сообщении получателю
        await bot.send_message(
            recipient_user,
            text="Вы получили новое сообщение!\n\n" + message.text)
    else:
        await bot.send_message(
            message.from_user.id,
            text="Получатель не найден!\n\nЧто бы отправить сообщение пользователю, нужно перейти в бота по его ссылке.")



async def main() -> None:
    # Запускаем получение обновлений
    try:
        await dp.start_polling(bot)
    except Exception:
        print(Exception)


if __name__ == "__main__":
    asyncio.run(main())
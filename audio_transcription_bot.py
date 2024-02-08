import os

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Filter
from aiogram.filters.command import Command

from dotenv import load_dotenv

load_dotenv()
# Теперь переменная TOKEN, описанная в файле .env,
# доступна в пространстве переменных окружения

token = os.getenv('TOKEN')

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


class VoiceMessageFilter(Filter):
    async def __call__(self, message):
        return message.voice is not None


@dp.message(VoiceMessageFilter())
async def voice_message_handler(message):
    await message.answer("Received voice")
    try:
        voice_file_id = message.voice.file_id
        voice_file = await bot.get_file(voice_file_id)
        # print(message.voice.mime_type)
        await bot.download(message.voice, "./voice_messages.ogg")
        await message.answer("Got voice file")
    except:
        await message.answer("Failed to get voice file")


@dp.message()
async def other_message_handler(message):
    await message.answer("Received not voice")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

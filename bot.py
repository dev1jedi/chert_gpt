from gpt_api import gpt
from aiogram import Bot, Dispatcher, types, executor
from config import token

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"🤖 Привет, {message.from_user.first_name}, я Черт-GPT, бот, основанный на API openai и написанный гениальнейшим кодером всех времен! Я умею воспринимать как текстовые вопросы, так и голосовые сообщения. Задавай мне вопрос и я попытаюсь на него ответить", parse_mode="html")


@dp.message_handler()
async def chat(message: types.Message):
    m = await message.answer("Подождите... Чат бот обрабатывает ваш запрос...")
    api = gpt.chat_text(message.text)

    await bot.delete_message(m.chat.id, m.message_id)
    await message.answer(api)



@dp.message_handler(content_types=["voice"])
async def audio_chat(message: types.Message):
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id

        file = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file.file_path)

        with open(f"{message.from_user.id}.oga", "wb") as f:
            f.write(downloaded_file.getvalue())


        name = f"{message.from_user.id}.oga"

        m = await bot.send_message(message.chat.id, "Подождите... Чат бот обрабатывает ваш запрос...")

        api = gpt.chat_audio(name)
        await bot.delete_message(m.chat.id, m.message_id)
        await message.answer(api)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

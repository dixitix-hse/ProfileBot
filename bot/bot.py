import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from db import db

TOKEN = '5800804042:AAGc2pGppN-hpb3Sxng4tAwBUY1YTWoipT4'

bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    await db.db_connect()


class Profile(StatesGroup):
    name = State()
    age = State()
    gender = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await Profile.name.set()
    await message.reply("Привет! Как тебя зовут?")


@dp.message_handler(state=Profile.name)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Profile.next()
    await message.reply("Сколько тебе лет?")


@dp.message_handler(lambda message: not message.text.isdigit(), state=Profile.age)
async def age_invalid(message: types.Message):
    return await message.reply("Возраст должен быть числом.\nСколько тебе лет? (введи число, пожалуйста)")


@dp.message_handler(lambda message: message.text.isdigit(), state=Profile.age)
async def get_age(message: types.Message, state: FSMContext):
    await Profile.next()
    await state.update_data(age=int(message.text))

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, selective=True)
    markup.add("Мужчина", "Женщина")
    markup.add("Другое")

    await message.reply("Какой у тебя гендер?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Мужчина", "Женщина", "Другое"], state=Profile.gender)
async def gender_invalid(message: types.Message):
    return await message.reply("Выбери гендер из предложенных, пожалуйста.")


@dp.message_handler(state=Profile.gender)
async def get_gender(message: types.Message, state: FSMContext):
    await message.answer('Приятно познакомиться!')
    async with state.proxy() as data:
        data['gender'] = message.text
        await message.answer(f"Вот твоя анкета:\nИмя: {data['name']}\nВозраст: {data['age']}\nГендер: {data['gender']}")

    await db.create_profile(state, message.from_user.id)
    await state.finish()


@dp.message_handler(commands='get_profile', state="*")
async def show_profile(message):
    profile = await db.get_profile(message.from_user.id)
    name = profile[1]
    gender = profile[2]
    age = profile[3]

    text_in_message = f'Это твоя анкета\n\n' + '*Имя:   *' + f'{name}\n' + '*Гендер:   *' + f'{gender}\n' + '*Возраст:   *' + f'{age}'

    await message.answer(text_in_message, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

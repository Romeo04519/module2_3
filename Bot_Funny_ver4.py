from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

from pyexpat.errors import messages

API = ''
bot = Bot(token = API)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton( text = 'Рассчитать')
button2 = KeyboardButton( text = 'Информация')
kb.row(button)
kb.insert(button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['Start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age_text = message.text)
    #data = await state.get_data()
    await message.answer('Введите свой рост(см):')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth_text = message.text)
    #data = await state.get_data()
    await message.answer('Введите свой вес(кг):')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight_text = message.text)
    data = await state.get_data()
    cal_ = 10*float(data['weight_text']) + 6.25*float(data['growth_text']) + 5*float(data['age_text']) +5
    await message.answer(f'Ваша норма калорий: {cal_}')
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)

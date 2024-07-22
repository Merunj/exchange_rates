from aiogram import F, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
import redis
import asyncio
from config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=0)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Приветствую, данный бот создан для конвертации из одной валюты в другую с помощью команды /exchange. Также, чтобы узнать актуальные курсы валют, введите команду /rates") 
    

@router.message(Command('exchange'))
async def get_exchange_rates(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return
    try:
        original_currency, to_convert_currency, number = command.args.split(" ", maxsplit=2)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/exchange <Изначальная валюта> <Перевести в валюту> <Сумма>"
        )
        return
    og_currency = float(r.get(original_currency.upper()))
    response = og_currency * float(number)
    await message.answer(str(response))


@router.message(Command('rates'))
async def get_rates(message: Message):
    keys = r.keys()
    rates = [f"{key.decode()} = {float(r.get(key)):.2f}" for key in keys]
    await message.answer("\n".join(rates))
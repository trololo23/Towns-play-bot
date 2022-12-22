import config

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from Data_Logic import UsedTownsData
from Data_Logic import UsersData
from Data_Logic import DataBaseTowns

UsedTowns = UsedTownsData() #Operates with towns used during game
DataTowns = DataBaseTowns() #Operates with towns database
UserData = UsersData() #Operates with registered users

bot = Bot(config.token)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=["start"])
async def greeting(message): 
    await bot.send_message(message.chat.id, "Прывітанне! Гэта бот для гульні ў гарады, для атрымання даведкі напішыце /help")

@dp.message_handler(commands=["help"])
async def help(message): 
    await bot.send_message(message.chat.id, "Правілы гульні стандартныя:\n/reggame - пачаць новую гульню\n/endgame - скончыць гульню\n/nextturn - зрабіць ход, рабіць хады па-за чаргой нельга\n/usedtowns - спіс выкарыстаных гарадоў")

class RegState(StatesGroup):
	active = State()

@dp.message_handler(commands=["reggame"])
async def start_game(message): 
    await RegState.active.set()
    id = message.chat.id
    if UserData.CheckState(id) == True:
        await bot.send_message(message.chat.id, "Спачатку завяршыце старую гульню")
    else:
        UserData.AddChatGame(id)
        await bot.send_message(message.chat.id, "Увядзіце колькасць удзельнікаў")

@dp.message_handler(state=RegState.active, content_types=types.ContentType.all())
async def get_players_numb(message: types.Message, state: FSMContext):
    id = message.chat.id
    UserData.AddPlayersNumb(id, int(message.text))
    await bot.send_message(message.chat.id, "Чтобы добавиться в игру вызови метод  /addme")
    await state.finish()

@dp.message_handler(commands=["addme"])
async def add_player(message):
    id = message.chat.id
    if UserData.CheckState(id) == False:
        await bot.send_message(message.chat.id, "Сначала зарегистрируйте игру")
        return   
    if UserData.Check(id) ==  True:
        UserData.AddUser(id, message.from_user.id) 
        if UserData.Check(id) == False:
            UsedTowns.Start(id)
            UsedTowns.Add(id, 'Minsk')
            await bot.send_message(message.chat.id, "Игра началась! Для хода используйте /nextturn Первый город Minsk")
    else:
        await bot.send_message(message.chat.id, "Места закончились")

class NextTurn(StatesGroup):
	active = State()

@dp.message_handler(commands=["nextturn"])
async def make_turn(message):
    await NextTurn.active.set()
    id = message.chat.id
    if UserData.CheckState(id) == False:
        await bot.send_message(message.chat.id, "Сначала зарегистрируйте игру")
        return
    await bot.send_message(message.chat.id, "Введи город на " + UsedTowns.GetLetter(id))

@dp.message_handler(state=NextTurn.active, content_types=types.ContentType.all())
async def accept_town(message: types.Message, state: FSMContext):
    id = message.chat.id
    town_name = message.text
    if UserData.CheckTurn(id, message.from_user.id) == False:
        await bot.send_message(message.chat.id, "Не твой ход браток")
    elif UsedTowns.CheckCorrectLetter(id, town_name) == False:
        await bot.send_message(message.chat.id, "Неверная буква")
    elif UsedTowns.Find(id, town_name) == True:
        await bot.send_message(message.chat.id, "Город уже использован")
    elif DataTowns.Search(town_name) == False:
        await bot.send_message(message.chat.id, "Такого города не существует")
    else:
        UserData.NextStep(id)
        UsedTowns.Add(id, town_name)
        await bot.send_message(message.chat.id, "Харош")

    await state.finish()

@dp.message_handler(commands=["endgame"])
async def end_game(message):
    await bot.send_message(message.chat.id, "Игра завершена!")
    UsedTowns.Clear()
    UserData.Clear()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
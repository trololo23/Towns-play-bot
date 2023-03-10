import config

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from data_logic import UsedTownsData
from data_logic import UsersData
from data_logic import DataBaseTowns

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
    id = message.chat.id
    if UserData.CheckState(id) == True:
        await bot.send_message(message.chat.id, "Спачатку завяршыце старую гульню")
    else:
        await RegState.active.set()
        UserData.AddChatGame(id)
        await bot.send_message(message.chat.id, "Увядзіце колькасць удзельнікаў")

@dp.message_handler(state=RegState.active, content_types=types.ContentType.all())
async def get_players_numb(message: types.Message, state: FSMContext):
    id = message.chat.id
    UserData.AddPlayersNumb(id, int(message.text))
    await bot.send_message(message.chat.id, "Каб дадацца ў гульню выкліч метад  /addme")
    await state.finish()

@dp.message_handler(commands=["addme"])
async def add_player(message):
    id = message.chat.id
    if UserData.CheckState(id) == False:
        await bot.send_message(message.chat.id, "Спачатку зарэгіструйце гульню")
        return   
    if UserData.Check(id) ==  True:
        UserData.AddUser(id, message.from_user.id) 
        if UserData.Check(id) == False:
            UsedTowns.Start(id)
            UsedTowns.Add(id, 'Minsk')
            await bot.send_message(message.chat.id, "Гульня пачалася! Для ходу выкарыстоўвайце /nextturn\nНазвы неабходна пісаць на англійскай мове\nПершы горад Minsk")
    else:
        await bot.send_message(message.chat.id, "Месцы скончыліся")

class NextTurn(StatesGroup):
	active = State()

@dp.message_handler(commands=["nextturn"])
async def make_turn(message):
    id = message.chat.id
    if UserData.CheckState(id) == False:
        await bot.send_message(message.chat.id, "Спачатку зарэгіструйце гульню")
        return
    await NextTurn.active.set()
    await bot.send_message(message.chat.id, "Увядзі горад на " + UsedTowns.GetLetter(id).upper())

@dp.message_handler(state=NextTurn.active, content_types=types.ContentType.all())
async def accept_town(message: types.Message, state: FSMContext):
    id = message.chat.id
    town_name = message.text
    if UserData.CheckTurn(id, message.from_user.id) == False:
        await bot.send_message(message.chat.id, "Не твой ход браток")
    elif UsedTowns.CheckCorrectLetter(id, town_name) == False:
        await bot.send_message(message.chat.id, "Няправільная літара")
    elif UsedTowns.Find(id, town_name) == True:
        await bot.send_message(message.chat.id, "Горад ужо выкарыстаны")
    elif DataTowns.Search(town_name) == False:
        await bot.send_message(message.chat.id, "Такога горада не існуе")
    else:
        UserData.NextStep(id)
        UsedTowns.Add(id, town_name)
        await bot.send_message(message.chat.id, "Харош")

    await state.finish()

@dp.message_handler(commands=["endgame"])
async def end_game(message):
    id = message.chat.id
    if UserData.CheckState(id) == False:
        await bot.send_message(message.chat.id, "Спачатку зарэгіструйце гульню")
        return
    await bot.send_message(message.chat.id, "Гульня завершана!")
    UsedTowns.Clear(id)
    UserData.Clear(id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

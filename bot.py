import telebot
import config
from Data_Logic import States
from Data_Logic import UsedTownsData
from Data_Logic import UsersData
from Data_Logic import DataBaseTowns

UsedTowns = UsedTownsData() #Operates with towns used during game
DataTowns = DataBaseTowns() #Operates with towns database
UserData = UsersData() #Operates with registered users

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def greeting(message): 
    bot.send_message(message.chat.id, '''Прывітанне! Гэта бот
для гульні ў гарады, для атрымання даведкі напішыце /help''')

@bot.message_handler(commands=["help"])
def greeting(message): 
    bot.send_message(message.chat.id, '''Правілы гульні стандартныя:\n
/reggame - пачаць новую гульню \n /endgame - скончыць гульню\n
/nextturn - зрабіць ход, рабіць хады па-за чаргой нельга\n
/usedtowns - спіс выкарыстаных гарадоў''')

@bot.message_handler(commands=["reggame"])
def start_game(message): 
    id = message.chat.id
    if UserData.CheckState(id) == True:
        bot.send_message(message.chat.id, "Спачатку завяршыце старую гульню")
    else:
        UserData.AddChatGame(id)
        bot.send_message(message.chat.id, "Увядзіце колькасць удзельнікаў")
        bot.register_next_step_handler(message, get_players_numb)

def get_players_numb(message):
    id = message.chat.id
    UserData.AddPlayersNumb(id, int(message.text))
    bot.send_message(message.chat.id, "Чтобы добавиться в игру вызови метод  /addme")

@bot.message_handler(commands=["addme"])
def add_player(message):
    id = message.chat.id
    if UserData.CheckState(id) == False:
        bot.send_message(message.chat.id, "Сначала зарегистрируйте игру")
        return   
    if UserData.Check(id) ==  True:
        UserData.AddUser(id, message.from_user.id) 
        if UserData.Check(id) == False:
            UsedTowns.Start(id)
            UsedTowns.Add(id, 'Minsk')
            bot.send_message(message.chat.id, "Игра началась! Для хода используйте /nextturn Первый город Minsk")
    else:
        bot.send_message(message.chat.id, "Места закончились")

@bot.message_handler(commands=["nextturn"])
def make_turn(message):
    id = message.chat.id
    if UserData.CheckState(id) == False:
        bot.send_message(message.chat.id, "Сначала зарегистрируйте игру")
        return
    bot.send_message(message.chat.id, "Введи город на " + UsedTowns.GetLetter(id))
    bot.register_next_step_handler(message, accept_town)

def accept_town(message):
    id = message.chat.id
    town_name = message.text
    if UserData.CheckTurn(id, message.from_user.id) == False:
        bot.send_message(message.chat.id, "Не твой ход браток")
    elif UsedTowns.CheckCorrectLetter(id, town_name) == False:
        bot.send_message(message.chat.id, "Неверная буква")
    elif UsedTowns.Find(id, town_name) == True:
        bot.send_message(message.chat.id, "Город уже использован")
    elif DataTowns.Search(town_name) == False:
        bot.send_message(message.chat.id, "Такого города не существует")
    else:
        UserData.NextStep(id)
        UsedTowns.Add(id, town_name)




@bot.message_handler(commands=["endgame"])
def start_game(message): 
    bot.send_message(message.chat.id, greeting)



@bot.message_handler(commands=["usedtowns"])
def start_game(message): 
    bot.send_message(message.chat.id, greeting)




bot.polling(none_stop=True, interval=0)



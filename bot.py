import telebot
import config
from Data_Logic import States
from Data_Logic import UsedTownsData
from Data_Logic import UsersData
from Data_Logic import DataBaseTowns

GameState = States.game_off



UsedTownsData #Operates with towns used during game
DataBaseTowns #Operates with towns database
UsersData #Operates with registered users

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def greeting(message): # Название функции не играет никакой роли
    bot.send_message(message.chat.id, '''Прывітанне! Гэта бот для гульні
     ў гарады, для атрымання даведкі напішыце /help''')

@bot.message_handler(commands=["help"])
def greeting(message): # Название функции не играет никакой роли
    bot.send_message(message.chat.id, '''Правілы гульні стандартныя: \n
    /reggame - пачаць новую гульню \n /endgame - скончыць гульню \n
    /nextturn - зрабіць ход, рабіць хады па-за чаргой нельга \n
    /usedtowns - спіс выкарыстаных гарадоў''')

@bot.message_handler(commands=["reggame"])
def start_game(message): 
    if GameState.name == States.game_on:
        bot.send_message(message.chat.id, "Спачатку завяршыце старую гульню")
    else:
        GameState = States.game_on
        bot.send_message(message.chat.id, "Увядзіце колькасць удзельнікаў")
        bot.register_next_step_handler(message, get_players_numb)

def get_players_numb(message):
    players_numb = int(message.text)
    for i in range(0, players_numb):
        bot.register_next_step_handler(message, get_players_numb)

def 


#bot.send_message(message.chat.id, "Гульня пачалася! Назвы гарадоў неабходна пісаць на англійскай")





@bot.message_handler(commands=["endgame"])
def start_game(message): 
    bot.send_message(message.chat.id, greeting)

@bot.message_handler(commands=["nextturn"])
def start_game(message): 
    bot.send_message(message.chat.id, greeting)

@bot.message_handler(commands=["usedtowns"])
def start_game(message): 
    bot.send_message(message.chat.id, greeting)




bot.polling(none_stop=True, interval=0)



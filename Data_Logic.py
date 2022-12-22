import pickle 
import csv
from enum import Enum, auto

#Operates with registered users
class UsersData:
    
    def __init__(self):
      with open('data/players_id_data.txt', 'rb') as f:
        try:
          self.chat_players_map = pickle.load(f)
        except EOFError:
          self.chat_players_map = dict()
      with open('data/players_turn_data.txt', 'rb') as f:
        try:
          self.players_turn = pickle.load(f)
        except EOFError:
          self.players_turn = dict()
        
    def write(self):
      with open('data/players_id_data.txt', 'wb') as f:
        pickle.dump(self.chat_players_map, f) 
      with open('data/players_turn_data.txt', 'wb') as f:
        pickle.dump(self.players_turn, f)

    def AddChatGame(self, chat_id):
      self.chat_players_map[chat_id] = list()
      self.players_turn[chat_id] = list()

    def AddUser(self, chat_id, user_id):
      self.chat_players_map[chat_id].append(user_id)

    def Check(self, chat_id):
      if len(self.chat_players_map[chat_id]) == self.players_turn[chat_id][0]:
        return False
      else:
        return True

    def AddPlayersNumb(self, chat_id, players_numb):
      self.players_turn[chat_id] = list()
      self.players_turn[chat_id].append(players_numb)
      self.players_turn[chat_id].append(0)

    def CheckTurn(self, chat_id, user_id):
      cur_player = self.players_turn[chat_id][1] 
      players_numb = self.players_turn[chat_id][0] 
      if self.chat_players_map[chat_id][cur_player] != user_id:
        return False
      return True

    def NextStep(self, chat_id):
      cur_player = self.players_turn[chat_id][1] 
      players_numb = self.players_turn[chat_id][0]
      self.players_turn[chat_id][1] = (cur_player + 1) % players_numb

    def CLear(self, chat_id):
      self.chat_players_map[chat_id] = list()
      self.players_turn[chat_id] = list()

    def CheckState(self, chat_id):
      if chat_id in self.players_turn.keys():
        if len(self.players_turn[chat_id]) > 0:
          return True
      return False


#Operates with towns used during game
class UsedTownsData:

    def __init__(self):
      with open('data/chat_used_towns.txt', 'rb') as f:
        try:
          self.used_towns = pickle.load(f)
        except EOFError:
          self.used_towns = dict()

    def Find(self, chat_id, town_name):
      if town_name in self.used_towns[chat_id]:
        return True
      else:
        return False

    def Start(self, chat_id):
      self.used_towns[chat_id] = list()

    def Add(self, chat_id, town_name):
      self.used_towns[chat_id].append(town_name)

    def CheckCorrectLetter(self, chat_id, user_ans):
      last_used_town = self.used_towns[chat_id][-1]
      if last_used_town[-1].lower() != user_ans[0].lower():
        return False
      return True

    def GetLetter(self, chat_id):
      last_used_town = self.used_towns[chat_id][-1]
      return last_used_town[-1]

    def Clear(self, chat_id):
      self.used_towns = dict() 

#Operates with towns database
class DataBaseTowns:

    def Search(self, town_name):
      with open('./data/world-cities.csv', 'r') as f:
        csvreader = csv.reader(f, delimiter=',')
        for row in csvreader:
          if row[0] == town_name:
            return True
        return False
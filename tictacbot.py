#!/usr/bin/env python3

import json
import time
import urllib
import random
import logging
from exceptions import *
from telegram.ext import Updater,CommandHandler
from game import Game

try:
	with open('api_token','r') as f:
		api_token = f.readline().rstrip()
except IOError:
	print("Unable to locate api token")
	sys.exit()

URL = "https://api.telegram.org/bot{}/".format(api_token)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)


updater = Updater(token=api_token)
dispatcher = updater.dispatcher
last_update_id = None
games = {}

def get_user(update):
	try:
		user = update.message.from_user
	except (NameError, AttributeError):
		try:
			user = update.inline_query.from_user
		except (NameError, AttributeError):
			try:
				user = update.inline_result.from_user
			except (NameError, AttributeError):
				try:
					user = update.callback_query.from_user
				except (NameError, AttributeError):
					return None
	return user

def get_user_id(update):
	user = get_user(update)
	if user == None:
		return None
	elif user.id == None:
		return None
	else:
		return user.id

def narrate(bot, update, text):
	bot.sendMessage(chat_id=update.message.chat_id, text=text)

def start_game(bot, update):
	if update.message.chat_id not in games:
		update.message.reply_text("There is no game on this chat. Start a new game with /new")
		return
	game = games[update.message.chat_id]	
	try:
		game.start()
		narrate(bot,update,"-----GAME STARTED-----")
		narrate(bot,update,game.getBoardString())
		narrate(bot,update,"It is now '{} ({})'s turn to move",game.current_player.name,game.current_player.token)
	except GameStartedError:
		update.message.reply_text("The game has already started")
	except TooFewPlayersError:	
		update.message.reply_text("2 players are required to start the game")

		
def move(bot, update, args):
	if update.message.chat_id not in games:
		update.message.reply_text("There is no game on this chat. Start a new game with /new")
		return
	game = games[update.message.chat_id]	
	try: 
		game.move(int(args[0]),players[user_id])
		narrate(bot,update,game.getBoardString())
		if game.checkWin(players[user_id]):
			narrate(bot,update,"CONGRATULATIONS! {} has won!".format(players[user_id]))
			return
		if game.current_player == 'X':
			game.current_player = 'O'
			narrate(bot,update,"It is now 'O's turn to move")
		elif game.current_player == 'O':
			game.current_player = 'X'
			narrate(bot,update,"It is now 'X's turn to move")
		else:
			update.message.reply_text("Error with player token!")
	except NotInGameError:
		update.message.reply_text("You are not in the game")
	except InvalidMoveError:
		update.message.reply_text("Invalid Move!")
	except GameNotStartedError:
		update.message.reply_text("Game has not started")

def get_players(bot,update):
	if update.message.chat_id not in games:
		update.message.reply_text("There is no game on this chat. Start a new game with /new")
		return
	game = games[update.message.chat_id]	
	playerString = "---Players---\n"
	playerString += game.getPlayers()
	update.message.reply_text(playerString)
	
def join_game(bot, update):
	if update.message.chat_id not in games:
		update.message.reply_text("There is no game on this chat. Start a new game with /new")
		return
	game = games[update.message.chat_id]	
	user = get_user(update)
	if not user:
		return
	try:
		token = game.add_player(user.id,user.first_name)
		update.message.reply_text("Welcome {}\nYou are playing as {}".format(user.first_name,token))
		if len(game.players) == 2:
			narrate(bot,update,"You have 2 players! You may start the game with /start")
	except PlayerLimitError:
		update.message.reply_text("Maximum Player Limit Reached")
	except AlreadyJoinedError:
		update.message.reply_text("You are already in the game")
		
def new_game(bot, update, args):
	if update.message.chat_id in games:
		update.message.reply_text("There is already a game running on this chat. To end the game, use /delete")
		return
	board_size = 3
	if len(args):
		try:
			board_size = int(args[0])
		except ValueError:
			board_size = 3
	games[update.message.chat_id] = Game(board_size)
	narrate(bot,update,"Game created! Join the game with /join and check players with /players")
			
def delete(bot, update):
	if update.message.chat_id not in games:
		update.message.reply_text("There is no game on this chat. Start a new game with /new")
		return
	del games[update.message.chat_id]
	narrate(bot,update,"Game deleted. Start a new game with /new")

def unjoin(bot, update):
	if update.message.chat_id not in games:
		update.message.reply_text("There is no game on this chat. Start a new game with /new")
		return
	game = games[update.message.chat_id]	
	user_id = get_user_id(update)
	try:
		game.remove_player(user_id)
		update.message.reply_text("You have left the game")
	except NotInGameError:
		update.message.reply_text("You are not in the game")
	except GameStartedError:
		update.message.reply_text("Game has already started")

def main():
	dispatcher.add_handler(CommandHandler('join',join_game))
	dispatcher.add_handler(CommandHandler('start',start_game))
	dispatcher.add_handler(CommandHandler('players',get_players))
	dispatcher.add_handler(CommandHandler('move',move,pass_args=True))
	dispatcher.add_handler(CommandHandler('new',new_game,pass_args=True))
	dispatcher.add_handler(CommandHandler('delete',delete))
	dispatcher.add_handler(CommandHandler('unjoin',unjoin))
	updater.start_polling()
	updater.idle()
	return

	#while True:
		#sendMessage: game.printBoardString()
		#get updates from player_id of 'X'
			#get number between 1-9
	
	#Let users join with /join
	#Setup tictac map
	#Randomly choose user1
	#Listen for O from user1
	#Listen for X from user2
	#Repeat until someone wins
	while True:
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			#echo_all(updates)
			game_update(game,updates)
		time.sleep(0.5)

if __name__ == '__main__':
	main()
	

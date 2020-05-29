import socketio
import random
import numpy as np
from IA_Engine import *

#Socket
socket = socketio.Client()

class Totito():
	def __init__(self):
		self.user_name = ''
		self.tournament_id = ''
		self.game_id = ''
		self.player_turn_id = ''
		self.board = []

#conection
@socket.on('connect')
def on_connect():
	socket.emit('signin',
		{
			'user_name': totito.user_name,
        	'tournament_id': totito.tournament_id,
        	'user_role': 'player'
		}
	)
	print('Connection succesfull')

#desconection
@socket.on('disconnect')
def on_disconnect():
    print('Disconnected, Bye!')
    socket.disconnect()

#login signal
@socket.on('ok_signin')
def on_ok_signin():
    print('Successfully signed in!') 


#ready to play
@socket.on('ready')
def on_ready(data):
	print('Playing! ')
	#createBoard()
	#print(totito.board) ---> Obtiene el board del juego

	totito.player_turn_id = data['player_turn_id']
	totito.game_id = data['game_id']
	totito.board = data['board']

	'''
	horizontal = random.randint(0, 1)
	vertical = random.randint(0,29)

	while int(totito.board[horizontal][vertical]) != 99:
		horizontal = random.randint(0,1)
		vertical = random.randint(0,29)
	
	movement =[random.randint(0,1), random.randint(0,29)]

	while validateMovement(movement) != True:
		movement = random.choice(movement)
		movement.remove(movement)
	'''

	socket.emit('play', 
		{	
			'tournament_id': totito.tournament_id,
			'player_turn_id': totito.player_turn_id,
			'game_id': totito.game_id,
			'movement': minMax(totito.board, 4, True, totito.player_turn_id)
        }
    )

@socket.on('finish')
def finish(data): 

	print('Game', data['game_id'], 'has finished')

	#totito.board = data['board']
	pointPlayer(totito.board)
	square(totito.board)

	#Message that you won
	if data['player_turn_id'] == data['winner_turn_id']:
		print('Congratulation! You Won: ', totito.user_name, 'ID', data['player_turn_id'])
	else:
		print('Sorry, you lost, player: ', totito.user_name, 'ID', data['player_turn_id'])

	socket.emit('player_ready', 
		{
        	"tournament_id": totito.tournament_id,
        	"game_id": totito.game_id,
        	"player_turn_id":totito.player_turn_id
        }
    )

#Validate movement
def validateMovement(movement):

	#Evitar null
	if movement == []:
		return False
	
	num = None

	for conv in (int, float, complex):
		try: 
			num = conv(movement[0])
			break
		except ValueError:
			pass
	
	if num is None:
		return False
	
	for conv in (int, float, complex):
		try: 
			num = conv(movement[1])
			break
		except ValueError:
			pass

	if num is None:
		return False

	movement = [int(movement[0]), int(movement[1])]

	if movement[0] < 0 or movement[0] >1:
		return False

	if movement[1] < 0 or movement[1] >29:
		return False

	return True

# connect to server
#socket.connect('http://localhost:4000')

#Control Data
totito = Totito()
totito.user_name = input("Ingrese Usuario/Nombre: ")
totito.tournament_id = input("Ingrese Tournament ID: ")

#socket.connect('http://3.12.129.126:5000')
socket.connect('http://localhost:4000')

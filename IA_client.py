import socketio
import random
from IA_Engine import *
from Totito import Totito

#Socket
socket = socketio.Client()

class user_data():
	pass

#conection
@socket.on('connect')
def on_connect():
	socket.emit('signin',
		{
			'user_name': user.user_name,
        	'tournament_id': user.tournament_id,
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

	minimax = MiniMax()
	totito = Totito()

	minimax.start(totito)
	move = minimax.get_move(data)

	direction_index = 0 if move[0] == Orientation.HORIZONTAL else 1
	pos = move[1]

	socket.emit('play', 
		{	
			'tournament_id': user.tournament_id,
			'player_turn_id': data['player_turn_id'],
			'game_id': data['game_id'],
			'movement': [direction_index, pos]
        }
    )

@socket.on('finish')
def finish(data): 

	print('Game', data['game_id'], 'has finished')

	#Message that you won
	if data['player_turn_id'] == data['winner_turn_id']:
		print('Congratulation! You Won: ', user.user_name, 'ID', data['player_turn_id'])
	else:
		print('Sorry, you lost, player: ', user.user_name, 'ID', data['player_turn_id'])

	socket.emit('player_ready', 
		{
        	"tournament_id": user.tournament_id,
        	"game_id": data['game_id'],
        	"player_turn_id": data['player_turn_id']
        }
    )

# connect to server
#socket.connect('http://localhost:4000')

#Control Data
user = user_data()
user.user_name = input("Ingrese Usuario/Nombre: ")
user.tournament_id = input("Ingrese Tournament ID: ")

#socket.connect('http://3.12.129.126:5000')
socket.connect('http://localhost:4000')

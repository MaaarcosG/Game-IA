import socketio

#Socket
socket = socketio.Client()

#conection
@socket.on('connect')
def on_connect():
	socket.emit('signin',
		{
			'user_name': 'maaarcosg_',
        	'tournament_id': 142857,
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
	socket.emit('play', 
		{	
			'tournament_id': 142857,
			'player_turn_id': data['player_turn_id'],
			'game_id': data['game_id'],
			#movement: ?
        }
    )

@socket.on('finish')
def finish(data): 
	print("The Game has Finished!")
	socket.emit('player_ready', 
		{
        	"tournament_id":tournament_id,
        	"game_id":data['game_id'],
        	"player_turn_id":data['player_turn_id']
        }
    )


# connect to server
socket.connect('http://localhost:4000')
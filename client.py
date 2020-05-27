import socketio
import random

#Socket
socket = socketio.Client()

#Tournament ID
tournament_id = 3

#list 
tirosPosibles = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,15],[0,16],[0,17],[0,18],[0,19],[0,20],[0,21],[0,22],[0,23],[0,24],[0,25],[0,26],[0,27],[0,28],[0,29],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,21],[1,22],[1,23],[1,24],[1,25],[1,26],[1,27],[1,28],[1,29]]

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

#conection
@socket.on('connect')
def on_connect():
	socket.emit('signin',
		{
			'user_name': 'Marcos Gutierrez',
        	'tournament_id': tournament_id,
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
	print('Ready to Play! ')

	#movement =[random.randint(0,1),random.randint(0,29)]
	movement = random.choice(tirosPosibles)

	while validateMovement(movement) != True:
		movement = random.choice(tirosPosibles)
		tirosPosibles.remove(movement)

	socket.emit('play', 
		{	
			'tournament_id': tournament_id,
			'player_turn_id': data['player_turn_id'],
			'game_id': data['game_id'],
			'movement': movement
        }
    )

@socket.on('finish')
def finish(data): 

	global tirosPosibles
	tirosPosibles = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,15],[0,16],[0,17],[0,18],[0,19],[0,20],[0,21],[0,22],[0,23],[0,24],[0,25],[0,26],[0,27],[0,28],[0,29],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,21],[1,22],[1,23],[1,24],[1,25],[1,26],[1,27],[1,28],[1,29]]

	print('Game', data['game_id'], 'has finished')

	socket.emit('player_ready', 
		{
        	"tournament_id":tournament_id,
        	"game_id":data['game_id'],
        	"player_turn_id":data['player_turn_id']
        }
    )


# connect to server
#socket.connect('http://localhost:4000')
socket.connect('http://3.12.129.126:5000')

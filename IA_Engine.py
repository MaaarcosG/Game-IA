import sys

def minMax(board, depth, Max, player_turn_id):
	a = -sys.maxsize - 1
	b = sys.maxsize

	#verificamos el turno
	oponent_turn_id = 1
	if(player_turn_id == 1):
		oponent_turn_id = 2

	if (depth == 0):
		return evaluateBoard(board)

	moves, boardLocation = generate_validate_move(board, player_turn_id)
	best = 0
	if Max:
		for board in boardLocation:
			v = minMax(board, depth-1, not Max, player_turn_id)
			if(v>a):
				a = v
				best = board
			if(a>=b):
				break
		if(best==0):
			return 0
		else:
			return moves[boardLocation.index(best)]
	else:
		for board in boardLocation:
			v = minMax(board, depth-1, not Max, player_turn_id)
			if(v<b):
				b = v
				best = board
			if(a>=b):
				break
		if(best==0):
			return 0
		else:
			return moves[boardLocation.index(best)]

def generate_validate_move(board, player_turn_id):
	bestValue = -90000000000
	location = -1
	position = -1
	EMPTY = 99

	#Verificamos el mejor movimiento
	for i in range(len(board)):
		for j in range(len(board[1])):
			if(board[i][j] == EMPTY):
				board[i][j] = 0
				move_value = minMax(board, 0, False, player_turn_id)
				board[i][j] = 99
				if(move_value>bestValue):
					location = i
					position = j
					bestValue = move_value

	bestMove = []
	bestMove.append(i)
	bestMove.append(j)
	return bestMove

def evaluateBoard(board):
	complete = board[0] + board[1]
	for i in range(len(complete)):
		if(complete[i] == 99 ):
			return True
	return False



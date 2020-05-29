from Totito import Player
from Totito import Orientation
from Totito import Totito

class MiniMax:

	def __init__(self):
		self.initial_alpha = -1000000
		self.initial_beta = 1000000
		self.maximizing_player = Player.PLAYER_ONE
		self.max_depth = 3
	
	def start(self, totito: Totito):
		self.game = totito
	
	def get_move(self, game_state):
		self.maximizing_player = Player.PLAYER_ONE if game_state['player_turn_id'] == 1 else Player.PLAYER_TWO
		self.game.set_board(game_state['board'])
		posible_moves = self._posible_moves_index(self.game.empty_lines())
		next_move = self._get_minimax_move(posible_moves)
		return next_move
	
	def _get_minimax_move(self, posible_moves):
		best_score = -1000000
		best_move = posible_moves[0]

		for move in posible_moves:
			self.game.draw_line(move[1], move[0], self.maximizing_player)
			score = self.minimax(self.game, False, 0, self.initial_alpha, self.initial_beta)
			self.game.empty_line(move[1], move[0])

			if score > best_score:
				best_score = score
				best_move = move
		
		return best_move


	def minimax(self, game: Totito, is_maximizing, depth, alpha, beta):
		if game.is_game_over() or depth == self.max_depth:
			score = game.get_current_score()
			return score[0] - score[1]
		elif is_maximizing:
			return self._max(game, depth, alpha, beta)
		else:
			return self._min(game, depth, alpha, beta)

	def _min(self, game: Totito, depth, alpha, beta):
		for move in self._posible_moves_index(game.empty_lines()):
			game.draw_line(move[1], move[0], self._get_opponent(self.maximizing_player))
			score = self.minimax(game, True, depth + 1, alpha, beta)
			self.game.empty_line(move[1], move[0])
			beta = min(beta, score)
			if(alpha >= beta):
				break
		return beta

	def _max(self, game: Totito, depth, alpha, beta):
		for move in self._posible_moves_index(game.empty_lines()):
			game.draw_line(move[1], move[0], self.maximizing_player)
			score = self.minimax(game, False, depth + 1, alpha, beta)
			self.game.empty_line(move[1], move[0])
			alpha = max(alpha, score)
			if(alpha >= beta):
				break
		return alpha

	def _posible_moves_index(self, move_dict):
		empty_vals = []
		for vertical in move_dict['v']:
			empty_vals.append((Orientation.VERTICAL, vertical))
		
		for horizontal in move_dict['h']:
			empty_vals.append((Orientation.HORIZONTAL, horizontal))
		
		return empty_vals
	
	def _get_opponent(self, player: Player):
		return Player.PLAYER_ONE if player == Player.PLAYER_TWO else Player.PLAYER_TWO
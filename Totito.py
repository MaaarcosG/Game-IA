from enum import Enum

EMPTY = 99
N = 6
FILLEDP11 = 1
FILLEDP12 = 2
FILLEDP21 = -1
FILLEDP22 = -2

class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class Player(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2



class Totito():
    
    def set_board(self, board):
        self.board = board
    
    def draw_line(self, position: int, orientation: Orientation, player: Player):
        before_score = self.get_closed_boxes()
        line_index = self._draw_line(position, orientation, 0)
        after_score = self.get_closed_boxes()

        if before_score < after_score:
            self.draw_line(position, orientation, self._get_player_constants(player, after_score - before_score))
        
        return line_index
    
    def empty_line(self, position: int, orientation: Orientation):
        return self._draw_line(position, orientation, EMPTY)

    def _draw_line(self, position: int, orientation: Orientation, line_value: int):
        board_index = 0 if orientation == Orientation.HORIZONTAL else 1

        if position < len(self.board[board_index]):
            self.board[board_index][position] = line_value
        
        return (board_index, position)
    
    def _get_player_constants(self, player: Player, value: int):
        if player == Player.PLAYER_ONE:
            if value == 1:
                return FILLEDP11
            elif value == 2:
                return FILLEDP12
        else:
            if value == 1:
                return FILLEDP21
            elif value == 2:
                return FILLEDP22
    
    def empty_lines(self):
        empty_v = []
        empty_h = []

        for i in range( len( self.board[0] ) ):
            if self.board[0][i] == EMPTY:
                empty_h.append(i)
            
            if self.board[1][i] == EMPTY:
                empty_v.append(i)
        
        return {
            'v': empty_v,
            'h': empty_h
        }
    
    def is_game_over(self):
        remaining = self.empty_lines()
        return len(remaining['v']) == 0 and len(remaining['h']) == 0

    
    def get_closed_boxes(self):
        acumulador = 0
        contador = 0
        contadorPuntos = 0
        board = self.board
        for i in range(len(board[0])):
            if ((i + 1) % N) != 0:
                if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                    contadorPuntos = contadorPuntos + 1
                acumulador = acumulador + N
            else:
                contador = contador + 1
                acumulador = 0
        return contadorPuntos
    
    def get_current_score(self):
        player1 = 0
        player2 = 0
        board = self.board

        for i in range(len(board[0])):
            if board[0][i] == FILLEDP12:
                player1 = player1 + 2
            elif board[0][i] == FILLEDP11:
                player1 = player1 + 1
            elif board[0][i] == FILLEDP22:
                player2 = player2 + 2
            elif board[0][i] == FILLEDP21:
                player2 = player2 + 1

        for j in range(len(board[1])):
            if board[1][j] == FILLEDP12:
                player1 = player1 + 2
            elif board[1][j] == FILLEDP11:
                player1 = player1 + 1
            elif board[1][j] == FILLEDP22:
                player2 = player2 + 2
            elif board[1][j] == FILLEDP21:
                player2 = player2 + 1
        
        return (player1, player2)

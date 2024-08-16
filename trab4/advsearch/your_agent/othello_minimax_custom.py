import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.

    return minimax_move(state, 4, evaluate_custom)

''' 
    ## Source
    Paper: An Analysis of Heuristics in Othello
    Authors: Vaishnavi Sannidhanam and Muthukaruppan Annamalai
    Summary: The results suggest that stability is a very powerful heuristic when used in conjunction
    with the corner, coin parity and mobility heuristics.Currently, the implementation of a typical
    stability heuristic provides an approximation to the actual stability value. This is due to the 
    complexity involved. But allocating more processor power for this task would definitely prove to
    be profitable. 
'''
def evaluate_custom(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on your custom heuristic
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    # Initialization 
    player_score = 0
    opponent_score = 0

    # Corner evaluation
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    corner_weight = 30
    for i, j in corners:
        if state.get_board().tiles[i][j] == player:
            player_score += corner_weight
        elif state.get_board().tiles[i][j] == Board.opponent(player):
            opponent_score += corner_weight

    # Edge and stability evaluation
    stability_score = 0
    edge_weight = 10
    stability_weight = 30
    for i in range(8):
        for j in range(8):
            if state.get_board().tiles[i][j] == player:
                if is_stable(state, i, j, player):
                    stability_score += stability_weight
                elif (i == 0 or i == 7 or j == 0 or j == 7):
                    player_score += edge_weight
            elif state.get_board().tiles[i][j] == Board.opponent(player):
                if is_stable(state, i, j, Board.opponent(player)):
                    stability_score -= stability_weight
                elif (i == 0 or i == 7 or j == 0 or j == 7):
                    opponent_score += edge_weight

    # Mobility evaluation
    mobility_weight = 15
    player_mobility = len(state.get_board().legal_moves(player))
    opponent_mobility = len(state.get_board().legal_moves(Board.opponent(player)))
    mobility_score = mobility_weight * (player_mobility - opponent_mobility)

    # Parity evaluation
    parity_weight = 15
    parity_score = parity_weight * (state.get_board().num_pieces(player) - state.get_board().num_pieces(Board.opponent(player)))/(state.get_board().num_pieces(player) + state.get_board().num_pieces(Board.opponent(player)))

    # Sum of all factors
    total_score = player_score - opponent_score + stability_score + mobility_score + parity_score

    return total_score

def is_stable(state, x, y, player):
    """
    Determines if a piece at position (x, y) is stable.

    The stability measure of a coin is a quantitative representation 
    of how vulnerable it is to being flanked. Stable coins are coins which
    cannot be flanked at any point of time in the
    game from the given state. 
    """

    '''
    Corners are always stable in nature, and as you build upon
    corners, more coins become stable in the region. 
    '''
    if (x == 0 or x == 7) and (y == 0 or y == 7):
        return True  
    
    # Checking stability at the edges
    stable = True
    # Directions: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] 
    for dx, dy in directions:
        tx, ty = x + dx, y + dy
        if 0 <= tx < 8 and 0 <= ty < 8:
            if state.get_board().tiles[tx][ty] != player:
                stable = False
                break
    return stable


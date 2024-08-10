from typing import Tuple, Callable



def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    if max_depth == -1:
        max_depth = float('inf')

    _, a = maxGain(state, float('-inf'), float('inf'), state.player, max_depth, eval_func)
    return a

def maxGain(state, alfa, beta, player, max_depth:int, eval_func:Callable):
    if state.is_terminal() or max_depth == 0:
        return eval_func(state, player), None
    v = float('-inf')
    a = None
    for action in state.legal_moves():
        new_state = state.next_state(action)
        val, _ = minGain(new_state, alfa, beta, player, max_depth-1, eval_func)
        if val > v:
            v = val
            a = action
        alfa = max(alfa, v)
        if beta <= alfa:
            break
    return v, a

def minGain(state, alfa, beta, player, max_depth:int, eval_func:Callable):
    if state.is_terminal() or max_depth == 0:
        return eval_func(state, player), None
    v = float('inf')
    a = None
    for action in state.legal_moves():
        new_state = state.next_state(action)
        val, _ = maxGain(new_state, alfa, beta, player, max_depth-1, eval_func)
        if val < v:
            v = val
            a = action
        beta = min(beta, v)
        if beta <= alfa:
            break
    return v, a

"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Improved the improved_score by adding the weighted coefficients to the number of legal move for player 1
    and player 2 – score = w1*player1_moves – w2*player2_moves. Where w1 = 3 and w2 = 4,
    so it makes perfect sense that if the score is positive, the player 1 is in much better situation comparing to player 2.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w1 = 3 # weight for the number of moves for active player
    w2 = 4 # weight for the number of moves for the opponent player

    return float(w1 * len(game.get_legal_moves(player)) - w2 * len(game.get_legal_moves(game.get_opponent(player))))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Attempt to make a partitioning of the board where the result is the difference of the number of empty spaces
    available for player’s 1 part of the board to the number of empty spaces available for player’s 2 part of the board.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # check partition
    player_position = game.get_player_location(player)
    opponent_position = game.get_player_location(game.get_opponent(player))

    pr, pc = player_position
    opr, opc = opponent_position

    blank_spaces = game.get_blank_spaces()

    num_player_spaces = len(blank_spaces)
    num_opponent_spaces = 0

    if pc < opc:
        # player is on the left
        player_spaces = [(r, c) for r, c in blank_spaces if c < pc]
        opponent_spaces = [(r, c) for r, c in blank_spaces if c > opc]

        num_player_spaces = len(player_spaces)
        num_opponent_spaces = len(opponent_spaces)

    elif pc > opc:
        # player is on the right
        player_spaces = [(r, c) for r, c in blank_spaces if c > pc]
        opponent_spaces = [(r, c) for r, c in blank_spaces if c < opc]

        num_player_spaces = len(player_spaces)
        num_opponent_spaces = len(opponent_spaces)

    else:
        if pr < opr:
            # player is on the top
            player_spaces = [(r, c) for r, c in blank_spaces if r < pr]
            opponent_spaces = [(r, c) for r, c in blank_spaces if r > opr]

            num_player_spaces = len(player_spaces)
            num_opponent_spaces = len(opponent_spaces)
        else:
            # player is on the bottom
            player_spaces = [(r, c) for r, c in blank_spaces if r > pr]
            opponent_spaces = [(r, c) for r, c in blank_spaces if r < opr]

            num_player_spaces = len(player_spaces)
            num_opponent_spaces = len(opponent_spaces)

    return float(num_player_spaces - num_opponent_spaces)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Getting the difference between the squared centered distance for player 2 and squared centered distance for player 1.
    In this case we assume that if player 1 is closer to the center, than player 2, it has higher chances to win.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    playerdist = float((h - y) ** 2 + (w - x) ** 2)

    y, x = game.get_player_location(game.get_opponent(player))
    opponentdist = float((h - y) ** 2 + (w - x) ** 2)

    return float(opponentdist - playerdist)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minvalue(self, game, depth):
        """
        Gets the min value which is possible to achieve from the current state.
        :param game: An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        :param depth: Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        :return: the min value which is possible to achieve from the current state.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, game._inactive_player)

        legal_moves = game.get_legal_moves(game._active_player)

        if len(legal_moves) == 0:
            return self.score(game, game._inactive_player)

        val = float("inf")

        for move in legal_moves:
            val = min(val, self.maxvalue(game.forecast_move(move), depth-1))

        return val

    def maxvalue(self, game, depth):
        """
        Gets the max value which is possible to achieve from the current state.
        :param game: An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        :param depth: Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        :return: the max value which is possible to achieve from the current state.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, game._active_player)

        legal_moves = game.get_legal_moves(game._active_player)

        if len(legal_moves) == 0:
            return self.score(game, game._active_player)

        val = float("-inf")

        for move in legal_moves:
            val = max(val, self.minvalue(game.forecast_move(move), depth-1))

        return val

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        legal_moves = game.get_legal_moves(game.active_player)

        best_move = (-1, -1)

        if len(legal_moves) > 0:

            max_value = self.minvalue(game.forecast_move(legal_moves[0]), depth-1)
            best_move = legal_moves[0]

            for move in legal_moves[1:]:
                new_max_value = max(max_value, self.minvalue(game.forecast_move(move), depth-1))

                if new_max_value > max_value:
                    max_value = new_max_value
                    best_move = move

        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            # Setting initial depth to 2. Increase it until getting the SearchTimeout.
            depth = 2
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minvalue(self, game, depth, alpha, beta, player):
        """
        Gets the min value possible to achieve from the current board state.
        :param game: An instance of the Isolation game `Board` class representing the
            current game state
        :param depth: Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        :param alpha: Alpha limits the lower bound of search on minimizing layers
        :param beta: Beta limits the upper bound of search on maximizing layers
        :param player: An instance of the 'Player' class representing the player we are calculating the score for
        :return: (float, (int, int)):
                    the min value possible to achieve from the current board state and the move leading to that value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)

        if depth == 0:
            return self.score(game, player), best_move

        legal_moves = game.get_legal_moves(game.active_player)

        if len(legal_moves) == 0:
            return self.score(game, player), best_move

        val = float("inf")

        for move in legal_moves:
            result = self.maxvalue(game.forecast_move(move), depth-1, alpha, beta, player)
            val = min(val, result[0])

            if val <= alpha:
                return val, result[1]

            if val < beta:
                beta = val
                best_move = move

        return val, best_move

    def maxvalue(self, game, depth, alpha, beta, player):
        """
        Gets the max value possible to achieve from the current board state.
        :param game: An instance of the Isolation game `Board` class representing the
            current game state
        :param depth: Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        :param alpha: Alpha limits the lower bound of search on minimizing layers
        :param beta: Beta limits the upper bound of search on maximizing layers
        :param player: An instance of the 'Player' class representing the player we are calculating the score for
        :return: (float, (int, int)):
                    the max value possible to achieve from the current board state and the move leading to that value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)

        if depth == 0:
            return self.score(game, player), best_move

        legal_moves = game.get_legal_moves(game.active_player)

        if len(legal_moves) == 0:
            return self.score(game, player), best_move

        val = float("-inf")

        for move in legal_moves:
            result = self.minvalue(game.forecast_move(move), depth-1, alpha, beta, player)
            val = max(val, result[0])
            if val >= beta:
                return val, move

            if val > alpha:
                alpha = val
                best_move = move

        return val, best_move


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        # TODO: finish this function!
        score, best_move = self.maxvalue(game, depth, alpha, beta, game.active_player)

        return best_move




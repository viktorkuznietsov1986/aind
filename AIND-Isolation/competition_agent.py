"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
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
        # OPTIONAL: Finish this function!
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        self.time_left = time_left

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

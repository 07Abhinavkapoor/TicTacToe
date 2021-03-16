from abc import ABC, abstractmethod
import random
import math


class Player(ABC):
    """
    Abstract base class for different types of players.

    Methods:
    get_move - To get the next move of the player.
    """

    def __init__(self, letter):
        self.letter = letter

    @abstractmethod
    def get_move(self, game):
        pass


class HumanPlayer(Player):
    """
    Class for creating a human player.
    """

    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_move = False
        next_move = None

        while not valid_move:
            square = input(self.letter + "\'s turn. Input move (0-8)\n> ")

            try:
                next_move = int(square)
                if next_move not in game.available_moves():
                    raise ValueError

                valid_move = True
            except ValueError:
                print("Invalid value. Try Again")

        return next_move


class ComputerPlayer(Player):
    """
    Class for creating a computer player. Easy level if smart is set to False, and Hard level if smart is set to True.
    """

    def __init__(self, letter, smart=False):
        super().__init__(letter)
        self.smart = smart

    def get_move(self, game):
        options = game.available_moves()
        if not self.smart or len(options) == 9:
            return random.choice(options)
        else:
            square = self.minimax(game, self.letter)["position"]
            return square

    def minimax(self, state, player):
        """
        Method to find the square which maximizes the chances of winning

        Parameters:
        state(TicTacToe)- The current state of the game
        player(Player)- The player whose turn is to make the move

        Returns: A dictionary with 2 keys-
        "position": The position on which the move was made
        "score": Score got after making that move
        (If the max_player wins the game, then score is calculated as 1 * (1 + number of squares left empty) and if the other_player wins the game then the score is calcualted as -1 * (1 + number of squares left empty) and 0 in case of a draw
        1 is added because if a player wins at the last move, then if 1 is not added then the score will be 0 which will be confused with draw by the computer hence to avoid that situation and get the correct result, 1 is added to the number of squares left empty when a player wins the game
        And the score of max_player is positive because we want to maximize the win of the max_player and the score of other_player is calculated as negative because we want to minimize the loss of that player, we can think of it as the X-axis, if a value will be above x axis then the chances of max_player win will increase and if the value is below x-axis then the chances of win of other_player will increase.
        So for max_player higher will be the score, higher will be the chances of winning and for other_player lower will be the score, lower will be chances of winning.)
        """
        max_player = self.letter
        other_player = "O" if player == "X" else "X"

        # Defining the exit condition for the recursion
        # We are checking the condition against other_player because if we make a move, we won't be checking if the player has won the game or not
        # And for the next move we will change the player, hence the player who made the last move will be other_player.
        if state.the_winner == other_player:
            return {"position": None, "score": 1 * (1 + state.number_of_empty_squares()) if other_player == max_player else -1 * (1 + state.number_of_empty_squares())}
        elif not state.number_of_empty_squares():  # 0 is treated as False
            return {"position": None, "score": 0}  # Draw condition responce

        if player == max_player:
            # So that we can maximize the score for max_player
            best = {"postion": None, "score": -math.inf}
        else:
            # And minimize the score for other_player
            best = {"positon": None, "score": math.inf}

        # Now we will try to simulate what will be happen on making which of the empty squares and calculate a score for that move
        # If the score will be greater than the best["score"] for max_player then we will update the best position and score
        # And for other_player, we will update the best["score"] if the score is less than the best["score"]

        # The whole process is divided into 4 parts
        for possible_move in state.available_moves():
            # First is to make the move
            state.make_move(player, possible_move)

            # Second step is to get the score on the basis of that move
            simulation = self.minimax(state, other_player)

            # Third step is to undo the move
            state.board[possible_move] = " "
            state.the_winner = None
            # Updating the position, going to which we got the current score
            simulation["position"] = possible_move

            # Now, the final step is to update the best score, based on minimizer of maximizer
            if player == max_player:
                if simulation["score"] > best["score"]:
                    best = simulation
            else:
                if simulation["score"] < best["score"]:
                    best = simulation

        # At last we return the best simulation results
        return best

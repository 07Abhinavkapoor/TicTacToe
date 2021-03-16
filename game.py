from players import HumanPlayer, ComputerPlayer


class TicTacToe:
    """
    The main game.
    """

    def __init__(self):
        self.board = [" " for i in range(9)]
        self.the_winner = None

    def print_board(self):
        """
        To print the board.

        Parameters: None

        Returns: None
        """
        x_value = "\033[1;31mX\033[0;37m"
        o_value = "\033[1;34mO\033[0;37m"
        rows = [[str(i) if self.board[i] == " " else x_value if self.board[i] == "X" else o_value
                 for i in range(j*3, (j+1)*3)] for j in range(3)]

        for row in rows:
            print("| " + " | ".join(row) + " |")

    def available_moves(self):
        """
        To get the index of empty squares.

        Parameters: None

        Returns:
        List - which contains the indexes of the empty squares.
        """
        return [i for (i, spot) in enumerate(self.board) if spot == " "]

    def has_empty_squares(self):
        """
        To check if there are any empty squares or not.

        Parameters: None

        Returns: 
        boolean - if any of the square is empty in the board or not.
        """
        return " " in self.board

    def number_of_empty_squares(self):
        """
        To get the number of empty squares.

        Parameters: None

        Returns:
        int - the number of empty squares left in the board.
        """
        return len(self.available_moves())

    def make_move(self, letter, square):
        """
        To mark the square with appropriate letter on the board.

        Parameters:
        letter(char) - The letter which is to be inserted.
        square(int) - The index on which the letter is to be inserted.

        Returns:
        boolean - Indicating if the operation was successful or not.
        """
        if self.board[square] == " ":
            self.board[square] = letter
            if self.is_winner(letter, square):
                self.the_winner = letter
            return True

        return False

    def is_winner(self, letter, square):
        """
        To check if a player has won the game or not.

        Parameters:
        letter(char) - The letter whose win is to be checked.
        square(int) - The postion along which the row, column and diagonal items are checked.

        Returns:
        boolean - True if the player won, else False
        """
        # One can win the game if all the squares either in row, or column or diagonals have same letter

        # First we will check for row
        row_index = square // 3
        row = self.board[row_index*3: (row_index+1)*3]

        if all([spot == letter for spot in row]):
            return True

        # Next we will check for column
        col_index = square % 3
        col = [self.board[col_index + i * 3] for i in range(3)]

        if all([spot == letter for spot in col]):
            return True

        # Next we will check for diagonals
        # If we look at the indexes of the squares then we will notice that the all the even indexes are the ones which lie on diagonal
        # Index 0, 2, 4, 6, 8 lie on diagonals
        # Index 0, 4, 8 forms the left diagonal
        # Index 2, 4, 6 forms the right diagonal

        if square % 2 == 0:
            # If the sqaure lies on a diagonal then only we will check for the diagonal condition else not.

            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True

            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False


def play(game, x_player, o_player, print_game=True):
    """
    To play the game.

    Parameters:
    game(TicTacToe) - The instance of the game which is to be played, like selecting a board from multiple boards.
    x_player(Player) - The Player instance which will be using the letter 'X'
    o_player(Player) - The Player instance which will be using the letter 'O'
    print_game(boolean) - Indicating if the data related to moves is to printed after each turn or not.

    Returns:
    string: "None" if the game ends in a tie, else the letter of the winner.
    """
    if print_game:
        game.print_board()

    letter = "X"  # Starting letter

    while game.has_empty_squares():
        if letter == "X":
            square = x_player.get_move(game)
        else:
            square = o_player.get_move(game)

        if game.make_move(letter, square):
            if print_game:
                val = f"\033[1;93m{letter}\033[0;37m"
                squ = f"\033[1;36m{square}\033[0;37m"
                print(f"{val} made the move at square {squ}")

                game.print_board()
                print("\n")

        if game.the_winner:
            game.print_board()
            print("")
            return letter

        # Changing Turns
        letter = "O" if letter == "X" else "X"

    return "None"


def menu():
    """
    Main menu of the game, to select from multiple modes.

    Parameters: None

    Returns:
    string - The value returned by play() method.
    """
    while True:
        print("")
        print("-"*20 + "\033[1;32mTic-Tac-Toe\033[0;37m" + "-"*20)
        print("")
        print("\t\t Choose the Mode \t\t")
        print("")
        print("\t1. Human Vs Human")
        print("\t2. Human Vs Computer")
        print("\t3. Quit")

        option = input("> ")

        if option == "1":
            return human_vs_human_mode()
        elif option == "2":
            return select_difficulty()
        elif option == "3":
            exit()
        else:
            print("Invalid Input. Try Again.")


def human_vs_human_mode():
    """
    To start a game in which 2 humans play against each other.

    Parameters: None

    Returns:
    string - The value returned by play().
    """
    game = TicTacToe()
    x_player = HumanPlayer("X")
    o_player = HumanPlayer("O")

    return play(game, x_player, o_player)


def select_difficulty():
    """
    To select the difficulty when a human plays aginst a computer.

    Parameters: None

    Returns:
    string - The value returned by the play() method.
    """
    while True:
        print("\t\t Choose the Difficulty \t\t")
        print("")
        print("\t1. Easy")
        print("\t2. Hard")
        print("\t3. Quit")

        option = input("> ")

        if option == "1":
            return human_vs_computer_mode(0)
        elif option == "2":
            return human_vs_computer_mode(1)
        elif option == "3":
            exit()
        else:
            print("Invalid Input. Try Again.")


def human_vs_computer_mode(difficulty):
    """
    To start the game in which a human plays against the computer.

    Paramters:
    difficulty(int) -  0 if the level of difficulty should be easy, and 1 if the level should be hard.

    Returns:
    string - The value returned by the play() method.

    """
    game = TicTacToe()
    x_player = HumanPlayer("X")
    o_player = ComputerPlayer(
        "O") if difficulty == 0 else ComputerPlayer("O", smart=True)

    return play(game, x_player, o_player)


if __name__ == "__main__":
    result = menu()

    if result == "None":
        print("\033[1;32mIt's a Tie\033[0;37m\n")

    else:
        result = f"\033[1;35m{result}\033[0;37m"
        print(f"{result} is the winner")

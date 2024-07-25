import pygame
import sys
import random
from tkinter import messagebox, Tk

# Initialize Pygame
pygame.init()

# Constants defining the size of the board and squares
ROWS, COLS = 6, 5
SQUARE_SIZE = 100
WIDTH, HEIGHT = COLS * SQUARE_SIZE, ROWS * SQUARE_SIZE + 50  # Extra space for reshuffle button

# Define colors used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Initialize the screen with the given dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers-like Game')

# Initialize fonts for rendering text
FONT = pygame.font.SysFont('Arial', 24)

# Define the reshuffle button properties
RESHUFFLE_BTN = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 40)
RESHUFFLE_BTN_COLOR = (200, 200, 200)
RESHUFFLE_BTN_TEXT = FONT.render('Reshuffle', True, BLACK)

class Piece:
    """
    Represents a game piece on the board.
    """
    PADDING = 15  # Padding inside the piece's circle
    OUTLINE = 2   # Outline thickness of the piece's circle

    def __init__(self, row, col, color):
        """
        Initializes a Piece object.

        Parameters:
        row (int): Row position on the board.
        col (int): Column position on the board.
        color (tuple): Color of the piece.
        """
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.calc_pos()  # Calculate the piece's position on the screen

    def calc_pos(self):
        """
        Calculates the screen position of the piece based on its row and column.
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, screen):
        """
        Draws the piece on the screen.

        Parameters:
        screen (Surface): The Pygame surface to draw on.
        """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(screen, GRAY, (self.x, self.y), radius + self.OUTLINE)  # Draw the piece's outline
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius)  # Draw the piece's color

    def move(self, row, col):
        """
        Moves the piece to a new position on the board.

        Parameters:
        row (int): New row position on the board.
        col (int): New column position on the board.
        """
        self.row = row
        self.col = col
        self.calc_pos()  # Recalculate the piece's position on the screen

def create_board():
    """
    Creates the initial board setup with pieces for red and blue players.

    Returns:
    list: A 2D list representing the board with Piece objects and empty cells.
    """
    board = []
    for row in range(ROWS):
        board.append([])
        for col in range(COLS):
            if row == 0:
                board[row].append(Piece(row, col, BLUE))  # Add blue pieces to the first row
            elif row == ROWS - 1:
                board[row].append(Piece(row, col, RED))  # Add red pieces to the last row
            else:
                board[row].append(0)  # Empty cells
    return board

def generate_mines(board, num_mines=4):
    """
    Randomly generates a set of mines on the board.

    Parameters:
    board (list): The current state of the board.
    num_mines (int): Number of mines to generate.

    Returns:
    set: A set of coordinates where mines are placed.
    """
    mines = set()
    while len(mines) < num_mines:
        row = random.randint(1, ROWS - 2)
        col = random.randint(0, COLS - 1)
        if board[row][col] == 0:
            # Ensure no two mines are adjacent in the same row
            if all((row, col + offset) not in mines for offset in [-1, 1]):
                mines.add((row, col))
    return mines

def draw_board(screen, board, mines, turn, red_shuffles, blue_shuffles):
    """
    Draws the game board including pieces and mines.

    Parameters:
    screen (Surface): The Pygame surface to draw on.
    board (list): The current state of the board.
    mines (set): The set of mine coordinates.
    turn (tuple): The color of the player whose turn it is.
    red_shuffles (int): Number of shuffles left for the red player.
    blue_shuffles (int): Number of shuffles left for the blue player.
    """
    screen.fill(WHITE)  # Fill the screen with white background

    for row in range(ROWS):
        for col in range(COLS):
            if (row, col) in mines:
                pygame.draw.rect(screen, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # Draw mines
            elif (row + col) % 2 == 0:
                pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # Draw black squares
            else:
                pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # Draw white squares

    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != 0:
                piece.draw(screen)  # Draw each piece on the board

    draw_reshuffle_button(screen, turn, red_shuffles, blue_shuffles)  # Draw the reshuffle button

def draw_reshuffle_button(screen, turn, red_shuffles, blue_shuffles):
    """
    Draws the reshuffle button and displays the number of reshuffles left for each player.

    Parameters:
    screen (Surface): The Pygame surface to draw on.
    turn (tuple): The color of the player whose turn it is.
    red_shuffles (int): Number of shuffles left for the red player.
    blue_shuffles (int): Number of shuffles left for the blue player.
    """
    pygame.draw.rect(screen, RESHUFFLE_BTN_COLOR, RESHUFFLE_BTN)  # Draw the reshuffle button
    screen.blit(RESHUFFLE_BTN_TEXT, (RESHUFFLE_BTN.x + 5, RESHUFFLE_BTN.y + 5))  # Draw the reshuffle button text

    # Display remaining reshuffles for each player
    red_text = FONT.render(f'Red Shuffles: {red_shuffles}', True, RED)
    blue_text = FONT.render(f'Blue Shuffles: {blue_shuffles}', True, BLUE)
    screen.blit(red_text, (10, HEIGHT - 30))  # Position red reshuffle text
    screen.blit(blue_text, (WIDTH - blue_text.get_width() - 10, HEIGHT - 30))  # Position blue reshuffle text

def get_row_col_from_mouse(pos):
    """
    Converts a mouse click position to board coordinates.

    Parameters:
    pos (tuple): The (x, y) position of the mouse click.

    Returns:
    tuple: The row and column coordinates on the board.
    """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def show_message(message):
    """
    Shows a message box with the game result.

    Parameters:
    message (str): The message to display.
    """
    root = Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Game Over", message)  # Show the message box
    try:
        root.destroy()  # Close the root window
    except:
        pass

def check_win_condition(board):
    """
    Checks if there is a winning condition on the board.

    Parameters:
    board (list): The current state of the board.

    Returns:
    str: A message indicating if the game is won or not.
    """
    for col in range(COLS):
        if isinstance(board[0][col], Piece) and board[0][col].color == RED:
            return "You won!"  # Red pieces in the first row means red won
        if isinstance(board[ROWS-1][col], Piece) and board[ROWS-1][col].color == BLUE:
            return "You lost!"  # Blue pieces in the last row means blue won
    return None

def check_no_pieces_left(board):
    """
    Checks if a player has lost all their pieces.

    Parameters:
    board (list): The current state of the board.

    Returns:
    str: A message indicating which player has lost all their pieces.
    """
    red_pieces = sum(isinstance(piece, Piece) and piece.color == RED for row in board for piece in row)
    blue_pieces = sum(isinstance(piece, Piece) and piece.color == BLUE for row in board for piece in row)
    if red_pieces == 0:
        return "Red lost!"  # Red player has no pieces left
    if blue_pieces == 0:
        return "Blue lost!"  # Blue player has no pieces left
    return None

def shuffle_mines(board, mines):
    """
    Shuffles the mines on the board to new positions.

    Parameters:
    board (list): The current state of the board.
    mines (set): The current set of mine coordinates.

    Returns:
    set: A new set of mine coordinates.
    """
    new_mines = generate_mines(board)
    while len(new_mines & mines) > 0:
        new_mines = generate_mines(board)  # Ensure no overlap with existing mines
    return new_mines

def evaluate(board):
    """
    Evaluates the board state for the minimax algorithm.

    Parameters:
    board (list): The current state of the board.

    Returns:
    int: The evaluation score of the board.
    """
    red_pieces = sum(isinstance(piece, Piece) and piece.color == RED for row in board for piece in row)
    blue_pieces = sum(isinstance(piece, Piece) and piece.color == BLUE for row in board for piece in row)
    return blue_pieces - red_pieces  # Positive score favors blue, negative favors red

def get_valid_moves(piece, board, mines):
    """
    Gets all valid moves for a given piece on the board.

    Parameters:
    piece (Piece): The piece to find moves for.
    board (list): The current state of the board.
    mines (set): The current set of mine coordinates.

    Returns:
    list: A list of valid moves for the piece.
    """
    if piece.color == RED:
        directions = [(-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1)]  # Moves for red pieces
    else:
        directions = [(1, 0), (1, -1), (1, 1), (0, -1), (0, 1)]  # Moves for blue pieces
    valid_moves = []
    for d in directions:
        r, c = piece.row + d[0], piece.col + d[1]
        if 0 <= r < ROWS and 0 <= c < COLS and (r, c) not in mines:
            if board[r][c] == 0:
                valid_moves.append((r, c))  # Empty cell is a valid move
            elif board[r][c].color != piece.color:
                valid_moves.append((r, c))  # Opponent's piece can be captured
    return valid_moves

def minimax(board, depth, alpha, beta, maximizing_player, mines):
    """
    Minimax algorithm with alpha-beta pruning to evaluate the best move.

    Parameters:
    board (list): The current state of the board.
    depth (int): The depth of the search tree.
    alpha (float): The best value that the maximizer can guarantee.
    beta (float): The best value that the minimizer can guarantee.
    maximizing_player (bool): True if it's the maximizing player's turn, False otherwise.
    mines (set): The current set of mine coordinates.

    Returns:
    int: The best evaluation score for the current player.
    """
    # Check for a win condition or if maximum depth is reached
    win_message = check_win_condition(board)
    if depth == 0 or win_message:
        if win_message == "You won!":
            return float('-inf')  # Maximizing player wins, return a very low score
        elif win_message == "You lost!":
            return float('inf')  # Minimizing player wins, return a very high score
        return evaluate(board)  # Return board evaluation score if no win/loss

    if maximizing_player:
        # Maximizing player's turn
        max_eval = float('-inf')  # Start with the lowest possible evaluation
        for row in board:
            for piece in row:
                if isinstance(piece, Piece) and piece.color == BLUE:
                    # For each blue piece, evaluate all possible moves
                    for move in get_valid_moves(piece, board, mines):
                        new_board = [list(r) for r in board]  # Create a copy of the board
                        new_piece = Piece(move[0], move[1], piece.color)  # Create a new piece in the new position
                        new_board[piece.row][piece.col], new_board[move[0]][move[1]] = 0, new_piece
                        # Recursively call minimax for the next turn
                        eval = minimax(new_board, depth - 1, alpha, beta, False, mines)
                        max_eval = max(max_eval, eval)  # Update max_eval with the best score found
                        alpha = max(alpha, eval)  # Update alpha with the best score for the maximizing player
                        if beta <= alpha:
                            break  # Beta cut-off: stop exploring this branch
        return max_eval  # Return the best score for the maximizing player

    else:
        # Minimizing player's turn
        min_eval = float('inf')  # Start with the highest possible evaluation
        for row in board:
            for piece in row:
                if isinstance(piece, Piece) and piece.color == RED:
                    # For each red piece, evaluate all possible moves
                    for move in get_valid_moves(piece, board, mines):
                        new_board = [list(r) for r in board]  # Create a copy of the board
                        new_piece = Piece(move[0], move[1], piece.color)  # Create a new piece in the new position
                        new_board[piece.row][piece.col], new_board[move[0]][move[1]] = 0, new_piece
                        # Recursively call minimax for the next turn
                        eval = minimax(new_board, depth - 1, alpha, beta, True, mines)
                        min_eval = min(min_eval, eval)  # Update min_eval with the worst score found
                        beta = min(beta, eval)  # Update beta with the best score for the minimizing player
                        if beta <= alpha:
                            break  # Alpha cut-off: stop exploring this branch
        return min_eval  # Return the best score for the minimizing player

def best_move(board, mines):
    """
    Determines the best move for the AI using the minimax algorithm.

    Parameters:
    board (list): The current state of the board.
    mines (set): The current set of mine coordinates.

    Returns:
    tuple: The best piece and move for the AI, or None if no moves are found.
    """
    best_moves = []
    best_eval = float('-inf')
    for row in board:
        for piece in row:
            if isinstance(piece, Piece) and piece.color == BLUE:
                for move in get_valid_moves(piece, board, mines):
                    new_board = [list(r) for r in board]
                    new_piece = Piece(move[0], move[1], piece.color)
                    new_board[piece.row][piece.col], new_board[move[0]][move[1]] = 0, new_piece
                    eval = minimax(new_board, 3, float('-inf'), float('inf'), False, mines)
                    if eval > best_eval:
                        best_eval = eval
                        best_moves = [(piece, move)]
                    elif eval == best_eval:
                        best_moves.append((piece, move))
    return random.choice(best_moves) if best_moves else None

def find_winning_move(board, mines):
    """
    Finds a winning move for the AI.

    Parameters:
    board (list): The current state of the board.
    mines (set): The current set of mine coordinates.

    Returns:
    tuple: The winning piece and move for the AI, or None if no winning move is found.
    """
    for row in board:
        for piece in row:
            if isinstance(piece, Piece) and piece.color == BLUE:
                for move in get_valid_moves(piece, board, mines):
                    if move[0] == ROWS - 1:  # Check if the move leads to the last row
                        return piece, move
    return None

def blue_shuffle_condition(board, mines, eval_value):
    """
    Determines if the blue player should shuffle mines based on certain conditions.

    Parameters:
    board (list): The current state of the board.
    mines (set): The current set of mine coordinates.
    eval_value (int): The evaluation score of the board.

    Returns:
    bool: True if the blue player should shuffle mines, False otherwise.
    """
    # Check if any red piece is 2 rows from the last row
    for col in range(COLS):
        if isinstance(board[2][col], Piece) and board[2][col].color == RED:
            return True

    # Check if the evaluation score is negative
    if eval_value < 0:
        return True

    return False

def main():
    """
    Main function to run the game loop.
    """
    board = create_board()  # Initialize the game board
    mines = generate_mines(board)  # Place mines on the board

    # Randomly decide which player (Red or Blue) starts
    turn = random.choice([RED, BLUE])
    start_message = "Red" if turn == RED else "Blue"

    # Display who starts the game
    screen.fill(WHITE)  # Clear the screen with white color
    start_text = FONT.render(f"After tossing the coin, {start_message} starts!", True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.flip()  # Update the display
    pygame.time.wait(2000)  # Wait for 2 seconds to show the starting message

    selected_piece = None  # Track the currently selected piece
    running = True  # Game loop flag
    red_shuffles = 2  # Number of reshuffles left for the red player
    blue_shuffles = 2  # Number of reshuffles left for the blue player
    blue_reshuffled = False  # Track if blue player has reshuffled this turn

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop if the window is closed

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # Get the mouse click position
                if RESHUFFLE_BTN.collidepoint(pos):
                    # Handle reshuffle button click
                    if turn == RED and red_shuffles > 0:
                        mines = shuffle_mines(board, mines)  # Shuffle mines for Red player
                        red_shuffles -= 1
                    elif turn == BLUE and blue_shuffles > 0 and not blue_reshuffled:
                        mines = shuffle_mines(board, mines)  # Shuffle mines for Blue player
                        blue_shuffles -= 1
                        blue_reshuffled = True
                else:
                    row, col = get_row_col_from_mouse(pos)  # Convert mouse position to board coordinates
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        piece = board[row][col]
                        if piece != 0 and piece.color == turn:
                            selected_piece = piece  # Select the piece if it belongs to the current player
                        elif selected_piece:
                            if (row, col) in get_valid_moves(selected_piece, board, mines):
                                # Move the selected piece to the new position if the move is valid
                                board[row][col] = selected_piece
                                board[selected_piece.row][selected_piece.col] = 0
                                selected_piece.move(row, col)
                                selected_piece = None
                                turn = BLUE if turn == RED else RED  # Switch turn

        # Check for win or lose conditions
        win_message = check_win_condition(board)
        if win_message:
            show_message(win_message)  # Display win message
            running = False

        lose_message = check_no_pieces_left(board)
        if lose_message:
            show_message(lose_message)  # Display lose message
            running = False

        # AI move for Blue player
        if turn == BLUE:
            if blue_reshuffled:
                blue_reshuffled = False
            else:
                winning_move = find_winning_move(board, mines)
                if winning_move:
                    # Execute the winning move if available
                    piece, move = winning_move
                    board[move[0]][move[1]] = piece
                    board[piece.row][piece.col] = 0
                    piece.move(move[0], move[1])
                    turn = RED  # Switch turn to Red player
                else:
                    # Determine the best move using the minimax algorithm
                    best = best_move(board, mines)
                    if best:
                        piece, move = best
                        board[move[0]][move[1]] = piece
                        board[piece.row][piece.col] = 0
                        piece.move(move[0], move[1])
                        turn = RED  # Switch turn to Red player

        # Draw the board and update the display
        draw_board(screen, board, mines, turn, red_shuffles, blue_shuffles)
        pygame.display.flip()  # Refresh the display

    pygame.quit()  # Quit Pygame
    sys.exit()  # Exit the program

if __name__ == "__main__":
    main()  # Run the main function

if __name__ == "__main__":
    main()  # Run the main function

import numpy as np
import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
WIN_COLOR = (255, 215, 0)  # Gold for winner text

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Unbeatable Tic-Tac-Toe')
screen.fill(BG_COLOR)

# Font
font = pygame.font.SysFont('Arial', 40)
restart_font = pygame.font.SysFont('Arial', 30)

# Board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Draw lines
def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw X and O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # O for human
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                 (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                  int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 
                                 CIRCLE_RADIUS, LINE_WIDTH)
            elif board[row][col] == 2:  # X for AI
                pygame.draw.line(screen, CROSS_COLOR, 
                                (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), 
                                CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                CROSS_WIDTH)

# Mark square
def mark_square(row, col, player):
    board[row][col] = player

# Check if square is available
def available_square(row, col):
    return board[row][col] == 0

# Check if board is full
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

# Check for win
def check_win(player):
    # Vertical win
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # Horizontal win
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # Diagonal win
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(2):
        return 1
    elif check_win(1):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -np.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = np.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# AI move
def best_move():
    best_score = -np.inf
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

# Display winner text
def show_winner(winner):
    if winner == 1:
        text = font.render('You Win!', True, WIN_COLOR)
    elif winner == 2:
        text = font.render('AI Wins!', True, WIN_COLOR)
    else:
        text = font.render('Draw!', True, WIN_COLOR)
    
    restart_text = restart_font.render('Press R to Restart', True, TEXT_COLOR)
    
    # Dark semi-transparent overlay
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))  # Black with 50% opacity
    screen.blit(s, (0, 0))
    
    # Center the text
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

# Reset game
def reset_game():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# Main game loop
def main():
    draw_lines()
    player = 1  # 1 for human (O), 2 for AI (X)
    game_over = False
    winner = None  # 1 for human, 2 for AI, 0 for draw

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    reset_game()
                    game_over = False
                    winner = None
                    player = 1

            if not game_over and player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if available_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, player)
                    if check_win(player):
                        game_over = True
                        winner = player
                    elif is_board_full():
                        game_over = True
                        winner = 0
                    else:
                        player = 2

        if not game_over and player == 2:
            if best_move():
                if check_win(2):
                    game_over = True
                    winner = 2
                elif is_board_full():
                    game_over = True
                    winner = 0
                else:
                    player = 1

        draw_figures()
        
        if game_over:
            show_winner(winner)
        
        pygame.display.update()

if __name__ == "__main__":
    main()
    
# python project_mini.py
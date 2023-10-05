import pygame
import sys
import random

#Configuracion de Pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

#Colores
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 128)
BUTTON_COLOR = (100, 100, 100)
TEXT_COLOR = (128, 0, 128)

#Fuentes
FONT = pygame.font.Font(None, 30)

#Inicializar la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego Tres en Línea")

#Tablero
board = [["" for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

#Funcion para dibujar el tablero
def draw_board():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

#Funcion para dibujar las fichas
def draw_markers():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                                 ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE),
                                 (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, LINE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - LINE_WIDTH)

#Funcion para verificar si el juego ha terminado (victoria o empate)
def is_game_over():
    #Verificar filas y columnas para la victoria
    for i in range(BOARD_ROWS):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return True
        if board[0][i] == board[1][i] == board[2][i] != "":
            return True

    #Verificar diagonales para la victoria
    if board[0][0] == board[1][1] == board[2][2] != "":
        return True
    if board[0][2] == board[1][1] == board[2][0] != "":
        return True

    #Verificar empate
    for row in board:
        for cell in row:
            if cell == "":
                return False
    return True

#Funcion para evaluar la posición actual del tablero
def evaluate():
    if is_game_over():
        if has_won("X"):
            return 1
        elif has_won("O"):
            return -1
        else:
            return 0
    else:
        return 0

#Funcion para verificar si un jugador ha ganado
def has_won(player):
    for i in range(BOARD_ROWS):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

#Funcion Minimax
#La IA toma decisiones
def minimax(board, depth, is_maximizing):
    if is_game_over():
        return evaluate()

    if is_maximizing:
        max_eval = float("-inf")
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == "":
                    board[row][col] = "X"
                    eval = minimax(board, depth + 1, False)
                    board[row][col] = ""
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == "":
                    board[row][col] = "O"
                    eval = minimax(board, depth + 1, True)
                    board[row][col] = ""
                    min_eval = min(min_eval, eval)
        return min_eval
#Funcion Minimax
#Funcion para que la IA haga su movimiento
def make_ia_move():
    best_move = None
    best_eval = float("-inf")
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "":
                board[row][col] = "X"
                eval = minimax(board, 0, False)
                board[row][col] = ""
                if eval > best_eval:
                    best_eval = eval
                    best_move = (row, col)
    board[best_move[0]][best_move[1]] = "X"

#Funcion para reiniciar la interfaz
def reset_game():
    global board
    board = [["" for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    screen.fill(WHITE)
    draw_board()
    pygame.display.update()

#Funcion principal
def play_game():
    player_turn = random.choice(["O", "X"])
    while not is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if player_turn == "O":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    clicked_row, clicked_col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE
                    if board[clicked_row][clicked_col] == "":
                        board[clicked_row][clicked_col] = "O"
                        player_turn = "X"

        screen.fill(WHITE)
        draw_board()
        draw_markers()
        pygame.display.update()

        if player_turn == "X" and not is_game_over():
            make_ia_move()
            player_turn = "O"

        pygame.display.update()

    #Muestra el resultado
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                reset_game()

        result_text = "EMPATE!" if evaluate() == 0 else "GANASTE!" if evaluate() == -1 else "LA IA GANÓ"
        result_surface = FONT.render(result_text, True, TEXT_COLOR)
        result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(result_surface, result_rect)
        pygame.display.update()

#Iniciar el juego
if __name__ == "__main__":
    play_game()
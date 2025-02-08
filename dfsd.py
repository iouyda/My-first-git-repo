import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню игр by iouyda")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

font = pygame.font.Font(None, 36)

def draw_button(screen, msg, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    text_surface = font.render(msg, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_surface, text_rect)
    return False

def guess_number():
    number = random.randint(1, 100)
    guess = None
    attempts = 0

    guess_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Угадайка чисел")

    input_box = pygame.Rect(300, 250, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        guess_screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            guess = int(text)
                            attempts += 1
                            if guess == number:
                                message = f"Поздравляем! Вы угадали число за {attempts} попыток!"
                                done = True
                            elif guess < number:
                                message = "Загаданное число больше!"
                            elif guess > number:
                                message = "Загаданное число меньше!"
                        except ValueError:
                            message = "Введите число!"
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        guess_screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(guess_screen, color, input_box, 2)

        if guess is not None:
            msg_surface = font.render(message, True, BLACK)
            guess_screen.blit(msg_surface, (300, 350))

        pygame.display.flip()

def tic_tac_toe():
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    player = 'X'
    game_over = False

    tic_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Крестики-нолики by iouyda")

    def draw_board():
        tic_screen.fill(WHITE)
        pygame.draw.line(tic_screen, BLACK, (300, 100), (300, 700), 5)
        pygame.draw.line(tic_screen, BLACK, (500, 100), (500, 700), 5)
        pygame.draw.line(tic_screen, BLACK, (100, 300), (700, 300), 5)
        pygame.draw.line(tic_screen, BLACK, (100, 500), (700, 500), 5)

        for i in range(3):
            for j in range(3):
                if board[i][j] == 'X':
                    pygame.draw.line(tic_screen, BLACK, (100 + j * 200, 100 + i * 200), (300 + j * 200, 300 + i * 200), 5)
                    pygame.draw.line(tic_screen, BLACK, (300 + j * 200, 100 + i * 200), (100 + j * 200, 300 + i * 200), 5)
                elif board[i][j] == 'O':
                    pygame.draw.circle(tic_screen, BLACK, (200 + j * 200, 200 + i * 200), 50, 5)

    def check_winner():
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != '':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != '':
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '':
            return board[0][2]
        return None

    while not game_over:
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = (y - 100) // 200
                col = (x - 100) // 200
                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == '':
                    board[row][col] = player
                    winner = check_winner()
                    if winner:
                        game_over = True
                    player = 'O' if player == 'X' else 'X'

        pygame.display.flip()

def snake_game():
    snake_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка by iouyda")

    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    food_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]
    food_spawn = True
    score = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]
        food_spawn = True

        snake_screen.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(snake_screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(snake_screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10 or snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
            break
        for block in snake_body[1:]:
            if snake_pos == block:
                break

        pygame.display.flip()
        clock.tick(15)

running = True
while running:
    screen.fill(WHITE)

    # Рисуем кнопки
    if draw_button(screen, "Угадай число", 300, 100, 200, 100, GREEN, (0, 200, 0)):
        guess_number()
    if draw_button(screen, "Крестики-нолики", 290, 250, 220, 100, BLUE, (0, 0, 200)):
        tic_tac_toe()
    if draw_button(screen, "Змейка", 300, 400, 200, 100, RED, (200, 0, 0)):
        snake_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
import pygame
import os

pygame.init()

# Initialize the game window
background = pygame.display.set_mode((1680, 960))
pygame.display.set_caption("벽돌 깨기")

fps = pygame.time.Clock()

# Load the background image
background_image = pygame.image.load(os.path.join("background.jpg"))
background_image = pygame.transform.scale(background_image, (1680, 960))

# Screen size variables
screen_width = background.get_size()[0]
screen_height = background.get_size()[1]


# Game text function
def game_text(word):
    font = pygame.font.SysFont(None, 100)
    text = font.render(word, True, (255, 255, 255))

    text_width = text.get_rect().size[0]
    text_height = text.get_rect().size[1]

    text_x_pos = screen_width // 2 - text_width // 2
    text_y_pos = screen_height // 2 - text_height // 2

    background.blit(text, (text_x_pos, text_y_pos))


# Paddle variables
paddle_width = 100
paddle_height = 30

paddle_x_pos = screen_width // 2 - paddle_width // 2
paddle_y_pos = screen_height - paddle_height - 100

paddle_to_x = 0
paddle_speed = 20

# Ball variables
ball_image = pygame.image.load(os.path.join("ball.png"))
ball_image = pygame.transform.scale(ball_image, (50, 100))
ball_width = ball_image.get_width()
ball_height = ball_image.get_height()

ball_x_pos = screen_width // 2
ball_y_pos = screen_height - paddle_height - ball_height - 100

ball_to_x = 5  # Adjust the ball's horizontal movement speed
ball_to_y = 5  # Adjust the ball's vertical movement speed

# Brick variables
brick_width = 100
brick_height = 30

brick_x_pos = 0
brick_y_pos = 0

brick_rect = [[] for _ in range(14)]

# Define the rainbow colors
rainbow_colors = [
    (255, 0, 0),     # Red
    (255, 165, 0),   # Orange
    (255, 255, 0),   # Yellow
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (75, 0, 130),    # Indigo
    (148, 0, 211)    # Violet
]

for column in range(14):
    for row in range(3):
        brick_rect[column].append(pygame.Rect(70 + column * (brick_width + 10), 100 + row * (brick_height + 10),
                                              brick_width, brick_height))

point = 0
start = True
play = True

while play:
    dt = fps.tick(60)

    # Display the title for 2 seconds
    if start:
        start = False
        title_font = pygame.font.SysFont(None, 100)
        title_text = title_font.render("Miyo says meow", True, (255, 165, 0))
        title_text_outline = title_font.render("Miyo says meow", True, (0, 0, 0))
        title_text_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2))
        background.blit(title_text_outline, title_text_rect.move(2, 2))
        background.blit(title_text_outline, title_text_rect.move(-2, -2))
        background.blit(title_text_outline, title_text_rect.move(2, -2))
        background.blit(title_text_outline, title_text_rect.move(-2, 2))
        background.blit(title_text, title_text_rect)
        pygame.display.update()
        pygame.time.delay(2000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                       
            play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                play = False
            elif event.key == pygame.K_LEFT:
                paddle_to_x -= paddle_speed
            elif event.key == pygame.K_RIGHT:
                paddle_to_x += paddle_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle_to_x = 0

    paddle_x_pos += paddle_to_x
    paddle_rect = pygame.Rect(paddle_x_pos, paddle_y_pos, paddle_width, paddle_height)

    background.blit(background_image, (0, 0))

    pygame.draw.rect(background, (254, 254, 254), paddle_rect)

    if paddle_x_pos <= 0:
        paddle_x_pos = 0
    elif paddle_x_pos + paddle_width >= screen_width:
        paddle_x_pos = screen_width - paddle_width

    if ball_x_pos - ball_width // 2 <= 0:
        ball_to_x = -ball_to_x
    elif ball_x_pos + ball_width // 2 >= screen_width:
        ball_to_x = -ball_to_x

    if ball_y_pos - ball_height // 2 <= 0:
        ball_to_y = -ball_to_y
    elif ball_y_pos + ball_height // 2 >= screen_height:
        game_text("GAME OVER")
        pygame.display.update()
        pygame.time.delay(1000)
        break

    ball_x_pos += ball_to_x
    ball_y_pos += ball_to_y

    background.blit(ball_image, (ball_x_pos - ball_width // 2, ball_y_pos - ball_height // 2))
    ball_rect = pygame.Rect(ball_x_pos - ball_width // 2, ball_y_pos - ball_height // 2, ball_width, ball_height)

    if ball_rect.colliderect(paddle_rect):
        ball_to_y = -ball_to_y
        if paddle_x_pos + paddle_width // 2 - 5 <= ball_rect.center[0] <= paddle_x_pos + paddle_width // 2 + 5:
            ball_to_x = 0.1 * ball_to_x
            print('real_center : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
        elif paddle_x_pos + paddle_width // 2 - 10 <= ball_x_pos <= paddle_x_pos + paddle_width // 2 + 10:
            ball_to_x = 0.8 * ball_to_x
            print('center : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
        elif paddle_x_pos + paddle_width // 2 - 30 <= ball_x_pos <= paddle_x_pos + paddle_width // 2 - 10:
            ball_to_x = max(-2 - abs(ball_to_x) * 2, -5)
            print('left_center : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
        elif ball_x_pos <= paddle_x_pos + paddle_width // 2 - 30:
            ball_to_x = max(-5 - abs(ball_to_x) * 5, -10)
            print('left : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
        elif paddle_x_pos + paddle_width // 2 + 10 <= ball_x_pos <= paddle_x_pos + paddle_width // 2 + 30:
            ball_to_x = min(2 + abs(ball_to_x) * 2, 5)
            print('right_center : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
        elif paddle_x_pos + paddle_width // 2 + 30 <= ball_x_pos:
            ball_to_x = min(5 + abs(ball_to_x) * 5, 10)
            print('right : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))

    for column in range(14):
        for row in range(3):
            if brick_rect[column][row]:
                color_index = int(column / 14 * len(rainbow_colors))
                brick_color = rainbow_colors[color_index]
                pygame.draw.rect(background, brick_color, brick_rect[column][row])
                brick_rect[column][row].topleft = (70 + column * (brick_width + 10), 100 + row * (brick_height + 10))
                if ball_rect.colliderect(brick_rect[column][row]):
                    ball_to_y = -ball_to_y
                    brick_rect[column][row] = 0
                    point += 1

    if point == 42:
        game_text("GAME CLEAR")
        pygame.display.update()
        pygame.time.delay(1000)
        play = False

    pygame.display.update()

pygame.quit()

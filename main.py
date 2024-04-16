import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
INDIGO = (75, 0, 130)

# Color palette for Tetris blocks and higher levels
colors = [BLACK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, INDIGO]

class Figure:
    # Define different Tetris figures
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # Square block
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # L-Shape block
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # Reverse L-Shape block
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # T-Shape block
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # Z-Shape block
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # S-Shape block
        [[1, 2, 5, 6]],  # Line block
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = self.type + 1
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

class Tetris:
    def __init__(self, height, width):
        self.level = 2  # Starting level
        self.score = 0  # Starting score
        self.state = "start"  # Initial game state
        self.field = [[0] * width for _ in range(height)]  # Game field
        self.height = height  # Height of the game field
        self.width = width    # Width of the game field
        self.x = 100          # X-coordinate for drawing the game field
        self.y = 60           # Y-coordinate for drawing the game field
        self.zoom = 20        # Size of each block in the game field
        self.figure = None    # Current active Tetris figure
        self.new_figure()     # Create a new Tetris figure

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        # Check if the current figure intersects with other blocks or the border
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if (
                        i + self.figure.y > self.height - 1
                        or j + self.figure.x > self.width - 1
                        or j + self.figure.x < 0
                        or self.field[i + self.figure.y][j + self.figure.x] > 0
                    ):
                        intersection = True
        return intersection

    def break_lines(self):
        # Break completed lines and update the score
        lines = 0
        for i in range(1, self.height):
            if all(self.field[i]):
                lines += 1
                del self.field[i]
                self.field.insert(0, [0] * self.width)
        self.score += lines ** 2

    def go_space(self):
        # Move the current figure all the way down and freeze it
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        # Move the current figure down
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        # Freeze the current figure in its position and check for game over
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        # Move the current figure sideways
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        # Rotate the current figure
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

# Initialize the game engine
pygame.init()
size = (400, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0
pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()  # Rotate the figure
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)  # Move the figure left
            if event.key == pygame.K_RIGHT:
                game.go_side(1)   # Move the figure right
            if event.key == pygame.K_SPACE:
                game.go_space()   # Move the figure all the way down
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)  # Reset the game
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(
                screen,
                GRAY,
                [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                1,
            )
            if game.field[i][j] > 0:
                pygame.draw.rect(
                    screen,
                    colors[game.field[i][j]],
                    [
                        game.x + game.zoom * j + 1,
                        game.y + game.zoom * i + 1,
                        game.zoom - 2,
                        game.zoom - 1,
                    ],
                )

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(
                        screen,
                        colors[game.figure.color],
                        [
                            game.x + game.zoom * (j + game.figure.x) + 1,
                            game.y + game.zoom * (i + game.figure.y) + 1,
                            game.zoom - 2,
                            game.zoom - 2,
                        ],
                    )

    font = pygame.font.SysFont("Calibri", 25, True, False)
    font1 = pygame.font.SysFont("Calibri", 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()


import pygame
import pygame.time
import random

# Global Variables
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

FPS = 10

CENTER = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

STOP = (0, 0)


class Snake:
    def __init__(self):
        self.length = 1
        self.score = 0
        self.positions = [CENTER]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = pygame.Color("darkgreen")
        self.outline_color = pygame.Color("slategrey")

    def get_head_position(self):
        return self.positions[0]

    def turn(self, new_dir):
        if self.length > 1 and (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return
        else:
            self.direction = new_dir

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new_pos = ((cur[0] + (x * GRID_SIZE)), cur[1] + (y * GRID_SIZE))
        if new_pos[0] < 0 or new_pos[0] >= SCREEN_WIDTH or new_pos[1] < 0 or new_pos[1] >= SCREEN_HEIGHT:
            self.die()
        elif len(self.positions) > 2 and new_pos in self.positions[2:]:
            self.die()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def die(self):
        self.length = 1
        self.positions = [CENTER]
        self.direction = STOP
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, self.outline_color, r, 1)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = pygame.Color("darkgoldenrod3")
        self.outline_color = pygame.Color("slategrey")
        self.randomize_position()

    def randomize_position(self):
        rand_x = random.randint(0, int(GRID_WIDTH - 1))
        rand_y = random.randint(0, int(GRID_HEIGHT - 1))
        self.position = (rand_x * GRID_SIZE, rand_y * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, self.outline_color, r, 1)


class World:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()

    def update(self):
        self.snake.move()
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.snake.score += 1
            self.food.randomize_position()

    def draw(self, surface):
        self.snake.draw(surface)
        self.food.draw(surface)

    def score(self):
        return self.snake.score

    def handle_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.turn(UP)
            elif event.key == pygame.K_DOWN:
                self.snake.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                self.snake.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                self.snake.turn(RIGHT)


def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color("lightslategrey"), r)
            else:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color("slategrey"), r)


def run():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Pygame Example")

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    draw_grid(surface)

    world = World()

    font = pygame.font.SysFont("monospace", 16)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    world.handle_keys(event)

        clock.tick(FPS)
        world.update()

        draw_grid(surface)
        world.draw(surface)

        screen.blit(surface, (0, 0))
        text = font.render("Score {0}".format(world.score()), 1, pygame.Color("black"))
        screen.blit(text, (5, 10))
        pygame.display.update()


if __name__ == '__main__':
    run()
    pygame.quit()

import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
snake_color = (0, 255, 0)
food_color = (255, 0, 0)
bg_color = (0, 0, 0)
cell_size = 10

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

snake = [(100, 50), (90, 50), (80, 50)]
snake_speed = 10
direction = RIGHT

food = (
	random.randint(0, WIDTH // cell_size - 1) * cell_size,
	random.randint(0, HEIGHT // cell_size - 1) * cell_size
)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and direction != DOWN:
				direction = UP
			elif event.key == pygame.K_DOWN and direction != UP:
				direction = DOWN
			elif event.key == pygame.K_LEFT and direction != RIGHT:
				direction = LEFT
			elif event.key == pygame.K_RIGHT and direction != LEFT:
				direction = RIGHT

	snake[0] = (
		snake[0][0] + direction[0] * cell_size,
		snake[0][1] + direction[1] * cell_size
	)

	if not (0 <= snake[0][0] < WIDTH and 0 <= snake[0][1] < HEIGHT) or snake[0] in snake[1:]:
		pygame.quit()
		sys.exit()

	if snake[0] == food:
		snake.append((0, 0))
		food = (
			random.randint(0, WIDTH // cell_size - 1) * cell_size,
			random.randint(0, HEIGHT // cell_size - 1) * cell_size
		)

	for i in range(len(snake) - 1, 0, -1):
		snake[i] = (snake[i - 1][0], snake[i - 1][1])

	screen.fill(bg_color)

	pygame.draw.rect(screen, food_color, (food[0], food[1], cell_size, cell_size))

	for segment in snake:
		pygame.draw.rect(screen, food_color, (segment[0], segment[1], cell_size, cell_size))

	pygame.display.flip()

	pygame.time.Clock().tick(snake_speed)

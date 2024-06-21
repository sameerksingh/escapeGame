import pygame
from utils.utils import generate_grid, draw_grid, handle_input, Player, place_start, congrats_popup
import constants as game_c


def main():
    pygame.init()
    screen = pygame.display.set_mode((game_c.SCREEN_WIDTH, game_c.SCREEN_HEIGHT))
    pygame.display.set_caption('Key Collector Game')

    clock = pygame.time.Clock()

    # Generate the grid
    m = 15
    n = 15
    num_keys = 5
    difficulty_factor = 0.4
    start_pos, grid, keys = generate_grid(m, n, num_keys, difficulty_factor)

    player = Player(*start_pos)
    collected_keys = []
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input
        handle_input(player, grid, keys, collected_keys)

        # Update game state

        # Draw grid
        screen.fill(game_c.WHITE)
        draw_grid(screen, grid, player, keys, collected_keys)
        pygame.display.flip()

        # Check if all keys are collected
        if len(collected_keys) == len(keys):
            game_over = True

        # If game over, display congrats popup
        if game_over:
            congrats_popup(screen)
            running = False

        clock.tick(15)

    pygame.quit()


if __name__ == "__main__":
    main()


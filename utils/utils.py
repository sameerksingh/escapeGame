import random
import pygame
import constants as game_c
from collections import deque


def generate_grid(m, n, num_keys, difficulty_factor):
    grid = [['.' for _ in range(n)] for _ in range(m)]

    # Place walls
    place_walls(grid, m, n, difficulty_factor)

    # Place keys and locks
    keys = place_keys(grid, m, n, num_keys)
    locks = place_locks(grid, m, n, num_keys)

    # Place starting point
    start_pos = place_start(grid, m, n)

    # Ensure all keys are reachable
    while all_keys_reachable(grid)==-1:
        grid = [['.' for _ in range(n)] for _ in range(m)]
        place_walls(grid, m, n, difficulty_factor)
        keys = place_keys(grid, m, n, num_keys)
        locks = place_locks(grid, m, n, num_keys)
        start_pos = place_start(grid, m, n)

    return start_pos, grid, keys


def place_walls(grid, m, n, difficulty_factor):
    for row in range(m):
        for col in range(n):
            if random.random() < difficulty_factor:
                grid[row][col] = '#'


def place_keys(grid, m, n, num_keys):
    # Let's randomly place keys and locks on the grid
    keys = []
    for i in range(num_keys):
        key = chr(ord('a') + i)
        row = random.randint(0, m - 1)
        col = random.randint(0, n - 1)
        grid[row][col] = key
        keys.append((key, (row, col)))
    return keys


def place_locks(grid, m, n, num_keys):
    locks = []
    for i in range(num_keys):
        lock = chr(ord('A') + i)
        while True:
            row = random.randint(0, m - 1)
            col = random.randint(0, n - 1)
            if grid[row][col] == '.':
                grid[row][col] = lock  # Ensure locks are represented by capital letters
                locks.append((lock, (row, col)))
                break
    return locks


def place_start(grid, m, n):
    # Let's randomly place the starting point on the grid
    while True:
        row = random.randint(0, m - 1)
        col = random.randint(0, n - 1)
        if grid[row][col] == '.':
            grid[row][col] = '@'
            return (row, col)


def all_keys_reachable(grid):
    # We'll use BFS to check if each key is reachable from the starting point
    n = len(grid)
    m = len(grid[0])
    cnt = 0
    a, b = 0, 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '@':
                a, b = i, j
            elif grid[i][j] in 'abcdef':
                cnt += 1
    vis = [[set() for i in range(m)] for __ in range(n)]
    q = deque()
    final_key_mask = 0
    for i in range(cnt):
        final_key_mask |= (1 << i)
    q.append((a, b, 0, 0, 0))
    while q:
        i, j, step, key_mask, unlocked_mask = q.popleft()
        if key_mask == final_key_mask:
            return step
        for dir1, dir2 in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x = i + dir1
            y = j + dir2
            if 0 <= x < n and 0 <= y < m and grid[x][y] != '#':
                new_key_mask = key_mask
                new_unlocked_mask = unlocked_mask
                if grid[x][y] in 'abcdef':
                    key_found = 1 << (ord(grid[x][y]) - ord('a'))
                    new_key_mask |= key_found
                elif grid[x][y] in 'ABCDEF':
                    lock_found = 1 << (ord(grid[x][y]) - ord('A'))
                    if lock_found & new_key_mask:
                        new_unlocked_mask |= lock_found
                    else:
                        continue
                state = (new_key_mask, new_unlocked_mask)
                if state in vis[x][y]:
                    continue
                q.append((x, y, step + 1, new_key_mask, new_unlocked_mask))
                vis[x][y].add(state)
    return -1


def draw_grid(screen, grid, player, keys, collected_keys):
    collected_keys_list = [x[0] for x in collected_keys]
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            rect = pygame.Rect(col_index * game_c.CELL_SIZE, row_index * game_c.CELL_SIZE, game_c.CELL_SIZE, game_c.CELL_SIZE)
            if cell == '#':
                pygame.draw.rect(screen, game_c.BLACK, rect)
            elif cell == '@':
                pygame.draw.rect(screen, game_c.GRAY, rect)
            elif cell.islower():
                pygame.draw.rect(screen, game_c.GREEN if cell in collected_keys_list else game_c.GRAY, rect)  # Key
                font = pygame.font.Font(None, 24)
                text_surface = font.render(cell, True, game_c.WHITE)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
            elif cell.isupper():
                pygame.draw.rect(screen, game_c.GRAY, rect)  # Lock
                font = pygame.font.Font(None, 24)
                text_surface = font.render(cell, True, game_c.WHITE)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

    # Draw player
    player_rect = pygame.Rect(player.col * game_c.CELL_SIZE, player.row * game_c.CELL_SIZE, game_c.CELL_SIZE, game_c.CELL_SIZE)
    pygame.draw.rect(screen, game_c.GRAY, player_rect)
    pygame.draw.circle(screen, game_c.BLACK, player_rect.center, game_c.CELL_SIZE // 2)

    # Draw collected keys
    collected_keys_text = "Collected Keys: "
    for key in collected_keys:
        collected_keys_text += key[0] + " "
    font = pygame.font.Font(None, 24)
    collected_keys_surface = font.render(collected_keys_text, True, game_c.BLACK)
    screen.blit(collected_keys_surface, (game_c.SCREEN_WIDTH - 200, 20))


class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move(self, dr, dc):
        self.row += dr
        self.col += dc


def handle_input(player, grid, keys, collected_keys):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT]:
        if player.col > 0 and grid[player.row][player.col - 1] != '#':
            handle_movement(player, grid, keys, collected_keys, 0, -1)
    elif keys_pressed[pygame.K_RIGHT]:
        if player.col < len(grid[0]) - 1 and grid[player.row][player.col + 1] != '#':
            handle_movement(player, grid, keys, collected_keys, 0, 1)
    elif keys_pressed[pygame.K_UP]:
        if player.row > 0 and grid[player.row - 1][player.col] != '#':
            handle_movement(player, grid, keys, collected_keys, -1, 0)
    elif keys_pressed[pygame.K_DOWN]:
        if player.row < len(grid) - 1 and grid[player.row + 1][player.col] != '#':
            handle_movement(player, grid, keys, collected_keys, 1, 0)


def handle_movement(player, grid, keys, collected_keys, dr, dc):
    new_row = player.row + dr
    new_col = player.col + dc

    # Check if new position is within bounds and not a wall
    if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] != '#':
        # Check if new position is a lock
        if grid[new_row][new_col].isupper():
            lock = grid[new_row][new_col]
            # Check if the player has the corresponding key
            if lock.lower() in [x[0] for x in collected_keys]:
                player.move(dr, dc)
        elif grid[new_row][new_col].islower():
            key = grid[new_row][new_col]
            if key.lower() not in [x[0] for x in collected_keys]:
                collected_keys.append((key, (new_row, new_col)))  # Update collected keys
            player.move(dr, dc)
        else:
            player.move(dr, dc)


def congrats_popup(screen):
    # Animation settings
    DISPLAY_DURATION = 2000  # Display duration in milliseconds

    # Main animation loop
    start_time = pygame.time.get_ticks()
    while True:
        # Calculate time elapsed
        elapsed_time = pygame.time.get_ticks() - start_time

        # Draw popup
        screen.fill((0, 0, 0))  # Clear screen
        font = pygame.font.Font(None, 72)
        text_surface = font.render("You Won!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(game_c.SCREEN_WIDTH // 2, game_c.SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        # Add fireworks particles
        if elapsed_time < DISPLAY_DURATION:
            fireworks(screen, text_rect.center)

        # Update screen
        pygame.display.flip()

        # Check if animation finished
        if elapsed_time >= DISPLAY_DURATION:
            break

        # Delay for smooth animation
        pygame.time.delay(10)


def fireworks(screen, center):
    # Number of particles
    num_particles = 150

    # Particle colors
    colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]

    # Generate particles
    for _ in range(num_particles):
        # Random position around the center
        x = center[0] + random.randint(-game_c.SCREEN_WIDTH//2, game_c.SCREEN_WIDTH//2)
        y = center[1] + random.randint(-game_c.SCREEN_HEIGHT//2, game_c.SCREEN_HEIGHT//2)

        # Random color
        color = random.choice(colors)

        # Draw particle
        pygame.draw.circle(screen, color, (int(x), int(y)), 3)


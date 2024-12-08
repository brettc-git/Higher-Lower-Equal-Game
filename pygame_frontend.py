import pygame
import os
import random
import game_engine as ge # Game Engine Functions

pygame.init()
pygame.display.set_caption("Higher-Lower-Equal Card Game")
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Cursor
system = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_NO)
directory = "assets/Card SVG files/"

# Load bg image and resize
casino_bg = pygame.image.load("assets/Casino_bg.jpg")
casino_bg = pygame.transform.scale(casino_bg, (1280, 720))

# Load back card and resize
back_card = pygame.image.load("assets/Card SVG files/BACK_CARD.svg")
back_card = pygame.transform.scale(back_card, (100, 150))

# Load card svg's from directory

card_images = {}
try:
    for filename in os.listdir(directory):
        if filename.endswith(".svg"):
            full_path = os.path.join(directory, filename)

            try:
                card_image = pygame.image.load(full_path)
                card_key = os.path.splitext(filename)[0]
                card_images[card_key] = card_image
            except pygame.error as e:
                print(f"Error loading {filename}: {e}")
except FileNotFoundError:
    print(f"Directory not found: {directory}")
except PermissionError:
    print(f"Permission denied to access {directory}")

# Top
card_positions_top = [(720, 30), (840, 30), (960, 30)]
# Middle
card_positions_middle = [(620, 270), (740, 270)]
# Bottom
card_positions_bottom = [(420, 515), (540, 515), (660, 515)]

if card_images:
    all_card_keys = list(card_images.keys())
    top_row = random.sample(all_card_keys, 3)

    remaining_cards = [card for card in all_card_keys if card not in top_row]

    bottom_row = random.sample(remaining_cards, 3)

else:
    card_keys = []

# Main
while ge.terminate_game() == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(casino_bg, (0, 0))

    for i, cards in enumerate(card_positions_top):
        card_image = pygame.transform.scale(
            card_images[top_row[i]], (100, 150)
        )  # Resize card
        screen.blit(card_image, cards)

    for i, cards in enumerate(card_positions_middle):
        if i == 0:
            placeholder_card = pygame.Surface((100, 150), pygame.SRCALPHA)
            pygame.draw.rect(
                placeholder_card, (0, 0, 0), placeholder_card.get_rect(), 3
            )  # Black border
            screen.blit(placeholder_card, cards)
        elif i == 1:
            screen.blit(back_card, cards)

    for i, cards in enumerate(card_positions_bottom):
        card_image = pygame.transform.scale(
            card_images[bottom_row[i]], (100, 150)
        )  # Resize card
        screen.blit(card_image, cards)

    pygame.display.update()

    clock.tick(60)

pygame.quit()

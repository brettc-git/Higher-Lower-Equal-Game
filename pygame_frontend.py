import pygame
import os
import random
import game_engine

pygame.init()
pygame.display.set_caption("Higher-Lower-Equal Card Game")
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

# Cursor
system = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_NO)
directory = "assets/Card SVG files/"

# Load bg image and resize
casino_bg = pygame.image.load("assets/Casino_bg.jpg")
casino_bg = pygame.transform.scale(casino_bg, (1280, 720))

# Load back card and resize
back_card = pygame.image.load("assets/BACK.png")
back_card = pygame.transform.scale(back_card, (100, 150))

# Load card svg's from directory
card_images = {}
try:
    for filename in os.listdir(directory):
        if filename.endswith('.svg'):
            full_path = os.path.join(directory, filename)

            try:
                card_image = pygame.image.load(full_path)
                card_key = os.path.splitext(filename)[0]
                card_images[card_key] = card_image
            except pygame.error as e:
                print(f"Error loading {filename}: {e}")
except FileNotFoundError:
    print(f"Directory not found: {directory}")

if card_images:
    all_card_keys = list(card_images.keys())
    top_row = random.sample(all_card_keys, 3)

    remaining_cards = [card for card in all_card_keys if card not in top_row]

    bottom_row = random.sample(remaining_cards, 3)

else:
    card_keys = []

# Top
card_positions_top = [(720, 30), (840, 30), (960, 30)]
# Middle
card_positions_middle = [(620, 270), (740, 270)]
# Bottom
card_positions_bottom = [(420, 515), (540, 515), (660, 515)]

pygame.font.init()

title_font = pygame.font.Font(None, 48)
score_font = pygame.font.Font(None, 45)

ge = game_engine.GameEngine()
ex = game_engine.Expectimax()
na = game_engine.NaiveBayes()

# Scores inhereted from GameEngine
player_score = ge.player.score
cpu_score = ge.cpu.score

players_hand = ge.sample_deck.deal(3)
cpu_hand = ge.sample_deck.deal(3)

remaining_cards = ge.sample_deck.size

ge.sample_deck.shuffle()

# Buttons
button = pygame.font.Font(None, 24)

button_width = 120
button_height = 50
button_color = (250, 0, 0)
text_color = (255, 255, 255)

button_texts = [
    "Higher",
    "Lower",
    "Equal",
    "Naive Bayes",
    "Expectimax"
]

# Button positions
button_positions = [
    (1050, 450),   # Higher
    (1050, 525),   # Lower
    (1050, 600),   # Equal
    (120, 500),   # Naive Bayes
    (250, 500)    # Expectimax
]

# Expectimax Panel
panel_width = 600
panel_height = 400
panel_color = (130,130,130)
panel_text_color = (255,255,255)

# def draw_expectimax():
#     panel_surface = pygame.Surface((panel_width, panel_height))
#     panel_surface.fill(panel_color)

#     expectimax_result = ge.expectimax()

#     expectimax_text = title_font.render(f"Expectimax Result: {expectimax_result}", True, panel_text_color)
#     expectimax_text_rect = expectimax_text.get_rect(center=(panel_width // 2, panel_height // 2))

#     panel_surface.blit(expectimax_text, expectimax_text_rect)

#     screen.blit(panel_surface, (340, 100))

# Button/Card Functions

# The three cards act as buttons
def pick_card():
    position = pygame.mouse.get_pos()

    # Card 1
    if 420 <= position[0] <= 520 and 515 <= position[1] <= 665:
        if pygame.mouse.get_pressed()[0]:
            # Highlights the card, same for other functions and buttons
            pygame.draw.rect(screen, (255, 0, 0), (420, 515, 100, 150), 3)
            return players_hand[0]

    # Card 2
    elif 540 <= position[0] <= 640 and 515 <= position[1] <= 665:
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, (255, 0, 0), (540, 515, 100, 150), 3)
            return players_hand[1]

    # Card 3
    elif 660 <= position[0] <= 760 and 515 <= position[1] <= 665:
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, (255, 0, 0), (660, 515, 100, 150), 3)
            return players_hand[2]

def on_higher():
    position = pygame.mouse.get_pos()

    if 1050 <= position[0] <= 1170 and 450 <= position[1] <= 500:
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, (0, 0, 255), (1050, 450, button_width, button_height), 3)
            pass

def on_lower():
    position = pygame.mouse.get_pos()

    if 1050 <= position[0] <= 1170 and 525 <= position[1] <= 575:
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, (0, 0, 255), (1050, 525, button_width, button_height), 3)
            pass

def on_equal():
    position = pygame.mouse.get_pos()

    if 1050 <= position[0] <= 1170 and 600 <= position[1] <= 650:
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, (0, 0, 255), (1050, 600, button_width, button_height), 3)
            pass

def on_expectimax():
    position = pygame.mouse.get_pos()

    if 250 <= position[0] <= 370 and 500 <= position[1] <= 550:
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, (0, 0, 255), (250, 500, button_width, button_height), 3)
            # Create a small gray window that shows the expectimax's decision
            panel_surface = pygame.Surface((600,400))
            panel_surface.fill((130,130,130))

            # expectimax_result = ge.expectimax(active_card, next_card)
            # result_text = title_font.render(f"Expectimax EV: {expectimax_result.n}", True, (255,255,255))

            screen.blit(panel_surface, (340, 100))

            pass

def on_naive_bayes():
    position = pygame.mouse.get_pos()

    if 120 <= position[0] <= 240 and 500 <= position[1] <= 550:
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, (0, 0, 255), (120, 500, button_width, button_height), 3)
            
            panel_surface = pygame.Surface((600,400))
            panel_surface.fill((130,130,130))
            pass




# Game over is initially false
game_over = False

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if ge.terminate_game():
        if game_over == True:
            winner_text = "You win!" if ge.player.score >= 50 else "CPU wins!"
    ## SETTING UP THE CARD GAME GUI


    # Background
    screen.blit(casino_bg, (0, 0))



    # Card Positions [Top]
    for i, cards in enumerate(card_positions_top):
        card_image = pygame.transform.scale(card_images[top_row[i]], (100, 150))
        screen.blit(card_image, cards)

    # Card Positions [Mid]
    for i, cards in enumerate(card_positions_middle):
        if i == 0:
            placeholder_card = pygame.Surface((100, 150), pygame.SRCALPHA)
            pygame.draw.rect(placeholder_card, (0, 0, 0), placeholder_card.get_rect(), 3)
            screen.blit(placeholder_card, cards)
        elif i == 1:
            screen.blit(back_card, cards)

    # Card Positions [Bottom]
    for i, cards in enumerate(card_positions_bottom):
        card_image = pygame.transform.scale(card_images[bottom_row[i]], (100, 150))
        screen.blit(card_image, cards)

    # Player
    player_text = title_font.render("Player", True, (255, 255, 255))
    player_text_rect = player_text.get_rect(center=(860, 530))
    screen.blit(player_text, player_text_rect)

    # CPU
    cpu_text = title_font.render("CPU", True, (255, 255, 255))
    cpu_text_rect = cpu_text.get_rect(center=(620, 50))
    screen.blit(cpu_text, cpu_text_rect)

    # Player score
    player_score_text = score_font.render(f" {player_score}", True, (255, 255, 255))
    player_score_rect = player_score_text.get_rect(center=(860, 580))
    screen.blit(player_score_text, player_score_rect)

    # CPU score
    cpu_score_text = score_font.render(f" {cpu_score}", True, (255, 255, 255))
    cpu_score_rect = cpu_score_text.get_rect(center=(620, 100))
    screen.blit(cpu_score_text, cpu_score_rect)


    def draw_buttons():
        for i, (text, switch) in enumerate(zip(button_texts, button_positions)):
            button_surface = pygame.Surface((button_width, button_height))
            button_surface.fill(button_color)

            text_surface = button.render(text, True, text_color)
            text_box = text_surface.get_rect(center=(button_width // 2, button_height // 2))

            button_surface.blit(text_surface, text_box)

            screen.blit(button_surface, switch)

    draw_buttons()


    # Player chooses their card
    active_card = pick_card()

    # Retrieve next card
    next_card = ge.sample_deck.deal(1)

    # Guess Options
    if on_higher(): # On pressing higher
        ge.score_system(active_card, next_card, "Higher",player_type="player")
    elif on_lower(): # On pressing lower
        ge.score_system(active_card, next_card, "Lower",player_type="player")
    elif on_equal(): # On pressing equal
        ge.score_system(active_card, next_card, "Equal",player_type="player")
    elif on_expectimax():
        pass
    elif on_naive_bayes():
        pass

    # Update player's score
    player_score = ge.player.score
    # Decrement card for player
    remaining_cards -= 1

    # Update CPU's score
    cpu_score = ge.cpu.score

    # Decrement card again for CPU
    remaining_cards -= 1

    pygame.display.update()

    clock.tick(60)

pygame.quit()

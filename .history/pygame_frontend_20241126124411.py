import pygame
import os


pygame.init()
pygame.display.set_caption("Higher-Lower-Equal Card Game")
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

system = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_NO)

directory = "assets/Card SVG files/"

# Load card svg's from directory


wood_bg = pygame.image.load("assets/wood_bg.jpeg")

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ### Create a card interface
    ### SET wood_bg as background

    clock.tick(60)
pygame.quit()

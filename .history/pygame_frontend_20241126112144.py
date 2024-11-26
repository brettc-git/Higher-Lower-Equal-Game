import pygame
import os


pygame.init()
pygame.display.set_caption("Higher-Lower-Equal Card Game")
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

directory = "/assets/Card SVG files/"

wood_bg = pygame.image.load("assets/wood_bg.jpeg")

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ### Create a card interface
    ### SET wood_bg as background

    screen.blit(wood_bg, (0, 0))
    clock.tick(60)
pygame.quit()

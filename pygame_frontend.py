import pygame

pygame.init()
pygame.display.set_caption("Higher-Lower-Equal Card Game")
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
running = True

wood_bg = pygame.image.load("wood_bg.jpg")

while running:

    ### Create a card interface
    ### SET wood_bg as background
    ### 
    clock.tick(60)
pygame.quit()

import pygame
import sys


def main():
    pygame.init()
    pygame.display.set_caption("The Polish Hammer")
    screen = pygame.display.set_mode((1000, 700))

    while True:
        for event in pygame.event.get():
            print(event)  # Used for an example here
            if event.type == pygame.QUIT:
                sys.exit()
            # Additional interactions

        # Draw things on the screen

        pygame.display.update()


main()
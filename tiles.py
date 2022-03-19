import pygame
import os, sys
from slide_puzzle import SlidePuzzle

def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Slide Puzzle")
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle((3,3), 150, 5)
    
    while True:
        dt = fpsclock.tick()/1000
        
        screen.fill((1,1,1))
        
        program.draw(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
                
        program.update(dt)

if __name__ == '__main__':
    main()
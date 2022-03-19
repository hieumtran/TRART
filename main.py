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
    
    BackGround = Background('bg.png', [0,0])
    
    
    while True:
        dt = fpsclock.tick()/1000
        
        screen.fill((1,1,1)) # Filling with missing pictures
        screen.fill([255, 255, 255])
        # screen.blit(BackGround.image, BackGround.rect)

        
        
        program.draw(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                
        program.update(dt)

if __name__ == '__main__':
    main()
import pygame
import os, sys
from slide_puzzle import SlidePuzzle
from menu import menuUI


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Slide Puzzle")
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    fpsclock = pygame.time.Clock()
    
    w_screen, h_screen = pygame.display.get_surface().get_size() 
    
    program = SlidePuzzle((3,3), 160, 5, w_screen, h_screen)
    program1 = SlidePuzzle((4,4), 140, 5, w_screen, h_screen)
    program2 = SlidePuzzle((5,5), 100, 5, w_screen, h_screen)
    menu_ui = menuUI('./ui_button/DeSwipe.png', './ui_button/start.png', './ui_button/quit.png',
                     ['./ui_button/3x3.png', './ui_button/4x4.png', './ui_button/5x5.png'], './ui_button/back.png', w_screen, h_screen)
    
    # Condition of ui
    cond = 0
    prev_cond = 0
    pos = w_screen, h_screen
    while True:
        dt = fpsclock.tick()/1000
        
        # screen.fill((1,1,1)) # Filling with missing pictures
        screen.fill([255, 255, 255])
        
        if cond < 2:
            cond = menu_ui.draw(screen, cond, pos)
            if prev_cond != cond:
                pos = w_screen, h_screen
                prev_cond == cond
        elif cond >= 2:
            program.draw(screen)
            cond = program.update(pos, cond)
            # elif cond == 2.5:
            #     program = SlidePuzzle((3,3), 160, 5, w_screen, h_screen)
            #     program.draw(screen)
            #     cond -= 0.5
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_r:
                    program = SlidePuzzle((3,3), 160, 5, w_screen, h_screen)
        
        if cond == -1:
            sys.exit()
                

if __name__ == '__main__':
    main()
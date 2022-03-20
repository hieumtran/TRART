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
    
    ui = True
    program = SlidePuzzle((3,3), 160, 5, w_screen, h_screen)
    menu_ui = menuUI('./ui_button/DeSwipe.png', './ui_button/start.png', './ui_button/quit.png',
                     ['./ui_button/3x3.png', './ui_button/4x4.png', './ui_button/5x5.png'], './ui_button/back.png', w_screen, h_screen)
    
    # Condition of ui
    cond = 0
    prev_cond = 0
    pos = 0, 0
    while True:
        dt = fpsclock.tick()/1000
        
        # screen.fill((1,1,1)) # Filling with missing pictures
        screen.fill([255, 255, 255])
        
        if cond < 2:
            cond = menu_ui.draw(screen, cond, pos)
            if prev_cond != cond:
                pos = 0, 0
                prev_cond == cond
        elif cond >= 2:
            program.draw(screen, fpsclock)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
        
        if cond == -1:
            sys.exit()
                
        program.update(dt)

if __name__ == '__main__':
    main()
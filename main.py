import pygame
import os, sys
from slide_puzzle import SlidePuzzle
from menu import menuUI

import tkinter as tk

os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = "center"
    pygame.display.set_caption("Slide Puzzle")
    
    root = tk.Tk()

    (w_screen, h_screen) = (root.winfo_screenwidth(), root.winfo_screenheight())

    screen = pygame.display.set_mode((w_screen, h_screen))
    
    # w_screen, h_screen = pygame.display.get_surface().get_size() 
    
    program_3x3 = SlidePuzzle((3,3), 160, 5, w_screen, h_screen)
    program_4x4 = SlidePuzzle((4,4), 130, 5, w_screen, h_screen)
    program_5x5 = SlidePuzzle((5,5), 100, 5, w_screen, h_screen)
    menu_ui = menuUI('./ui_button/DeSwipe.png', './ui_button/start.png', './ui_button/quit.png',
                     ['./ui_button/3x3.png', './ui_button/4x4.png', './ui_button/5x5.png'], './ui_button/back.png', w_screen, h_screen)
    
    # Condition of ui
    cond = 0
    prev_cond = 0
    pos = w_screen, h_screen
    win_cnt = 0
    while True:
        # screen.fill((1,1,1)) # Filling with missing pictures
        screen.fill([255, 255, 255])
        
        if cond < 2:
            cond = menu_ui.draw(screen, cond, pos)
            if prev_cond != cond:
                pos = w_screen, h_screen
                prev_cond == cond
        elif cond >= 2:
            if cond == 2:
                program_3x3.draw(screen, win_cnt)
                cond, win_cnt = program_3x3.update(pos, cond, win_cnt)
            elif cond == 3:
                program_4x4.draw(screen, win_cnt)
                cond, win_cnt = program_4x4.update(pos, cond, win_cnt)
            elif cond == 4:
                program_5x5.draw(screen, win_cnt)
                cond, win_cnt = program_5x5.update(pos, cond, win_cnt)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
        
        if cond == -1:
            sys.exit()
                

if __name__ == '__main__':
    main()
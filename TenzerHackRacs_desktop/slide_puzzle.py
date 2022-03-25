import pygame, os
from random import shuffle, choice
import copy
import time
import glob


# gs - grid size
# ts - tile size
# ms - margin size

class SlidePuzzle:
    def __init__(self, gs, ts, ms, w_screen, h_screen):
        # Initialize parameters
        self.gs, self.ts, self.ms = gs, ts, ms
        self.tiles_len = (gs[0]*gs[1]) - 1
        self.tiles = [(x,y) for x in range(gs[0]) for y in range(gs[1])]
        self.tilesOG = [(x,y) for x in range(gs[0]) for y in range(gs[1])]   
        self.tilespos = {(x,y):(x*(ts+ms)+ms,y*(ts+ms)+ms) for y in range(gs[1]) for x in range(gs[0])}   
        self.font = pygame.font.Font(None, 120)    
        self.w, self.h = gs[0]*(ts+ms)+ms, gs[1]*(ts+ms)+ms
        
        # Windows screen 
        self.w_screen = w_screen
        self.h_screen = h_screen
        
        # Scaling factor
        self.w_adjust = (w_screen - self.ts*self.gs[0] - self.ms*(self.gs[0] - 1)) / 2
        self.h_adjust = (h_screen - self.ts*self.gs[1] - self.ms*(self.gs[1] - 1)) / 2
        
        # Picture loader
        picture = choice(glob.glob('./data/building/*.jpg'))
        self.pic = pygame.image.load(picture)
        self.pic = pygame.transform.scale(self.pic, (self.w, self.h))
        
        # Facts loader
        fact = open('./data/building/'+picture.split('\\')[1].replace('jpg', 'txt'), 'r')
        self.text = fact.read().split('\n')
        font = pygame.font.Font('./font/Roboto-Bold.ttf', 46)
        self.display_name = font.render(self.text[0], False, (0, 0, 0), (255, 255, 255))
        self.display_year = font.render('Construction finished in ' + self.text[1], False, (0, 0, 0), (255, 255, 255))
        
        # Button
        self.back_button = pygame.image.load('./ui_button/back_button.png')
        self.back_button = pygame.transform.scale(self.back_button, (self.w/4, self.h/4))
        self.retry = pygame.image.load('./ui_button/retry.png')
        self.retry = pygame.transform.scale(self.retry, (self.w/4, self.h/4))
        
        # Game condition
        self.finish = 0
        
        # Total move
        self.total_move = 0
        
        self.images = []
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            image = self.pic.subsurface(x,y,ts,ts)
            self.images += [image] 
            
        self.temp = self.tiles[:-1]
        self.origin = copy.deepcopy(self.temp)
        shuffle(self.temp)
        self.temp.insert(len(self.temp), self.tiles[-1])
        self.tiles = self.temp
        

    def getBlank(self): return self.tiles[-1]
    def setBlank(self, pos): self.tiles[-1] = pos
    
    opentile = property(getBlank, setBlank)
    
    def switch(self, tile):
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile, self.tiles[n]
        if self.tiles == self.tilesOG:
            self.finish = 1
    
    def is_grid(self, tile): 
        return tile[0] >= 0 and tile[0] < self.gs[0] and tile[1] >= 0 and tile[1] < self.gs[1]
    
    def adjacent(self):
        x,y = self.opentile
        return (x-1, y), (x+1,y), (x,y-1), (x,y+1)
    
    def update(self, pos, cond):
        """
        # Find the tile mouse is on
        # Switch as long as open tile is adjacent
        """
        
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        
        # Convert mouse position relative to tile position and check in grid
        if mouse[0]:
            tile = (mpos[0] - self.w_adjust)//self.ts , (mpos[1] - self.h_adjust)//self.ts
            if self.is_grid(tile) and self.finish == 0: 
                if tile in self.adjacent():
                    self.switch(tile)
                    sound = pygame.mixer.Sound("./sounds/click.mp3")
                    pygame.mixer.Sound.play(sound)
                    self.total_move += 1
                    
            if self.back_button_rect.collidepoint(pos):
                cond = 0
            elif self.retry_rect.collidepoint(pos):
                self.__init__(self.gs, self.ts, self.ms, self.w_screen, self.h_screen)
            else: self.finish = 0
        return cond

    def draw(self, screen):
        init_w, init_h = self.tilespos[(0, 0)][0] + self.w_adjust, self.tilespos[(0, 0)][1] + self.h_adjust
        init_w_size, init_h_size = self.ts*self.gs[0] + self.ms*(self.gs[0] - 1), self.ts*self.gs[1] + self.ms*(self.gs[1] - 1)
        
        # Blocks
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(init_w-self.ms*2, init_h-self.ms*2, init_w_size+self.ms*4, init_h_size+self.ms*4))
        pygame.draw.rect(screen, (251, 205, 5), pygame.Rect(init_w, init_h, init_w_size, init_h_size))
        
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            screen.blit(self.images[i], (x+self.w_adjust,y+self.h_adjust))
        
        # Goals
        goal_w, goal_h = self.w / 2, self.h / 2
        goal_init_w, goal_init_h = (init_w - goal_w)/2, init_h +  (init_h_size - goal_h)/2 
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(goal_init_w-self.ms*2, goal_init_h-self.ms*2, goal_w+self.ms*4, goal_h+self.ms*4))
        screen.blit(pygame.transform.scale(self.pic, (goal_w, goal_h)), (goal_init_w, goal_init_h))
        
        # Buttons
        self.back_button_rect = self.back_button.get_rect(x=0,y=self.h_screen-self.back_button.get_height())
        screen.blit(self.back_button, self.back_button_rect)
        self.retry_rect = self.retry.get_rect(x=self.w_screen-self.retry.get_width(),y=self.h_screen-self.back_button.get_height())
        screen.blit(self.retry, self.retry_rect)
        
        # Name & Year
        self.display_name_rect = self.display_name.get_rect(center=(self.w_screen/2, self.display_name.get_height()))
        self.display_year_rect = self.display_year.get_rect(center=(self.w_screen/2, self.display_name.get_height()+self.display_year.get_height()))
        screen.blit(self.display_name, self.display_name_rect)
        screen.blit(self.display_year, self.display_year_rect)
        
        # Fact
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.retry.get_width(), self.h_screen-self.retry.get_height(), 
                                                              self.w_screen-self.retry.get_width()-self.retry.get_width(), self.retry.get_height()))
        self.blit_text(screen, self.text[2], (self.retry.get_width(), self.h_screen-self.retry.get_height()), pygame.font.Font('./font/Roboto-Light.ttf', 24))
        
        # Total number of moves
        font = pygame.font.Font('./font/Roboto-Bold.ttf', 30)
        total_num = font.render('Total number of moves ' + str(self.total_move), 0, (0, 0, 0))
        total_num_w_pos = self.w_screen-((self.w_screen-(init_w_size+self.ms*4))/4)
        total_num_rect = total_num.get_rect(center=(total_num_w_pos, goal_init_h))
        screen.blit(total_num, total_num_rect)
    

        # Winning condition
        if self.finish == 1:
            congrat = pygame.image.load('./ui_button/congrat.png')
            congrat = pygame.transform.scale(congrat, (1829*0.95, 430*0.95))
            # pygame.draw.rect(screen, (0, 0, 0, 0.2), pygame.Rect(0, 0, self.w_screen, self.h_screen))
            s = pygame.Surface((self.w_screen, self.h_screen))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill((255,255,255))           # this fills the entire surface
            screen.blit(s, (0,0)) 
            screen.blit(congrat, (0, (self.h_screen-congrat.get_size()[1])/2))
    
    def blit_text(self, surface, text, text_pos, font):
        words = text.split(' ') # 2D array where each row is a list of words.
        x, y = text_pos
        line = ''
        for i in range(len(words)):
            line += ' ' + words[i]
            word_surface = font.render(line, 0, (0, 0, 0))

            if x+word_surface.get_width() >= (self.w_screen - self.retry.get_width() - self.back_button.get_width()) or i == len(words)-1:
                word_rect = word_surface.get_rect(x=x, y=y)
                surface.blit(word_surface, word_rect)
                y += word_surface.get_height()
                line = ''
        
            # for word in line:
            #     word_surface = font.render(word, 0, (0, 0, 0))
            #     word_width, word_height = word_surface.get_size()
            #     if x + word_width >= max_width:
            #         x = text_pos[0]  # Reset the x.
            #         y += word_height  # Start on new row.
            #     # word_rect = word_surface.get_rect(center=(x, y))
            #     surface.blit(word_surface, word_rect)
            #     x += word_width + space
            # x = text_pos[0]  # Reset the x.
            # y += word_height  # Start on new row.
                    
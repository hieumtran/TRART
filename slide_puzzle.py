# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 18:44:06 2019
@author: Manish
"""

import pygame, sys, os
from random import shuffle
import copy


# gs - grid size
# ts - tile size
# ms - margin size

class SlidePuzzle:
    def __init__(self, gs, ts, ms):
        self.gs, self.ts, self.ms = gs, ts, ms
        self.tiles_len = (gs[0]*gs[1]) - 1
        self.tiles = [(x,y) for x in range(gs[0]) for y in range(gs[1])]
        self.tilesOG = [(x,y) for x in range(gs[0]) for y in range(gs[1])]   
        self.tilespos = {(x,y):(x*(ts+ms)+ms,y*(ts+ms)+ms) for y in range(gs[1]) for x in range(gs[0])}   
        self.font = pygame.font.Font(None, 120)    
        self.w, self.h = gs[0]*(ts+ms)+ms, gs[1]*(ts+ms)+ms
        self.pic = pygame.image.load('./building/peeler.jpg')
        self.pic = pygame.transform.scale(self.pic, (self.w, self.h))
        
        # Scaling factor
        w_screen, h_screen = pygame.display.get_surface().get_size() 
        self.w_adjust = (w_screen - self.ts*self.gs[0] - self.ms*(self.gs[0] - 1)) / 2
        self.h_adjust = (h_screen - self.ts*self.gs[1] - self.ms*(self.gs[1] - 1)) / 2
        
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
            print("COMPLETE")
    
    def is_grid(self, tile): 
        return tile[0] >= 0 and tile[0] < self.gs[0] and tile[1] >= 0 and tile[1] < self.gs[1]
    
    def adjacent(self):
        x,y = self.opentile
        return (x-1, y), (x+1,y), (x,y-1), (x,y+1)
    
    def update(self, dt):
        """
        # Find the tile mouse is on
        # Switch as long as open tile is adjacent
        """
        
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        
        # Convert mouse position relative to tile position and check in grid
        if mouse[0]:
            tile = (mpos[0] - self.w_adjust)//self.ts , (mpos[1] - self.h_adjust)//self.ts
            if self.is_grid(tile): 
                if tile in self.adjacent():
                    self.switch(tile)
    
    def draw(self, screen):
        init_w, init_h = self.tilespos[(0, 0)][0] + self.w_adjust, self.tilespos[(0, 0)][1] + self.h_adjust
        init_w_size, init_h_size = self.ts*self.gs[0] + self.ms*(self.gs[0] - 1), self.ts*self.gs[1] + self.ms*(self.gs[1] - 1)
        
        # Place holder for images
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(init_w-self.ms*2, init_h-self.ms*2, init_w_size+self.ms*4, init_h_size+self.ms*4))
        pygame.draw.rect(screen, (251, 205, 5), pygame.Rect(init_w, init_h, init_w_size, init_h_size))
        
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            screen.blit(self.images[i], (x+self.w_adjust,y+self.h_adjust))
        
        # Place holder for goals
        # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((init_w / 4)*0.9, (init_h + init_h_size/4)*0.95,, init_h_si))
        goal_w, goal_h = self.w / 2, self.h / 2
        goal_init_w, goal_init_h = (init_w - goal_w)/2, init_h +  (init_h_size - goal_h)/2 
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(goal_init_w-self.ms*2, goal_init_h-self.ms*2, goal_w+self.ms*4, goal_h+self.ms*4))
        screen.blit(pygame.transform.scale(self.pic, (goal_w, goal_h)), (goal_init_w, goal_init_h))
            
        
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 18:44:06 2019
@author: Manish
"""

import pygame, sys, os
from random import shuffle


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
        w,h = gs[0]*(ts+ms)+ms, gs[1]*(ts+ms)+ms
        
        pic = pygame.image.load('./building/gcpa.jpg')
        pic = pygame.transform.scale(pic, (w,h))
        
        self.images = []
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            image = pic.subsurface(x,y,ts,ts)
            self.images += [image] 
            
        self.temp = self.tiles[:-1]
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
            tile = mpos[0]//self.ts, mpos[1]//self.ts
            
            if self.is_grid(tile): 
                if tile in self.adjacent():
                    self.switch(tile)
    
    def draw(self, screen):
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            screen.blit(self.images[i], (x,y))            
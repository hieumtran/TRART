import pygame

class menuUI:
    def __init__(self, title, start, quit, diff, back, w_screen, h_screen):
        self.title = pygame.image.load(title)
        self.start = pygame.image.load(start)
        self.quit = pygame.image.load(quit)
        self.diff = [pygame.image.load(i) for i in diff] 
        self.back = pygame.image.load(back)
        
        self.title = self.transform(self.title, 0.8)
        self.start = self.transform(self.start, 0.5)
        self.quit = self.transform(self.quit, 0.5)
        self.back = self.transform(self.back, 0.5)
        
        for i in range(len(self.diff)):
            self.diff[i] = self.transform(self.diff[i], 0.3)
        
        self.w_screen = w_screen
        self.h_screen = h_screen
    
    def transform(self, img, factor):
        return pygame.transform.scale(img, (img.get_width()*factor, img.get_height()*factor))
    
    def draw(self, screen, cond, pos):
        diff_rects = []

        if cond == 0:
            title_rect = self.title.get_rect(center=(self.w_screen/2, self.title.get_height()))
            screen.blit(self.title, title_rect)
            
            start_rect = self.start.get_rect(center=(self.w_screen/2, self.title.get_height()+self.start.get_height()*2.5))
            screen.blit(self.start, start_rect)
            
            quit_rect = self.quit.get_rect(center=(self.w_screen/2, 
                                                    self.title.get_height()+self.start.get_height()*2.5+self.quit.get_height()*1.5))
            screen.blit(self.quit, quit_rect)
        
        if cond == 1:
            title_rect = self.title.get_rect(center=(self.w_screen/2, self.title.get_height()))
            screen.blit(self.title, title_rect)
            
            up_height = self.title.get_height()
            for i in range(len(self.diff)):
                up_height += self.diff[i].get_height()*2
                diff_rect = self.diff[i].get_rect(center=(self.w_screen/2, up_height))
                screen.blit(self.diff[i], diff_rect)
                diff_rects.append(diff_rect)
            
            back_rect = self.back.get_rect(center=(self.w_screen/2, up_height+self.back.get_height()*1.5))
            screen.blit(self.back, back_rect)
        
        if cond == 0:
            if start_rect.collidepoint(pos):
                cond = 1
            if quit_rect.collidepoint(pos):
                cond = -1
        elif cond == 1:
            for i in range(len(diff_rects)):
                if diff_rects[i].collidepoint(pos):
                    cond += 1+i
            if back_rect.collidepoint(pos):
                cond = 0
        
        return cond
                
            
        
        
        
import pygame

def write(text, screen, font, x, y, color="Coral",):
    text = font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(center=(500 // 2, y))
    screen.blit(text, text_rect)
    return text

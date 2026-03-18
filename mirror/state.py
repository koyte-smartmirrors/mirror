import pygame
from datetime import datetime


class MirrorState:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 64)
        self.time_text = ""

    def update(self):
        self.time_text = datetime.now().strftime("%H:%M:%S")

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.render(self.time_text, True, (255, 255, 255))
        rect = text.get_rect(center=(240, 160))
        screen.blit(text, rect)

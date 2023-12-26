import pygame
import config
from player import Player


class NPC:
    def __init__(self, x_position, y_position, image_path):
        print("NPC Criado")
        self.position = [x_position, y_position]
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE,
                                config.SCALE, config.SCALE)

    def update(self):
        print("Atualizado")

    def update_position(self, new_position):
        self.position[0] = new_position[0]
        self.position[1] = new_position[1]
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)

    def render(self, screen, camera):
        self.rect = pygame.Rect(self.position[0] * config.SCALE - camera[0] * config.SCALE,
                                self.position[1] * config.SCALE - camera[1] * config.SCALE,
                                config.SCALE, config.SCALE)
        screen.blit(self.image, self.rect)

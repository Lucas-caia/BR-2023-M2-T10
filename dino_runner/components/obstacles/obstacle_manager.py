import pygame
import random

from dino_runner.components.obstacles.large_cactus import LargeCactus
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            obstacle_type = random.choice(["cactus", "large_cactus", "bird"])
            if obstacle_type == "cactus":
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif obstacle_type == "large_cactus":
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            elif obstacle_type == "bird":
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break               

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
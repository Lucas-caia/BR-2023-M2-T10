import random

from dino_runner.utils.constants import SCREEN_WIDTH

class Bird:
    def __init__(self, images):
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(210, 305)
        self.animation_time = 5
        self.current_time = 0

    def update(self, game_speed, obstacles):
        self.current_time += 1
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.image_index = 0
            self.image = self.images[self.image_index]

        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

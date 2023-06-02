from dino_runner.utils.constants import SHIELD, SHIELD_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Shield(PowerUp):
    def __init__(self):
        self.image = SHIELD
        self.type = SHIELD_TYPE
        super().__init__(self.image, self.type)

    def apply_power_up(self, player):
        player.has_power_up = True
        player.power_up_time = pygame.time.get_ticks() + 2000
        player.type = self.type

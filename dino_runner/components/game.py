import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, RESTART
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = "freesansbold.ttf"

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        self.playing = False
        self.game_speed = 20
        self.initial_game_speed = 20
        self.game_speed = self.initial_game_speed
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.death_count = 0
        self.highscore = 0

        self.player = Dinosaur()
        self.selected_dinosaur = None
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def reset_score(self):
        self.score = 0
        self.game_speed = self.initial_game_speed

    def run(self):
        # Game loop: events - update - draw
        self.reset_score()
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.obstacle_manager.reset_obstacles()
        while self.running:
            self.events()
            if self.playing:
                self.update()
                self.draw()
            else:
                self.show_menu()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.power_up_manager.update(self)
        self.player.update(user_input)

        if self.score > self.highscore:
            self.highscore = self.score
            
        self.obstacle_manager.update(self)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

        if self.player.is_dead and not self.playing:
            self.handle_death()
            
    def handle_death(self):
        self.death_count += 1
        self.reset_score()
        self.player.is_dead = False
        self.playing = False
        
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_text(f"Score: {self.score}", (1000, 50))
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        self.draw_text(f"Highscore: {self.highscore}", (1000, 80))
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_text(self, text, pos):
        font = pygame.font.Font(FONT_STYLE, 22)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        self.screen.blit(text_surface, text_rect)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.draw_text(
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",
                    (500, 40),
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_death()
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.draw_text("Press any key to start", (half_screen_width, half_screen_height))
            self.screen.blit(ICON, (half_screen_width - 50, half_screen_height - 130))
        else:
            reset_image_rect = RESTART.get_rect()
            reset_image_rect.center = (half_screen_width, half_screen_height + 50)
            self.screen.blit(RESTART, (half_screen_width - 40, half_screen_height - 110))
            self.draw_text("Press any key to restart", (half_screen_width, half_screen_height))
            self.draw_text(f"Deaths: {self.death_count}", (half_screen_width, half_screen_height + 30))
            self.draw_text(f"Highscore: {self.highscore}", (half_screen_width, half_screen_height + 60))

        pygame.display.flip()
        self.handle_events_on_menu()

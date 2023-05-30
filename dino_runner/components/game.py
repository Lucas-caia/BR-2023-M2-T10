import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        
        self.player = Dinosaur()
        self.selected_dinosaur = None

    def run(self):
        self.show_start_screen()
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)

    def show_start_screen(self):
        start_font = pygame.font.Font(None, 40)
        start_text = start_font.render("Press any key to start", True, (0, 0, 0))
        start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    running = False

            self.screen.fill((255, 255, 255))
            self.screen.blit(ICON, (SCREEN_WIDTH // 2 - ICON.get_width() // 2, SCREEN_HEIGHT // 2 - ICON.get_height() // 2 - 70))
            self.screen.blit(start_text, start_text_rect)
            pygame.display.update()
            self.clock.tick(FPS)
    


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
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

  #  def dinosaur_selection_screen(self):
  #      selected = False
  #      while not selected:
  #          for event in pygame.event.get():
  #              if event.type == pygame.QUIT:
  #                  pygame.quit()

  #  def start_game(self):
  #      self.dinosaur_selection_screen()
  #      if self.selected_dinosaur == "default":
  #          self.player = Dinosaur()
   #     elif self.selected_dinosaur == "alternative":
  #          self.player = AlternativeDinosaur()

  #      self.run()

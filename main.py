import pygame
import sys
import random


class Scene:
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


class TitleScreen(Scene):
    def __init__(self):
        self.floor_x_pos = 0
        self.game_over_rect = game_over_surface.get_rect(center=(288, 512))

    def render(self):
        screen.blit(bg_surface, (0, 0))
        screen.blit(game_over_surface, self.game_over_rect)

    def update(self):
        self.floor_x_pos -= 1
        self.draw_floor()
        if self.floor_x_pos <= -576:
            self.floor_x_pos = 0

    def draw_floor(self):
        screen.blit(floor_surface, (self.floor_x_pos, 900))
        screen.blit(floor_surface, (self.floor_x_pos + 576, 900))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()


class SceneManager:
    def __init__(self):
        self.go_to(TitleScreen())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
pygame.display.set_caption("Flappy Bird")

screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.ttf", 40)

bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)

bird_downflap = pygame.transform.scale2x(
    pygame.image.load("assets/bluebird-downflap.png").convert_alpha()
)
bird_midflap = pygame.transform.scale2x(
    pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
)
bird_upflap = pygame.transform.scale2x(
    pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
)

pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)

game_over_surface = pygame.transform.scale2x(
    pygame.image.load("assets/message.png").convert_alpha()
)

flap_sound = pygame.mixer.Sound("sounds/sound_sfx_wing.wav")
death_sound = pygame.mixer.Sound("sounds/sound_sfx_hit.wav")
score_sound = pygame.mixer.Sound("sounds/sound_sfx_point.wav")

manager = SceneManager()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    manager.scene.handle_events(events)
    manager.scene.update()
    manager.scene.render()
    pygame.display.update()
    clock.tick(120)

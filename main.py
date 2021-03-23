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


class GameScene(Scene):
    def __init__(self):
        self.gravity = 0.33
        self.bird_movement = 0
        self.score = 0
        self.high_score = 0
        self.floor_x_pos = 0
        self.game_over = False

        self.bird_frames = [bird_downflap, bird_midflap, bird_upflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(100, 512))

        self.pipe_list = []
        self.pipe_height = [400, 600, 800]
        self.score_sound_countdown = 100

    def render(self):
        # Bird
        screen.blit(bg_surface, (0, 0))
        screen.blit(self.rotated_bird, self.bird_rect)

        # Pipes
        self.pipe_list = self.move_pipes(self.pipe_list)
        self.pipe_list = self.remove_pipes(self.pipe_list)
        self.draw_pipes(self.pipe_list)

        # Floor
        self.draw_floor()

    def update(self):
        self.bird_movement += self.gravity
        self.rotated_bird = self.rotate_bird(self.bird_surface)
        self.bird_rect.centery += self.bird_movement

        # Floor
        self.floor_x_pos -= 1
        if self.floor_x_pos <= -576:
            self.floor_x_pos = 0

        # Game Over state change
        self.game_over = self.check_collision(self.pipe_list)
        if self.game_over is True:
            manager.go_to(TitleScreen())

    def check_collision(self, pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                death_sound.play()
                return True

        if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 900:
            death_sound.play()
            return True

        return False

    def draw_floor(self):
        screen.blit(floor_surface, (self.floor_x_pos, 900))
        screen.blit(floor_surface, (self.floor_x_pos + 576, 900))

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
        top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
        return bottom_pipe, top_pipe

    def move_pipes(self, pipes):
        for pipe in pipes:
            pipe.centerx -= 5
        return pipes

    def draw_pipes(self, pipes):
        for pipe in pipes:
            if pipe.bottom >= 1024:
                screen.blit(pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)

    def remove_pipes(self, pipes):
        for pipe in pipes:
            if pipe.centerx == -600:
                pipes.remove(pipe)
        return pipes

    def rotate_bird(self, bird):
        new_bird = pygame.transform.rotozoom(bird, -self.bird_movement * 3, 1)
        return new_bird

    def animate_bird(self):
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=(100, self.bird_rect.centery))
        return new_bird, new_bird_rect

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird_movement = 0
                    self.bird_movement -= 12
                    flap_sound.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.bird_movement = 0
                self.bird_movement -= 12
                flap_sound.play()

            if event.type == SPAWNPIPE:
                self.pipe_list.extend(self.create_pipe())
            if event.type == BIRDFLAP:
                if self.bird_index < 2:
                    self.bird_index += 1
                else:
                    self.bird_index = 0
                self.bird_surface, self.bird_rect = self.animate_bird()


class TitleScreen(Scene):
    def __init__(self):
        self.game_over_rect = game_over_surface.get_rect(center=(288, 512))

    def render(self):
        screen.blit(bg_surface, (0, 0))
        screen.blit(game_over_surface, self.game_over_rect)

    def update(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                manager.go_to(GameScene())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    manager.go_to(GameScene())


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
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

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

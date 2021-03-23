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


class SceneManager:
    def __init__(self):
        pass

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self


def main():
    pass


if __name__ == "__main__":
    main()

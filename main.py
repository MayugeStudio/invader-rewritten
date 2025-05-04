import math
import pygame

DEFAULT_SCREEN_SIZE = (800, 800)
IMAGES_PATH = "./images/"
SOUNDS_PATH = "./sounds/"
FONTS_PATH  = "./fonts/"

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.quit = False

    def tick(self) -> float:
        return self.clock.tick(self.fps)/1000

class BaseScene:
    def draw(self, game: Game):
        pass

    def update(self, dt: float):
        pass

class MenuScene(BaseScene):
    def __init__(self, screen_size: tuple[int, int]):
        self.backgrounds = [pygame.image.load(IMAGES_PATH + f"background/background_1_{i+1}.png") for i in range(12)]
        for i in range(len(self.backgrounds)):
            self.backgrounds[i] = pygame.transform.scale(self.backgrounds[i], screen_size)
        self.background_index = 0

    def draw(self, game: Game):
        game.screen.blit(self.backgrounds[math.floor(self.background_index)])

    def update(self, dt: float):
        self.background_index += dt * 5
        if self.background_index > len(self.backgrounds):
            self.background_index = 0


def main():
    pygame.init()
    game = Game()
    scene: BaseScene = MenuScene(DEFAULT_SCREEN_SIZE)

    while not game.quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit = True

        dt = game.tick()

        scene.draw(game)
        scene.update(dt)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()


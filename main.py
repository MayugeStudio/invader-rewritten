import math
import pygame

DEFAULT_SCREEN_SIZE = (900, 600)
IMAGES_PATH = "./images/"
SOUNDS_PATH = "./sounds/"
FONTS_PATH  = "./fonts/"


class TransitionalColor:
    def __init__(self, initial_color: tuple[int, int, int], direction: tuple[int, int, int]) -> None:
        self.data = list(initial_color)
        self.direction = list(direction)
        self.speed = 4

    def transition(self) -> None:
        minimum = 50
        maximum = 240
        for i in range(3):
            self.data[i] += self.direction[i] * self.speed
            if self.data[i] <= minimum or self.data[i] >= maximum:
                self.direction[i] *= -1
            if self.data[i] < minimum:
                self.data[i] = minimum
            elif self.data[i] > maximum:
                self.data[i] = maximum


class Game:
    def __init__(self, screen_size: tuple[int, int]) -> None:
        self.screen = pygame.display.set_mode(screen_size)
        self.screen_size = screen_size
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.quit = False

    def tick(self) -> float:
        return self.clock.tick(self.fps)/1000


class BaseScene:
    def draw(self, game: Game) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def handle_input(self, game: Game, event: pygame.event.Event) -> None:
        pass


class MenuScene(BaseScene):
    def __init__(self, screen_size: tuple[int, int], font: pygame.Font) -> None:
        self.font = font
        self.backgrounds = [pygame.image.load(IMAGES_PATH + f"background/background_1_{i+1}.png") for i in range(12)]
        for i in range(len(self.backgrounds)):
            self.backgrounds[i] = pygame.transform.scale(self.backgrounds[i], screen_size)
        self.background_index = 0
        self.background_scroll_speed = 8

        # TODO delete masic numbers such as 150, 80
        # TODO factor out buttons into Button-class
        self.button_color = TransitionalColor((100, 245, 30), (1, 0, 0))

        # transparent background
        self.transparent_surface = pygame.Surface((400, 180))
        self.transparent_surface.set_alpha(200)
        self.transparent_surface_rect = self.transparent_surface.get_rect()
        self.transparent_surface_rect.x = screen_size[0]//2 - self.transparent_surface_rect.w//2
        self.transparent_surface_rect.y = screen_size[1] - self.transparent_surface_rect.h - 30

        self.start_button_text = "START"
        self.start_button = self.font.render(self.start_button_text, False, (255, 255, 255))

        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.x = screen_size[0]//2 - self.start_button.width//2
        self.start_button_rect.y = self.transparent_surface_rect.y + (self.transparent_surface_rect.h//4) - self.start_button_rect.h//2

        self.quit_button_text = "QUIT GAME"
        self.quit_button = self.font.render(self.quit_button_text, False, (255, 255, 255))

        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_button_rect.x = screen_size[0]//2 - self.quit_button.width//2
        self.quit_button_rect.y = self.transparent_surface_rect.y + (self.transparent_surface_rect.h*3//4) - self.quit_button_rect.h//2

        # options
        self.option_cursor = 0
        self.option_buttons = [self.start_button, self.quit_button]
        self.option_texts = [self.start_button_text, self.quit_button_text]
        self.option_rects = [self.start_button_rect, self.quit_button_rect]
        self.options_count = len(self.option_buttons)


    def draw(self, game: Game) -> None:
        game.screen.blit(self.backgrounds[self.background_index], (0, 0))
        self.transparent_surface.fill((50, 50, 50))
        game.screen.blit(self.transparent_surface, self.transparent_surface_rect)
        for index in range(self.options_count):
            game.screen.blit(self.option_buttons[index], (self.option_rects[index].x, self.option_rects[index].y))

    def update(self, dt: float) -> None:
        self.background_index += math.floor(dt * self.background_scroll_speed)
        if self.background_index > len(self.backgrounds):
            self.background_index = 0

        self.button_color.transition()
        text = self.option_texts[self.option_cursor]
        self.option_buttons[self.option_cursor] = self.font.render(text, False, self.button_color.data)


    def handle_input(self, game: Game, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            text = self.option_texts[self.option_cursor]
            if event.key == pygame.K_UP:
                self.option_buttons[self.option_cursor] = self.font.render(text, False, (255, 255, 255))
                self.option_cursor += 1
                self.option_cursor %= len(self.option_buttons)
            elif event.key == pygame.K_DOWN:
                self.option_buttons[self.option_cursor] = self.font.render(text, False, (255, 255, 255))
                self.option_cursor -= 1
                self.option_cursor %= len(self.option_buttons)
            elif event.key == pygame.K_SPACE:
                if self.option_cursor == 0: # Game scene
                    pass
                elif self.option_cursor == 1: # Quit game
                    game.quit = True



def handle_input(game: Game, scene: BaseScene) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit = True
        else:
            scene.handle_input(game, event)


def draw_screen(game: Game, scene: BaseScene) -> None:
    game.screen.fill((0, 0, 0))
    scene.draw(game)


def update_scene(game: Game, scene: BaseScene) -> None:
    dt = game.tick()
    scene.update(dt)
    pygame.display.update()


def main() -> None:
    pygame.init()
    game = Game(DEFAULT_SCREEN_SIZE)
    font = pygame.font.Font(FONTS_PATH + "PixelMplus12-Regular.ttf", 60)
    scene: BaseScene = MenuScene(DEFAULT_SCREEN_SIZE, font)

    while not game.quit:
        handle_input(game, scene)
        draw_screen(game, scene)
        update_scene(game, scene)

    pygame.quit()


if __name__ == "__main__":
    main()


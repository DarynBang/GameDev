import pygame
import sys
from script.entities import *
from script.utils import *
from script.tilemap import Tilemap
from script.clouds import *
from icecream import ic

yellow = (255, 255, 0)
purple = (160, 32, 240)
MAP_PATH = r'C:\Users\steph\Desktop\pygame_files\mapss.json'

class Game:
    def __init__(self):
        # Start up pygame
        pygame.init()

        # Set up name and screen for game
        pygame.display.set_caption(title="random game")
        self.screen = pygame.display.set_mode(size=(800, 600))

        # Surface is an empty image and will be used for rendering
        self.display = pygame.Surface((320, 240))

        font = pygame.font.SysFont('comicsansms', 14)

        # Restrict fps for the game
        self.clock = pygame.time.Clock()

        self.movement = [False, False]


        # Assets are used to load images
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'background': load_image('background2.png'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'cloud': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_duration=6),
            'player/run': Animation(load_images('entities/player/run'), img_duration=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'))
        }

        # ic(self.assets)

        self.player = Player(self, pos=(100, 50), size=(8, 15))

        self.clouds = Clouds(self.assets['cloud'], count=12)
        self.tilemap = Tilemap(self, tile_size=16)

        try:
            self.tilemap.load_map(MAP_PATH)
        except FileNotFoundError or FileExistsError:
            ic("No map found")


        # Variable to adjust camera position
        self.scroll = [0, 0]

        self.num_jumps_left = 2

        self.leaf_spawners  = []

        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree.pos[0], 4 + tree.pos[1], 23, 13))
            ic(tree.get_dict())

        self.num_jumps_text = Text(f"Number of jumps left: {str(self.num_jumps_left)}", (self.display.get_width() // 4, 10),
                                   font, yellow)


    def run(self):
        # Each frame is an iteration in a loop -> Update screen after getting data for each iteration
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            # self.scroll += (where the camera should be centered - where the camera originally was) / extra distance
            self.scroll[0] += (self.player.create_rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.create_rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            rendered_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=rendered_scroll)

            self.tilemap.render(self.display, offset=rendered_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=rendered_scroll)

            # For loop for getting user input
            # An event can be a button press, mouse moving or any kind of interaction
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                ## KEYDOWN -> A key is pressed, KEYUP -> A key stops being pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.num_jumps_left > 0:
                        self.player.velocity[1] = -5

                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True

                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and self.num_jumps_left > 0:
                        self.num_jumps_left -= 1
                        self.num_jumps_text.update_text(f"Number of jumps left: {str(self.num_jumps_left)}")

                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False

                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            if self.player.collisions['down']:
                self.num_jumps_left = 2
                self.num_jumps_text.update_text(f"Number of jumps left: {str(self.num_jumps_left)}")


            self.num_jumps_text.render(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), dest=(0, 0))

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    Game().run()

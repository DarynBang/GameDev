import pygame
import sys
from script.entities import *
from script.utils import *
from script.tilemap import *
from script.clouds import *
from icecream import ic

yellow = (255, 255, 0)
purple = (160, 32, 240)

MAP_PATH = r'C:\Users\steph\Desktop\pygame_files\mapss.json'

RENDER_SCALE = 2.0  # Render scale is 2 because the screen is 2x larger than the display, so we have to scale down the mouse position
class Editor:
    def __init__(self):
        # Start up pygame
        pygame.init()

        # Set up name and screen for game
        pygame.display.set_caption(title="editor")
        self.screen = pygame.display.set_mode(size=(640, 480))

        # Surface is an empty image and will be used for rendering
        self.display = pygame.Surface((320, 240))

        # Restrict fps for the game
        self.clock = pygame.time.Clock()

        self.movement = [False, False, False, False]  # For moving camera
        font = pygame.font.SysFont('comicsansms', 14)

        # Assets are used to load images
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
        }

        # ic(self.assets)

        self.tilemap = Tilemap(self, tile_size=16)

        # Load pre-saved map
        try:
            self.tilemap.load_map(MAP_PATH)
        except FileNotFoundError or FileExistsError:
            ic("No map found")
        #     pass

        # Variable to adjust camera position
        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 1  # groups: grass, large decor or stone
        self.tile_variant = 0

        self.left_clicking = False
        self.right_clicking = False

        self.shift_key = False

        self.on_grid = True

        self.ctrl_key = False

        self.zoom = 1.0  # Initial zoom level

        self.flip = False

        self.zoom_text = Text(f"Current zoom level: {round(self.zoom, 2)}", (self.display.get_width() / 1.5, 10), font, yellow)

    def run(self):
        # Each frame is an iteration in a loop -> Update screen after getting data for each iteration
        while True:
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 3
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 3

            rendered_scroll = (int(self.scroll[0] * self.zoom), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=rendered_scroll, zoom=self.zoom)
            self.zoom_text.render(self.display)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant]
            current_tile_img.set_alpha(150)  # 0 -> fully transparent and 255 -> fully opaque

            mouse_pos = pygame.mouse.get_pos()

            mouse_pos = (mouse_pos[0] / RENDER_SCALE / self.zoom, mouse_pos[1] / RENDER_SCALE / self.zoom)  # Rendered mouse position
            # Mouse position in terms of tile position
            tile_pos = (int(mouse_pos[0] + rendered_scroll[0]) // self.tilemap.tile_size,
                        int(mouse_pos[1] + rendered_scroll[1]) // self.tilemap.tile_size)

            display_img = current_tile_img.copy()

            if self.flip:
                current_tile_img = pygame.transform.flip(current_tile_img, True, False)

            if self.on_grid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size * self.zoom - self.scroll[0] * self.zoom,
                                                     tile_pos[1] * self.tilemap.tile_size * self.zoom - self.scroll[1] * self.zoom))
            else:
                self.display.blit(current_tile_img, (mouse_pos[0] * self.zoom, mouse_pos[1] * self.zoom))

            if not self.ctrl_key:
                # Place down tile
                if self.left_clicking and self.on_grid:
                    current_tile = Tile(self.tile_list[self.tile_group], self.tile_variant, tile_pos)
                    if self.flip:
                        current_tile.flip = True
                    self.tilemap.tile_map[f"{tile_pos[0]};{tile_pos[1]}"] = current_tile

                # Remove tile
                if self.right_clicking:
                    tile_loc = f"{tile_pos[0]};{tile_pos[1]}"
                    if tile_loc in self.tilemap.tile_map:
                        del self.tilemap.tile_map[tile_loc]

                    for tile in self.tilemap.offgrid_tiles.copy():
                        tile_img = self.assets[tile.type][tile.variant]
                        tile_img_width, tile_img_height = tile_img.get_size()

                        tile_rect = pygame.Rect(tile.pos[0] - self.scroll[0], tile.pos[1] - self.scroll[1], tile_img_width, tile_img_height)
                        if tile_rect.collidepoint(mouse_pos):
                            self.tilemap.offgrid_tiles.remove(tile)


            self.display.blit(display_img, (5, 5))

            # For loop for getting user input
            # An event can be a button press, mouse moving or any kind of interaction
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.left_clicking = True
                        if not self.on_grid:
                            current_offgrid_tile = Tile(self.tile_list[self.tile_group], self.tile_variant,
                                                                   (mouse_pos[0] + self.scroll[0], mouse_pos[1] + self.scroll[1]))
                            if self.flip:
                                current_offgrid_tile.flip = True
                            self.tilemap.offgrid_tiles.append(current_offgrid_tile)

                    if event.button == 3:
                        self.right_clicking = True

                    if not self.ctrl_key:
                        if self.shift_key:
                            if event.button == 4:
                                self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])

                            if event.button == 5:
                                self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])

                            self.flip = False

                        else:
                            if event.button == 4:
                                self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                                self.tile_variant = 0


                            if event.button == 5:
                                self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                                self.tile_variant = 0

                            self.flip = False


                    if self.ctrl_key:
                        if event.button == 4:  # Scroll up
                            self.zoom = min(self.zoom + 0.1, 5)  # Cap the zoom level to a maximum value
                        if event.button == 5:  # Scroll down
                            self.zoom = max(self.zoom - 0.1, 0.5)  # Cap the zoom level to a minimum value
                        if abs(self.zoom - 1) < 0.01:
                            self.zoom = 1
                        self.zoom_text.update_text(f"Current zoom level: {round(self.zoom, 2)}")




                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.left_clicking = False

                    if event.button == 3:
                        self.right_clicking = False



                ## KEYDOWN -> A key is pressed, KEYUP -> A key stops being pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True

                    if event.key == pygame.K_d:
                        self.movement[1] = True

                    if event.key == pygame.K_w:
                        self.movement[2] = True

                    if event.key == pygame.K_s:
                        self.movement[3] = True

                    if event.key == pygame.K_LSHIFT:
                        self.shift_key = True

                    if event.key == pygame.K_LCTRL:
                        self.ctrl_key = True

                    if event.key == pygame.K_f:
                        self.flip = not self.flip

                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False

                    if event.key == pygame.K_d:
                        self.movement[1] = False

                    if event.key == pygame.K_w:
                        self.movement[2] = False

                    if event.key == pygame.K_s:
                        self.movement[3] = False

                    if event.key == pygame.K_o:
                        ic(self.tilemap)
                        self.tilemap.save_map(r'C:\Users\steph\Desktop\pygame_files\mapss.json')

                    if event.key == pygame.K_LSHIFT:
                        self.shift_key = False

                    if event.key == pygame.K_LCTRL:
                        self.ctrl_key = False



            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), dest=(0, 0))

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    Editor().run()

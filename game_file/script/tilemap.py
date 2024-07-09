import pygame
import json


NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
## All the combinations of locations surrounding entities

PHYSICS_TILES = ('grass', 'stone')
## Tiles that have physics properties applied to

class Tile:
    def __init__(self,
                 type: str,
                 variant: int,
                 pos,
                 flip: bool = False):
        self.type = type
        self.variant = variant
        self.pos = pos

        self.flip = flip

    def get_dict(self):
        return {
            'type': self.type,
            'variant': self.variant,
            'pos': self.pos,
            'flip': self.flip
        }

    def copy(self):
        return Tile(self.type, self.variant, self.pos.copy(), self.flip)

class Tilemap:
    def __init__(self,
                 game,
                 tile_size: int):
        self.game = game
        self.tile_size = tile_size

        self.tile_map = {}
        # tile_map is a dictionary of tiles on a square grid

        self.offgrid_tiles = []
        # List of objects that aren't on the grid

        #  { (0, 0): 'grass'. {0, 1}: 'dirt', (9999, 0): 'grass' } -> An idea of how the map should look like

    def save_map(self, path):
        ##  Tile Objects are not serializable to Json, so we convert it into a Json-compatible format.
        serializable_tile_map = {}
        for k, v in self.tile_map.items():
            serializable_tile_map[f"{k}"] = v.get_dict()

        serializable_offgrid_tiles = [tile.get_dict() for tile in self.offgrid_tiles]

        f = open(path, 'w')
        json.dump({'tilemap': serializable_tile_map,
                   'tile_size': self.tile_size,
                   'offgrid_tiles': serializable_offgrid_tiles}, f)
        f.close()


    def load_map(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        offgrid_tiles_dict = map_data['offgrid_tiles']
        tile_map_dict = map_data['tilemap']
        saved_tile_map = {}

        for k, v in tile_map_dict.items():
            saved_tile_map[f"{k}"] = Tile(v['type'], v['variant'], v['pos'], v['flip'])

        saved_offgrid_tiles = [Tile(tile['type'], tile['variant'], tile['pos'], tile['flip']) for tile in offgrid_tiles_dict]

        self.tile_map = saved_tile_map
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = saved_offgrid_tiles


    def extract(self, id_pairs, keep=False):
        # An id pair is (tile type, its variant)
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile.type, tile.variant) in id_pairs:
                matches.append(tile.copy())

                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tile_map:
            tile = self.tile_map[loc]
            if (tile.type, tile.variant) in id_pairs:
                copied_tile = tile.copy()
                copied_tile.pos[0] *= self.tile_size
                copied_tile.pos[1] *= self.tile_size
                matches.append(copied_tile)

                if not keep:
                    del self.tile_map[loc]

        return matches


    ## Function to return a list of tiles around a specific tile
    def tiles_around(self, pos):
        tile_loc = (int(pos[0] // self.tile_size)), int(pos[1] // self.tile_size)  # Convert pixel position to a grid position
        tiles = []
        for offset in NEIGHBOR_OFFSETS:
            check_loc = f'{tile_loc[0] + offset[0]};{tile_loc[1] + offset[1]}'
            if check_loc in self.tile_map:
                tiles.append(self.tile_map[check_loc])
        return tiles

    ## Return pygame rect objects that have physics properties from specific tile types
    def physics_rect_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile.type in PHYSICS_TILES:
                rects.append(pygame.Rect(tile.pos[0] * self.tile_size,
                                         tile.pos[1] * self.tile_size,
                                         self.tile_size,
                                         self.tile_size))

        return rects


    def render(self, surface, offset=(0, 0), zoom=1.0):

        for tile in self.offgrid_tiles:
            tile_img = self.game.assets[tile.type][tile.variant]
            tile_img_width, tile_img_height = tile_img.get_size()
            scaled_img = pygame.transform.scale(tile_img, (int(tile_img_width * zoom), int(tile_img_height * zoom)))

            if tile.flip:
                scaled_img = pygame.transform.flip(scaled_img, True, False)

            surface.blit(scaled_img,
                         ((tile.pos[0] - offset[0]) * zoom,
                          (tile.pos[1] - offset[1]) * zoom))


        start_x = int(offset[0] // self.tile_size)
        end_x = int((offset[0] + surface.get_width() / zoom) // self.tile_size + 1)
        start_y = int(offset[1] // self.tile_size)
        end_y = int((offset[1] + surface.get_height() / zoom) // self.tile_size + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                location = f"{x};{y}"
                if location in self.tile_map:
                    tile = self.tile_map[location]

                    tile_img = self.game.assets[tile.type][tile.variant]
                    tile_img_width, tile_img_height = tile_img.get_size()
                    scaled_img = pygame.transform.scale(tile_img,
                                                        (int(tile_img_width * zoom), int(tile_img_height * zoom)))

                    if tile.flip:
                        scaled_img = pygame.transform.flip(scaled_img, True, False)

                    surface.blit(scaled_img,
                                 ((tile.pos[0] * self.tile_size - offset[0]) * zoom,
                                  (tile.pos[1] * self.tile_size - offset[1]) * zoom))





from script.tilemap import *
import json
from icecream import ic

MAP_PATH = r'C:\Users\steph\Desktop\pygame_files\map.json'

f = open(MAP_PATH, 'r')
map_data = json.load(f)
offgrid_tiles_dict = map_data['offgrid_tiles']
tile_size = map_data['tile_size']
tile_map_dict = map_data['tilemap']
tile_map = {}

for k, v in tile_map_dict.items():
    tile_map[f"{k}"] = Tile(v['type'], v['variant'], v['pos'])

offgrid_tiles = [Tile(tile['type'], tile['variant'], tile['pos']) for tile in offgrid_tiles_dict]

ic(tile_map)
ic(offgrid_tiles)
ic(map_data['tile_size'])



import pygame

class PhysicsEntity:
    def __init__(self,
                 game,
                 e_type: str,
                 pos: tuple[int, int],
                 size: tuple[int, int]):
        self.game = game
        self.type = e_type  # Entity type
        self.pos = list(pos)  # Positions is set as a list so each entity can have its own list for its position
        self.size = size
        self.velocity = [0.0, 0.0]
        # Dictionary to check in what direction did the entity collide with
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.animation = any
        self.action = ''
        self.animation_offset = (-3, -3)
        self.flip = False  # Control direction the player is facing
        self.set_action('idle')

    def create_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()


    def update(self, tile_map, movement=(0, 0)):
        # collisions dictionary is reset back to False after every frame
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        ## first element in pos represents x axis
        self.pos[0] += frame_movement[0]
        entity_rect = self.create_rect()
        for rect in tile_map.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        ## second element in pos represents y axis
        self.pos[1] += frame_movement[1]
        entity_rect = self.create_rect()
        for rect in tile_map.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

            
        self.velocity[1] = min(5.0, self.velocity[1] + 0.2)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()


    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.animation_offset[0],
                                                                                     self.pos[1] - offset[1] + self.animation_offset[1]))
        # surface.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Player(PhysicsEntity):
    def __init__(self,
                 game,
                 pos: tuple[int, int],
                 size: tuple[int, int]):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0

        if self.air_time >= 5:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')


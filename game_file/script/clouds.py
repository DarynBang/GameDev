import random

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surface, offset=(0, 0)):
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surface.blit(self.img, (render_pos[0] % (surface.get_width() + self.img.get_width()) - self.img.get_width(),
                            (render_pos[1] % (surface.get_height() + self.img.get_height()) - self.img.get_height())))

class Clouds:
    def __init__(self, cloud_images, count=12):
        self.clouds = []

        for i in range(count):
            self.clouds.append(Cloud(pos = (random.random() * 99999, random.random() * 99999),
                               img = random.choice(cloud_images),
                               speed = random.random() * 0.01 + 0.1,
                               depth = random.random() * 0.2 + 0.5))

            self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()


    def render(self, surface, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surface, offset=offset)


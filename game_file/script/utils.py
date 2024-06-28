import pygame
import os

BASE_IMG_PATH = r'C:\Users\steph\Desktop\pygame_files\00_resources\data\images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()

    img.set_colorkey((0, 0, 0))

    return img

def load_images(path):
    images = []

    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + "/" + img_name))

    return images

class Animation:
    def __init__(self,
                 images: list,
                 img_duration: int = 5,
                 loop=True):
        self.images = images
        self.img_duration = img_duration  # Number of frames of image in the animation
        self.loop = loop
        self.done = False  # Set to true if reaches the end of loop
        self.frame = 0   # Keep track of animation step

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def img(self):
        return self.images[int(self.frame / self.img_duration)]

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))  # Use modulo to loop back to 0

        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True


class Text:
    def __init__(self, text, pos, font, color):
        self.text = text
        self.color = color
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))

    def render(self, surface):
        surface.blit(self.text_surface, self.text_rect)




class Particle:
    def __init__(self, game, p_type, pos, velocity=[0.0, 0.0], frame=0):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particles/' + p_type].copy()
        self.animation.frame = frame

    def update(self):
        kill = False

        if self.animation.done:
            kill = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()  # Update the animation to move the particles

        # Return true as soon as the animation is finished
        return kill

    def render(self, surface, offset=(0, 0)):
        image = self.animation.img()
        surface.blit(image, (self.pos[0] - offset[0] - image.get_width() // 2, self.pos[1] - offset[1] - image.get_height() // 2))


class GameObject:
    def __init__(self, x, y, texture, width, height, frame, solid, collidable, consumable, onCollide, onConsume, hit, animation, key):
        self.x = x
        self.y = y
        self.texture = texture
        self.width = width
        self.height = height
        self.frame = frame
        self.solid = solid
        self.collidable = collidable
        self.consumable = consumable
        self.onCollide = onCollide
        self.onConsume = onConsume
        self.hit = hit
        self.animation = animation
        if self.texture == 'keys-and-locks':
            if key:
                self.key = True
            else:
                self.key = False

    def collides(self, target):
        return not (target.x > self.x + self.width or self.x > target.x + target.width or
            target.y > self.y + self.height or self.y > target.y + target.height)

    def update(self, dt):
        if self.animation:
            self.animation.update(dt)

    def render(self):
        if self.animation:
            pass
        else:
            pass
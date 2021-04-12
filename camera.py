class Camera:
    STEP_SIZE = 20

    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def move(self, x, y):
        self.dx += x
        self.dy += y

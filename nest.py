class Nest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_count = 0

    def __str__(self):
        return f'Nest food count = {self.food_count}'

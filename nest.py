class Nest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ants_inside = 0
        self.ants_outside = 0

    def update_ant_status(self, ants):
        self.ants_inside = 0
        self.ants_outside = 0
        for ant in ants:
            if ant.x == self.x and ant.y == self.y:
                self.ants_inside += 1
            else:
                self.ants_outside += 1

    def __str__(self):
        return f'Nest at ({self.x}, {self.y}): {self.ants_inside} ants inside, {self.ants_outside} ants outside'

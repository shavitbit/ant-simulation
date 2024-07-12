import numpy as np
import random
from models.nest import Nest

class Environment:
    def __init__(self, width, height, num_of_food):
        self.width = width
        self.height = height
        self.localnest = Nest(width // 2, height // 2)
        self.num_of_food = num_of_food
        self.environment = np.zeros((width, height))
        self.environment[self.localnest.x, self.localnest.y] = -2
        self.pheromone_grid = np.zeros((width, height))
        self.place_food()

    def place_food(self):
        for _ in range(self.num_of_food):
            food_x, food_y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            self.environment[food_x, food_y] = 50

    def add_food_to_nest(self):
        self.localnest.food_count += 1

    def pheromone_decay(self, decay_factor=0.5):
        self.pheromone_grid = np.maximum(0, self.pheromone_grid - decay_factor)
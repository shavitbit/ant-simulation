import numpy as np
import random
from nest import Nest
# environment[x,y] = 0 --> 0 represents empty space
# environment[x,y] = 1 --> 1,2,3 ...n represents the Food
# environment[x,y] = -2 --> -2 represents the Nest

class Environment:
    def __init__(self, width, height,num_of_food):
        # Whidth and height of the envaronment greed 
        self.width = width
        self.height = height
        #Create new nest and place it in the middle
        self.localnest = Nest(width // 2 , height // 2) 
        self.num_of_food = num_of_food
        # Create a grid to represent the environment
        self.environment = np.zeros((width, height))        
        self.environment[self.localnest.x, self.localnest.x] = -2  # -2 represents the nest
        # Create new pheramone_grid
        self.pheromone_grid = np.zeros((width, height))
        self.place_food()

    # Place Food randomly on environment grid - the amount of food is self.num_of_food
    def place_food (self):
        for _ in range(self.num_of_food):
            food_x, food_y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            self.environment[food_x, food_y] = 50
    
    # Add collected food to the nest
    def add_food_to_nest(self):
        self.localnest.food_count += 1

    def pheromone_decay(self, pheromone_grid, decay_factor=0.5):
        for i in range(pheromone_grid.shape[0]):
            for j in range(pheromone_grid.shape[1]):
                pheromone_grid[i, j] = pheromone_grid[i, j] - decay_factor
                if pheromone_grid[i, j] < 0:
                    pheromone_grid[i, j] = 0    



#Need to correct the toString method
    def __str__(self):
        return f'Nest at ({self.x}, {self.y}): {self.ants_inside} ants inside, {self.ants_outside} ants outside'

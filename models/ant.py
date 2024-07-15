import random
import string
from abc import ABC, abstractmethod

# An abstract class that represents an ant
# Create new scout ant or worker ant that inherits from this class
class Ant(ABC):
    def __init__(self, environment,drop_pheromone_value):
        self.environment = environment
        self.x = environment.localnest.x
        self.y = environment.localnest.y
        self.carrying_food = False
        self.nest_x = environment.localnest.x
        self.nest_y = environment.localnest.y
        self.name = "ant-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        self.drop_pheromone_value = drop_pheromone_value



    def sense_food(self):
        if self.environment.environment[self.x, self.y] > 0:
            self.carrying_food = True
            self.environment.environment[self.x, self.y] -= 1

    def drop_pheromone(self,drop_pheromone_value):
        if self.carrying_food:
            distance_to_nest = abs(self.x - self.nest_x) + abs(self.y - self.nest_y)
            self.environment.pheromone_grid[self.x, self.y] += drop_pheromone_value * distance_to_nest
    
    def decrement_pheromone_if_overlap(self, ant_positions,decrement_pheromone_if_overlap_value):

        num_ants_at_position = ant_positions.get((self.x, self.y), 0)

        if num_ants_at_position > 1:

            self.environment.pheromone_grid[self.x, self.y] = max(0, self.environment.pheromone_grid[self.x, self.y] - (num_ants_at_position * decrement_pheromone_if_overlap_value))    

    def sense_pheromone(self):
        sensing_radius = self.get_sensing_radius()
        max_pheromone = 0
        best_move = None
        
        for dx in range(-sensing_radius, sensing_radius + 1):
            for dy in range(-sensing_radius, sensing_radius + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < self.environment.width and 0 <= new_y < self.environment.height:
                    if self.environment.pheromone_grid[new_x, new_y] > max_pheromone:
                        max_pheromone = self.environment.pheromone_grid[new_x, new_y]
                        best_move = (new_x, new_y)

        if best_move:
            move_x, move_y = best_move
            if move_x < self.x:
                return 'left'
            elif move_x > self.x:
                return 'right'
            elif move_y < self.y:
                return 'up'
            elif move_y > self.y:
                return 'down'
        return None
   
    def apply_move(self, direction):
        if direction == 'up' and self.y > 0:
            self.y -= 1
        elif direction == 'down' and self.y < self.environment.height - 1:
            self.y += 1
        elif direction == 'left' and self.x > 0:
            self.x -= 1
        elif direction == 'right' and self.x < self.environment.width - 1:
            self.x += 1

    def go_nest(self):
        if self.x < self.nest_x:
            self.x += 1
        elif self.x > self.nest_x:
            self.x -= 1

        if self.y < self.nest_y:
            self.y += 1
        elif self.y > self.nest_y:
            self.y -= 1

        if self.x == self.nest_x and self.y == self.nest_y and self.carrying_food:
            self.carrying_food = False
            self.environment.add_food_to_nest()
    
    def get_sensing_radius(self):
        return 5    # Default sensing radius for generic Ant

    def __str__(self):
        return f"I am {self.name}, at ({self.x}, {self.y}), carrying food: {self.carrying_food}"
import random
import string
from environment import Environment as enviro
class Ant:
    def __init__(self, environment):#x, y, height, width, environment):
        self.x = environment.localnest.x
        self.y = environment.localnest.y
        self.environment = environment
        self.carrying_food = False
        self.height = environment.height
        self.width = environment.width
        self.nest_x = environment.localnest.x
        self.nest_y = environment.localnest.y
        self.name = "ant-" + "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))

    def move(self, pheromone_grid):
        # Move based on pheromone concentration
        if self.carrying_food == True:
            self.go_nest()
            self.drop_pheromone(pheromone_grid)
        else:
            best_move = self.sense_pheromone(pheromone_grid)
            if best_move:
                if best_move == 'up' and self.y > 0:
                    self.y -= 1
                elif best_move == 'down' and self.y < self.height - 1:
                    self.y += 1
                elif best_move == 'left' and self.x > 0:
                    self.x -= 1
                elif best_move == 'right' and self.x < self.width - 1:
                    self.x += 1
            else:
                # If no pheromone detected, move randomly
                random_move = random.choice(['up', 'down', 'left', 'right'])
                if random_move == 'up' and self.y > 0:
                    self.y -= 1
                elif random_move == 'down' and self.y < self.height - 1:
                    self.y += 1
                elif random_move == 'left' and self.x > 0:
                    self.x -= 1
                elif random_move == 'right' and self.x < self.width - 1:
                    self.x += 1

    def sense_food(self, environment):
        # Simple sensing for now
        if environment.environment[self.x, self.y] == 1:
            self.carrying_food = True
            environment.environment[self.x, self.y] = 0  # Remove food from the environment

    def drop_pheromone(self, pheromone_grid):
        if self.carrying_food:
           # Calculate the Manhattan distance to the nest
           distance_to_nest = abs(self.x - self.nest_x) + abs(self.y - self.nest_y)

           # Add pheromone proportional to the distance to the nest
           # You can adjust the factor if needed
           pheromone_grid[self.x, self.y] += 10 * (distance_to_nest + 1)

    def sense_pheromone(self, pheromone_grid):
        # Define the Sensing Radius
        sensing_radius = 1
        max_pheromone = 0
        best_move = None
        possible_moves = ['up', 'down', 'left', 'right']

        for move in possible_moves:
            new_x, new_y = self.x, self.y
            if move == 'up' and self.y > 0:
                new_y -= 1
            elif move == 'down' and self.y < self.height - 1:
                new_y += 1
            elif move == 'left' and self.x > 0:
                new_x -= 1
            elif move == 'right' and self.x < self.width - 1:
                new_x += 1
            
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                if pheromone_grid[new_x, new_y] > max_pheromone:
                    max_pheromone = pheromone_grid[new_x, new_y]
                    best_move = move

        return best_move


    def go_nest(self):
        # Move towards the nest
        if self.x < self.nest_x:
            self.x += 1
        elif self.x > self.nest_x:
            self.x -= 1

        if self.y < self.nest_y:
            self.y += 1
        elif self.y > self.nest_y:
            self.y -= 1

        if self.x == self.nest_x and self.y == self.nest_y:
           self.carrying_food = False
           
           


        


    def to_string(self):
        print("I am " + self.name)
        print("My location is: " + str(self.x) + " " + str(self.y))
        print("Do I carry food? " + str(self.carrying_food))



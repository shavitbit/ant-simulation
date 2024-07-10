import random
import string

class Ant:
    def __init__(self, environment):
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
        if self.carrying_food:
            self.drop_pheromone(pheromone_grid)
            self.go_nest()
            
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
        if environment.environment[self.x, self.y] > 0:
            self.carrying_food = True
            environment.environment[self.x, self.y] -= 1  # Decreace the food count

    def drop_pheromone(self, pheromone_grid):
        if self.carrying_food:
           # Calculate the Manhattan distance to the nest
           distance_to_nest = abs(self.x - self.nest_x) + abs(self.y - self.nest_y)

           # Add pheromone proportional to the distance to the nest
           # You can adjust the factor if needed
           #if pheromone_grid[self.x, self.y] < 300:
           pheromone_grid[self.x, self.y] += 3.5 * (distance_to_nest + 1)

    def sense_pheromone(self, pheromone_grid):
        sensing_radius = 5
        max_pheromone = 0
        best_move = None
    
        for dx in range(-sensing_radius, sensing_radius + 1):
            for dy in range(-sensing_radius, sensing_radius + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    if pheromone_grid[new_x, new_y] > max_pheromone:
                        max_pheromone = pheromone_grid[new_x, new_y]
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
           self.environment.add_food_to_nest()
           
           


        


    def to_string(self):
        print("I am " + self.name)
        print("My location is: " + str(self.x) + " " + str(self.y))
        print("Do I carry food? " + str(self.carrying_food))



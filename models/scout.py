from models.ant import Ant
import random
class Scout(Ant):
   #  sense_pheromone completed
   
    def move(self):
        if self.carrying_food:
            self.drop_pheromone(self.drop_pheromone_value)
            self.go_nest()
        else:
            self.random_or_pheromone_move()

    def random_or_pheromone_move(self):
        best_move = self.sense_pheromone()
        if best_move:
            self.apply_move(best_move)
        else:
            self.random_move()

 
    def random_move(self):
        direction = random.choice(['up', 'down', 'left', 'right'])
        self.apply_move(direction)
    def get_sensing_radius(self):
        return 5  # Sensing radius for Scout

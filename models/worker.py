from models.ant import Ant
class Worker(Ant):
    
    def move(self):
        if self.carrying_food:
            self.drop_pheromone(self.drop_pheromone_value)
            self.go_nest()
        else:
            self.home_or_pheromone_move()

    def home_or_pheromone_move(self):
        best_move = self.sense_pheromone()
        if best_move:
            self.apply_move(best_move)
        else:
                self.go_nest()

    def get_sensing_radius(self):
            return 10  # Sensing radius for Worker
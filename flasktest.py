from flask import Flask, jsonify, render_template
import numpy as np
from ant import Ant
from environment import Environment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['GET'])
def simulate():
    # Run your simulation code here and return the result
    environment = Environment(width=100, height=100, num_of_food=20)
    ants = [Ant(environment) for _ in range(20)]
    # Simulate some steps
    for _ in range(400):
        for ant in ants:
            ant.move(environment.pheromone_grid)
            ant.sense_food(environment)
            ant.drop_pheromone(environment.pheromone_grid)
            environment.pheromone_decay(environment.pheromone_grid)
    # Prepare the data to return
    ant_positions = [(ant.x, ant.y) for ant in ants]
    food_positions = np.argwhere(environment.environment > 0).tolist()
    pheromone_grid = environment.pheromone_grid.tolist()
    return jsonify({
        'ant_positions': ant_positions,
        'food_positions': food_positions,
        'pheromone_grid': pheromone_grid
    })

if __name__ == '__main__':
    app.run(debug=True)
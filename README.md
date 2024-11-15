# Ant Simulation (still in development)

Ant Simulation is a Python-based project that simulates the behavior of ants to find the fastest way to collect food using a combination of parameters. The simulation can be run with a graphical user interface (GUI) using Matplotlib, command-line interface (CLI) using argparse or application programming interface (API) using Flask.
## Features

- Visual simulation of ant behavior using Matplotlib.
- Adjustable parameters via sliders in the GUI.
- CLI mode for running simulations without visual effects.
- Send simulation results to a web server.
- Webpage with statistics result including bar charts, API, and a Swagger page (/home, /swagger)

## Requirements

- Python 3.6+
- numpy
- matplotlib
- requests
- argparse
- Docker - for running the CLI alongside the web server
- Kubernetes/Minikube - for running the web server and extensive parallel simulation jobs in Kubernetes

## Simulation Objects
### Environment
 Environment class represents the environment in which the ants are moving. It contains the following attributes:
  - 2D array that represents the environment.
  - 2D array that represents pheromone trails.
  - Food sources that are randomly placed in the environment, with each food source having 50 pieces of food.
### Ant
The Ant class is an abstract class that represents an ant (you can create new scout ants or worker ants that inherit from the Ant class). It contains the following attributes:
 - Sense Food Function - If the ant is standing on a food source, it will collect the food and move to the nest.
 - Sense Pheromone Function - If the ant is standing on a pheromone trail, it will follow the trail. Scouts can sense pheromone within a 5px radius, and workers within a 10px radius.
 - Drop Pheromone Function - If the ant has food, it will calculate the distance to the nest and drop more pheromone near the food source, decreasing the pheromone amount as it gets closer to the nest.
 - Decrement Pheromone If Overlap Function - When too many ants are in the same place, it reduces the pheromone concentration at that spot.
 - Apply Move Function - Checks if the ant can move to the next cell (i.e., there is no wall or obstacle), and if the ant can move, it will move to the next cell.
 - Go Nest - When the ant finds food, it will go directly to the nest.
 - Get Sensing Radius - Retrieves the sensing radius of the ant.
#### Scout Ant
A scout ant moves randomly through the environment, cell by cell, searching for pheromone trails or food sources. If it finds food, it will deposit pheromone and return to its nest.
 - Move - If carrying food, it drops pheromone and goes to the nest; otherwise, it makes a random move or follows a pheromone trail.
 - Random or Pheromone Move - Decides if the ant should move to the next cell randomly or follow a pheromone trail.
 - Random Move - Randomly chooses between moving up, down, left, or right

#### Worker Ant
A worker ant stays at the nest and, when a scout ant returns, follows the trail to collect the food. The worker ant has a better sensing radius and is always ready at the nest to follow pheromone trails.
 - Move - If carrying food, it drops pheromone and goes to the nest; otherwise, it follows the nest pheromone trail.
 - Home or Pheromone Move - Decides if the ant should return to the nest or follow a pheromone trail.
 - Sensing Radius - Defines the range within which the ant can detect pheromone trails and food.

#### Nest class
 The Nest class represents the nest of the ants. It contains the following attributes:
 - X and Y coordinates of the nest.
 - Food counter


## Simulation Parameters
'Ant simulation' simulates the behavior of ants to find the fastest way to collect food using a combination 4 parameters and in 1600 steps.
1. Decrement Pheromone If Overlap:<br/>
The function is designed to manage the pheromone levels in the simulation environment.
When too many ants are in the same place, it reduces the pheromone concentration at that spot.
This helps to prevent the pheromone trail from becoming too strong and encourages ants to explore other paths, promoting more realistic foraging behavior.
```python
max(0, pheromone_grid[x,y] - (num_ants_at_position * decrement_pheromone_if_overlap_value)
```
2. Pheromone Decay:<br/> Allows you to adjust the rate at which pheromone trails left by the ants dissipate over time.
Pheromone decay is a crucial aspect of ant behavior simulation as it controls how long the pheromone scent remains effective in guiding other ants towards food sources.
```python
max(0, pheromone_grid - pheromone_decay_value)
```
3. Drop Pheromone: <br/>
Allows you to adjust the amount of pheromone that each ant deposits on the ground as it moves.
Pheromone deposition is a key mechanism in ant behavior simulations, as it influences how other ants navigate and make decisions. Only ants with food can drop pheromone.
```python
pheromone_grid[x,y] += distance_to_nest * drop_pheromone_value
```
4. Worker Scout Ratio: <br/>
Allows you to adjust the proportion of worker ants to scout ants in the simulation.
This ratio influences the behavior and efficiency of the ant colony, as workers and scouts have different roles.
Workers are primarily responsible for collecting food and returning it to the nest.
They have a better sensing radius and are ready at the nest to follow the pheromone trails.
Scouts are responsible for exploring the environment and laying down pheromone trails to guide workers and other scouts to food sources.
You have 30 ants, so if you choose 5 on the slider, that means you will spawn 5 workers and 25 scouts.
### GUI
Customize the slides before starting the simulation
![simulation settings Screenshot](/media/ants-settings.png) 
<!-- <img src="/media/ants-settings.png" alt="Simulation Settings Screenshot" width="400" width="200">-->
### CLI
   The simulation_id parameter format is decay-overlap-pdecay-drop-ratio in float variable for example 20.0-142.0-1.0-5.0 , where:
   * decay: Pheromone decay value.
   * overlap: Decrement pheromone if overlap value.
   * pdecay: Pheromone decay value.
   * drop: Drop pheromone value.
   * ratio: Worker to scout ratio.

## Installation GUI Mode
1. Run GUI Simulation:
   ```sh
   git clone https://github.com/shavitbit/ant-simulation.git
   cd ant-simulation
   pip install -r requirements.txt
   python main.py 
   ```
   
2. Run CLI Simulations:
   ```sh
   git clone https://github.com/shavitbit/ant-simulation.git
   cd ant-simulation
   python ant_cli.py run --rounds <number_of_rounds> --id <simulation_id> -c <server_url>
   # For example:
   python cli.py run --rounds 3 --id 20.0-142.0-1.0-5.0 -c "http://192.168.1.100:5000"
   # Meaning run 3 times, simulation id 20.0-142.0-1.0-5.0 and send results to server http://192.168.1.100:5000
   
   # Run list command to get statistics on simulation id from the server.
   python ant_cli.py list --id <simulation_id> -c <server_url>
   ```
## Installation Docker Mode
   Build mysql image from the dockerfile in mysql folder, go to root folder and build the dockerfile in flask folder and create a network.
   ```sh
   cd mysql
   docker build -f .\dockerfile . -t antmysql:0.0.3
   cd ..
   docker build -t flaskapiant:0.0.1 -f flask\dockerfile .
  docker network create app-network 
```
   Run the mysql and flask containers
   ```sh
   docker run --name mysql-container --network app-network \
    -e MYSQL_ROOT_PASSWORD=rootoren \
    -e MYSQL_DATABASE=ant_db \
    -e MYSQL_USER=oren \
    -e MYSQL_PASSWORD=oren \
    -p 3306:3306 \
    -d antmysql:0.0.3

   docker run --name flask-container --network app-network \
       -e MYSQL_HOST=mysql-container \
       -e MYSQL_USER=oren \
       -e MYSQL_PASSWORD=oren \
       -e MYSQL_DB=ant_db \
       -p 5000:5000 \
       -d flaskapiant:0.0.1
   ```
## Installation Kubernetes Mode

### Diagrams
#### GUI and class structure 
![Web server and class structure](/media/Ant_diagram.drawio.png)

#### Web page
![Web server and class structure](/media/web.png)
#### Swagger
![Web server and class structure](/media/swagger.png)
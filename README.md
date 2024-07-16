# Ant Simulation (still in development)

Ants Simulation is a Python-based project that simulates the behavior of ants to find the fastest way to collect food using a combination of parameters. The simulation can be run both with a graphical user interface (GUI) using Matplotlib and via a command-line interface (CLI).
## Simulation Objects

## Features

- Visual simulation of ant behavior using Matplotlib.
- Adjustable parameters via sliders in the GUI.
- CLI mode for running simulations without visual effects.
- Send simulation results to a web server.

## Requirements

- Python 3.6+
- numpy
- matplotlib
- requests
- argparse

## Simulation Parameters
'Ants simulation' simulates the behavior of ants to find the fastest way to collect food using a combination 4 parameters and in 1600 steps.
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
   git clone https://github.com/shavitbit/ants-simulation.git
   cd ants-simulation
   pip install -r requirements.txt
   python main.py 
   ```
   
2. Run CLI Simulations:
   ```sh
   git clone https://github.com/shavitbit/ants-simulation.git
   cd ants-simulation
   python ant_cli.py run --rounds <number_of_rounds> --id <simulation_id> -c <server_url>
   # For example:
   python cli.py run --rounds 3 --id 20.0-142.0-1.0-5.0 -c "http://192.168.1.100:5000"
   # Meaning run 3 times, simulation id 20.0-142.0-1.0-5.0 and send results to server http://192.168.1.100:5000
   
   # Run list command to get statistics on simulation id from the server.
   python ant_cli.py list --id <simulation_id> -c <server_url>
   ```
## Installation Docker Mode

## Installation Kubernetes Mode

### Diagrams
#### GUI and class structure 
![Web server and class structure](/media/Ant_diagram.drawio.png)

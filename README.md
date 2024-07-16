# Ants Simulation

Ants Simulation is a Python-based project that simulates the behavior of ants to find the fastest way to collect food using a combination of parameters. The simulation can be run both with a graphical user interface (GUI) using Matplotlib and via a command-line interface (CLI).

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
   python ant_cli.py run --rounds <number_of_rounds> --id <simulation_id> -c <server_url>
   # For example:
   python cli.py run --rounds 3 --id 20.0-142.0-1.0-5.0 -c "http://192.168.1.100:5000"
   # Run list command to get statistics on simulation id
   python ant_cli.py list --id <simulation_id> -c <server_url>
   ```
## Installation Docker Mode

## Installation Kubernetes Mode
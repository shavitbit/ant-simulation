import argparse
import requests
from models.scout import Scout
from models.worker import Worker
from models.environment import Environment
#ID Example: 20.0-1.5-1.0-5.0
def run_simulation(rounds, sim_id, server_url):
    """
    Run the ant simulation for a specified number of rounds and send the results to a web server.

    Args:
        rounds (int): Number of simulation rounds to run.
        sim_id (str): Simulation ID containing parameters in the format 'decay-overlap-pdecay-drop-ratio'.
        server_url (str): URL of the server to send the results to.
    """
    # Parse simulation parameters from sim_id
    sim_params = [float(x) for x in sim_id.split('-')]
    decrement_pheromone_if_overlap, pheromone_decay_factor, drop_pheromone_value, worker_to_scout_ratio = sim_params

    # Define simulation constants
    num_ants = 30
    width = 100
    height = 100
    num_of_food = 20
    num_steps = 1600

    # Store results for each round
    results = []

    for _ in range(rounds):
        # Initialize environment and ants
        environment = Environment(width=width, height=height, num_of_food=num_of_food, pheromone_decay_factor=pheromone_decay_factor)
        ants = [Scout(environment, drop_pheromone_value) for _ in range(num_ants - int(worker_to_scout_ratio))] + \
               [Worker(environment, drop_pheromone_value) for _ in range(int(worker_to_scout_ratio))]

        # Run simulation steps
        for _ in range(num_steps):
            ant_positions = {}
            for ant in ants:
                ant.move()
                ant.sense_food()
                position = (ant.x, ant.y)
                if position in ant_positions:
                    ant_positions[position] += 1
                else:
                    ant_positions[position] = 1

            for ant in ants:
                ant.decrement_pheromone_if_overlap(ant_positions, int(decrement_pheromone_if_overlap))

            environment.pheromone_decay()

        # Collect food count from the nest
        results.append(environment.localnest.food_count)

    # Calculate average food collected
    total_food_collected = sum(results)  
    print(f"Average food collected: {total_food_collected / rounds}")
    # Send results to the server
    response = requests.post(server_url, json={"id": sim_id, "sim_result": total_food_collected, 'runs': rounds})
    if response.status_code == 200:
        print(f"Results successfully sent to {server_url}")
    else:
        print(f"Failed to send results to {server_url}")

def main():
    parser = argparse.ArgumentParser(description="Ant Simulation CLI")
    subparsers = parser.add_subparsers(dest="action")

    # Subparser for the 'run' action
    run_parser = subparsers.add_parser("run", help="Run the ant simulation")
    run_parser.add_argument("--rounds", type=int, required=True, help="Number of simulation rounds")
    run_parser.add_argument("--id", type=str, required=True, help="Simulation ID in the format 'decay-overlap-pdecay-drop-ratio'")
    run_parser.add_argument("-c", "--connect", type=str, required=True, help="Server URL to send results")

    # Placeholder for 'list' action
    # list_parser = subparsers.add_parser("list", help="List statistics from the web server")

    args = parser.parse_args()

    # Execute the action based on the parsed arguments
    if args.action == "run":
        run_simulation(args.rounds, args.id, args.connect)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
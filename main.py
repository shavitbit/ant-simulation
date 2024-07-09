from ant import Ant
from environment import Environment
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
#-------------------------------
num_ants = 20                   #
width = 100                     #  
height = 100                    #
num_of_food = 20                 #
# Number of simulation steps    #
num_steps = 200                 #
#--------------------------------

#Create the 2d environment include nest location, pheromone grid and randomly place food
environment = Environment(width=width,height=height,num_of_food=num_of_food)
# Create num_ants amount of ants
ants = [Ant(environment) for _ in range(num_ants)]

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, environment.width)
ax.set_ylim(0, environment.height)
ax.set_title('Ant Simulator')
ax.set_xlabel ("X")
ax.set_ylabel ("Y")

scat = ax.scatter([], [], c='red', s=10)  # Scatter plot for ants
food_scat = ax.scatter([], [], c='green', s=10)  # Scatter plot for food
pheromone_im = ax.imshow(environment.pheromone_grid, cmap='Greens', alpha=0.6, extent=[0, environment.width, 0, environment.height], origin='lower')

# Add text for frame count
frame_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
nest_scat = ax.scatter([environment.localnest.x], [environment.localnest.y], c='blue', s=50, marker='s')  # Scatter plot for the nest

# Custom format for displaying coordinates
def format_coord(x, y):
    col = int(x)
    row = int(y)
    if 0 <= col < environment.width and 0 <= row < environment.height:
        coord = f'x={col}, y={row}'
    else:
        coord = f'x={x:.2f}, y={y:.2f}'
    print(coord)
    return coord

# Set the custom coordinate formatter
ax.format_coord = format_coord

def update(frame):
    # Perform one step of the simulation
    for ant in ants:
        ant.move(environment.pheromone_grid)  # Pass pheromone_grid to move function
        ant.sense_food(environment)
        ant.drop_pheromone(environment.pheromone_grid)
        environment.pheromone_decay(environment.pheromone_grid)

    # Update ant positions
    ant_positions = [(ant.x, ant.y) for ant in ants]
    scat.set_offsets(ant_positions)

    # Update food positions
    food_positions = np.argwhere(environment.environment == 1)
    food_scat.set_offsets(food_positions)

    # Update pheromone grid
    pheromone_im.set_array(environment.pheromone_grid)

    # Update frame count text
    frame_text.set_text(f'Frame: {frame}')

    return scat, food_scat, pheromone_im, frame_text, nest_scat

# Create the animation, setting repeat to False to stop after the last frame
ani = animation.FuncAnimation(fig, update, frames=range(num_steps), interval=100, blit=True, repeat=False)

# Show the plot
plt.show()
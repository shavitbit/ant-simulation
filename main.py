import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from ant import Ant
from environment import Environment

num_ants = 20
width = 100
height = 100
num_of_food = 20
num_steps = 400

environment = Environment(width=width, height=height, num_of_food=num_of_food)
ants = [Ant(environment) for _ in range(num_ants)]

fig, ax = plt.subplots()
ax.set_xlim(0, environment.width)
ax.set_ylim(0, environment.height)
ax.set_title('Ant Simulator')
ax.set_xlabel("X")
ax.set_ylabel("Y")
fig.canvas.manager.set_window_title('Ant Simulator')

scat = ax.scatter([], [], c='red', s=10)
food_scat = ax.scatter([], [], c='green', s=10)
pheromone_im = ax.imshow(environment.pheromone_grid, cmap='gray', vmin=0, vmax=100, alpha=0.6, extent=[0, environment.width, 0, environment.height], origin='lower')
frame_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
nest_scat = ax.scatter([environment.localnest.x], [environment.localnest.y], c='blue', s=50, marker='s')

def format_coord(x, y):
    col = int(x)
    row = int(y)
    if 0 <= col < environment.width and 0 <= row < environment.height:
        coord = f'x={col}, y={row}'
    else:
        coord = f'x={x:.2f}, y={y:.2f}'
    return coord

ax.format_coord = format_coord

def update(frame):
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
        ant.decrement_pheromone_if_overlap(ant_positions)
        
    environment.pheromone_decay()

    ant_positions_list = [(ant.x, ant.y) for ant in ants]
    scat.set_offsets(ant_positions_list)

    food_positions = np.argwhere(environment.environment > 0)
    food_scat.set_offsets(food_positions)

    pheromone_im.set_array(environment.pheromone_grid)

    frame_text.set_text(f'Frame: {frame}')
    return scat, food_scat, pheromone_im, frame_text, nest_scat

ant_patch = mpatches.Patch(color='red', label='Ants')
food_patch = mpatches.Patch(color='green', label='Food')
nest_patch = mpatches.Patch(color='blue', label='Nest')
pheromone_patch = mpatches.Patch(color='gray', label='Pheromone')

ax.legend(handles=[ant_patch, food_patch, nest_patch, pheromone_patch], loc='upper left', bbox_to_anchor=(1, 1))

ani = animation.FuncAnimation(fig, update, frames=range(num_steps), interval=100, blit=True, repeat=True)
plt.show()
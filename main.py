#
# Parameters that i want to give to the user to tweak the simulation
# From Environment class
# 1. pheromone_decay_factor = 
# From Ant class
# 1. drop_pheromone (value)
#    self.environment.pheromone_grid[self.x, self.y] += value * distance_to_nest
# 2. decrement_pheromone_if_overlap (value)
#    self.environment.pheromone_grid[self.x, self.y] = max(0, self.environment.pheromone_grid[self.x, self.y] - (num_ants_at_position * value))
# 3. amount of worker per scouter Ants (you can have total of 30 ants and the user choose how many will be workers and how many will be)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
from models.ant import Ant
from models.environment import Environment
import time

num_ants = 20
width = 100
height = 100
num_of_food = 20
num_steps = 1600

environment = Environment(width=width, height=height, num_of_food=num_of_food)
ants = [Ant(environment) for _ in range(num_ants)]

fig, ax = plt.subplots(figsize=(12, 12))
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
nest_food_text = ax.text(0.02, 0.90, "", transform=ax.transAxes)
timer_text = ax.text(0.02, 0.85, '', transform=ax.transAxes, color='white')

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
    frame_text.set_color('white')
    nest_food_text.set_text(f'Food: {environment.localnest.food_count}')
    nest_food_text.set_color('white')
    elapsed_time = time.time() - start_time
    timer_text.set_text(f'Timer: {elapsed_time:.2f} s')

    return scat, food_scat, pheromone_im, frame_text, nest_scat,nest_food_text,timer_text

# Add start button at the bottom center
start_ax = plt.axes([0.45, 0.01, 0.1, 0.075])  # Centered at the bottom
start_button = Button(start_ax, 'Start')

# Define the callback function for the button
def start(event):
    global ani, start_time
    start_time = time.time()
    ani = animation.FuncAnimation(fig, update, frames=range(num_steps), interval=100, blit=True, repeat=False)
    plt.draw()
    start_button.ax.set_visible(False) 
    

# Connect the button to the callback function
start_button.on_clicked(start)


ant_patch = mpatches.Patch(color='red', label='Ants')
food_patch = mpatches.Patch(color='green', label='Food')
nest_patch = mpatches.Patch(color='blue', label='Nest')
pheromone_patch = mpatches.Patch(color='gray', label='Pheromone')

ax.legend(handles=[ant_patch, food_patch, nest_patch, pheromone_patch], loc='upper left', bbox_to_anchor=(1, 1))

def close_fig(event):
    print("close event")
    plt.close('all')

#ani = animation.FuncAnimation(fig, update, frames=range(num_steps), interval=100, blit=True, repeat=False)
#ani.event_source.stop() 
#fig.canvas.mpl_connect('close_event', close_fig)
plt.show()
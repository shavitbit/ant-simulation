import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button, Slider,TextBox
from models.scout import Scout
from models.worker import Worker
from models.environment import Environment
import time

# Initial default parameters
num_ants = 30
width = 100
height = 100
num_of_food = 20
num_steps = 1600
pheromone_decay_factor = 1.5
drop_pheromone_value = 1
worker_to_scout_ratio = 5
decrement_pheromone_if_overlap_value = 20

# Create the plot for the settings menu
fig, ax = plt.subplots(figsize=(12, 12))
plt.subplots_adjust(left=0.25, bottom=0.4)
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_title('Ant Simulator Settings')
# Create sliders for parameters
ax_decrement_pheromone_if_overlap_value = plt.axes([0.25, 0.3, 0.65, 0.03])
slider_decrement_pheromone_if_overlap_value = Slider(ax_decrement_pheromone_if_overlap_value, 'Decrement pheromone if overlap', 0, 100, valinit=decrement_pheromone_if_overlap_value)

ax_pheromone_decay = plt.axes([0.25, 0.25, 0.65, 0.03])
slider_pheromone_decay = Slider(ax_pheromone_decay, 'Pheromone Decay', 0.0, 150, valinit=pheromone_decay_factor, valstep=0.5)

ax_drop_pheromone = plt.axes([0.25, 0.2, 0.65, 0.03])
slider_drop_pheromone = Slider(ax_drop_pheromone, 'Drop Pheromone', 0.5, 100.0, valinit=drop_pheromone_value, valstep=0.5)

ax_worker_scout_ratio = plt.axes([0.25, 0.15, 0.65, 0.03])
slider_worker_scout_ratio = Slider(ax_worker_scout_ratio, 'Worker/Scout Ratio', 1, 30, valinit=worker_to_scout_ratio, valstep=1)

# Add buttons
start_ax = plt.axes([0.45, 0.01, 0.1, 0.05])
start_button = Button(start_ax, 'Start')

help_ax = plt.axes([0.85, 0.95, 0.1, 0.05])
help_button = Button(help_ax, 'Help')

# Function to show help dialog
def show_help(event):
    plt.figure("Ant Simulation Help",figsize=(13,8))
    plt.text(0.01, 0.1, "'Ant simulation' simulates the behavior of ants to find the fastest way\n\
to collect food using a combination 4 parameters and in 1600 steps.\n\n\
Decrement Pheromone If Overlap:\nThe function is designed to manage the pheromone levels in the simulation environment.\n\
When too many ants are in the same place, it reduces the pheromone concentration at that spot.\n\
This helps to prevent the pheromone trail from becoming too strong and encourages ants \n\
to explore other paths, promoting more realistic foraging behavior.\n\
max(0, pheromone_grid[x,y] - (num_ants_at_position * decrement_pheromone_if_overlap_value) \n\n\
Pheromone Decay:\nAllows you to adjust the rate at which pheromone trails left by the ants dissipate over time. \n\
Pheromone decay is a crucial aspect of ant behavior simulation as it controls how long the pheromone scent\nremains effective in guiding other ants towards food sources.\n\
max(0, pheromone_grid - pheromone_decay_value)\n\n\
Drop Pheromone:\n\
Allows you to adjust the amount of pheromone that each ant deposits on the ground as it moves.\n\
Pheromone deposition is a key mechanism in ant behavior simulations,\n\
as it influences how other ants navigate and make decisions. Only ants with food can drop pheromone.\n\
pheromone_grid[x,y] += distance_to_nest * drop_pheromone_value\n\n\
Worker Scout Ratio:\n\
Allows you to adjust the proportion of worker ants to scout ants in the simulation.\n\
This ratio influences the behavior and efficiency of the ant colony, as workers and scouts have different roles.\n\
Workers are primarily responsible for collecting food and returning it to the nest.\n\
They have a better sensing radius and are ready at the nest to follow the pheromone trails.\n\
Scouts are responsible for exploring the environment and laying down pheromone trails to guide workers\nand other scouts to food sources.\n\
You have 30 ants, so if you choose 5 on the slider, that means you will spawn 5 workers and 25 scouts.",
             fontsize=12)
    plt.axis('off')
    plt.show()

help_button.on_clicked(show_help)


# Initialize the environment and ants
def initialize_simulation():
    global environment, ants, ani, start_time, scout_scat, worker_scat
    decrement_pheromone_if_overlap = int(slider_decrement_pheromone_if_overlap_value.val)
    
    pheromone_decay_factor = slider_pheromone_decay.val
    drop_pheromone_value = slider_drop_pheromone.val
    worker_to_scout_ratio = int(slider_worker_scout_ratio.val)

    environment = Environment(width=width, height=height, num_of_food=num_of_food, pheromone_decay_factor=pheromone_decay_factor)
    ants = [Scout(environment, drop_pheromone_value) for _ in range(num_ants - worker_to_scout_ratio)] + \
           [Worker(environment, drop_pheromone_value) for _ in range(worker_to_scout_ratio)]
    
    # Update plot settings
    ax.clear()
    slider_decrement_pheromone_if_overlap_value.active = False
    #slider_decrement_pheromone_if_overlap_value.ax.set_visible(False)
    start_button.ax.set_visible(False)
    slider_pheromone_decay.active = False
    slider_drop_pheromone.active = False
    slider_worker_scout_ratio.active = False
    start_button.set_active(False)
    plt.axes([0.25, 0.25, 0.65, 0.03]).set_visible(False)
    ax.set_xlim(0, environment.width)
    ax.set_ylim(0, environment.height)
    ax.set_title("Simulation ID: " + str(float(slider_decrement_pheromone_if_overlap_value.val))+"-" \
                 + str(float(slider_pheromone_decay.val))+"-" + str(float(slider_drop_pheromone.val))+"-"\
                    + str(float(slider_worker_scout_ratio.val)) )
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    fig.canvas.manager.set_window_title('Ant Simulator')

    global food_scat, pheromone_im, frame_text, nest_scat, nest_food_text, timer_text
    scout_scat = ax.scatter([], [], c='red', s=10, label='Scouts')
    worker_scat = ax.scatter([], [], c='yellow', s=20, label='Workers')
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
            ant.decrement_pheromone_if_overlap(ant_positions, int(decrement_pheromone_if_overlap))
            
        environment.pheromone_decay()

        scout_positions = [(ant.x, ant.y) for ant in ants if isinstance(ant, Scout)]
        worker_positions = [(ant.x, ant.y) for ant in ants if isinstance(ant, Worker)]
        scout_scat.set_offsets(scout_positions)
        worker_scat.set_offsets(worker_positions)

        food_positions = np.argwhere(environment.environment > 0)
        food_scat.set_offsets(food_positions)

        pheromone_im.set_array(environment.pheromone_grid)

        frame_text.set_text(f'Frame: {frame}')
        frame_text.set_color('white')
        nest_food_text.set_text(f'Food: {environment.localnest.food_count}')
        nest_food_text.set_color('white')
        elapsed_time = time.time() - start_time
        timer_text.set_text(f'Timer: {int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}')

        return scout_scat, worker_scat, food_scat, pheromone_im, frame_text, nest_scat, nest_food_text, timer_text

    # Start animation
    start_time = time.time()
    ani = animation.FuncAnimation(fig, update, frames=range(num_steps), interval=100, blit=True, repeat=False)
    plt.draw()

# Connect the start button to initialize_simulation function
start_button.on_clicked(lambda event: initialize_simulation())

plt.show()
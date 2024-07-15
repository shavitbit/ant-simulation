import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button, Slider
from models.scout import Scout
from models.worker import Worker
from models.environment import Environment
import time

# Initial default parameters
num_ants = 30
scout_ants = 0
worker_ants = 0

width = 100
height = 100
num_of_food = 20
num_steps = 1600
pheromone_decay_factor = 1.5
drop_pheromone_value = 1
worker_to_scout_ratio = 0
decrement_pheromone_if_overlap_value = 20

# Create the plot for the settings menu
fig, ax = plt.subplots(figsize=(12, 12))
plt.subplots_adjust(left=0.25, bottom=0.4)
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_title('Ant Simulator Settings')

# Add sliders for parameters
ax_decrement_pheromone_if_overlap_value = plt.axes([0.25, 0.3, 0.65, 0.03])
slider_decrement_pheromone_if_overlap_value = Slider(ax_decrement_pheromone_if_overlap_value, 'Decrement pheromone if overlap', 0, 100, valinit=decrement_pheromone_if_overlap_value)

ax_pheromone_decay = plt.axes([0.25, 0.25, 0.65, 0.03])
slider_pheromone_decay = Slider(ax_pheromone_decay, 'Pheromone Decay', 0.01, 10.0, valinit=pheromone_decay_factor)

ax_drop_pheromone = plt.axes([0.25, 0.2, 0.65, 0.03])
slider_drop_pheromone = Slider(ax_drop_pheromone, 'Drop Pheromone', 0.1, 100.0, valinit=drop_pheromone_value)

ax_worker_scout_ratio = plt.axes([0.25, 0.15, 0.65, 0.03])
slider_worker_scout_ratio = Slider(ax_worker_scout_ratio, 'Worker/Scout Ratio', 1, 30, valinit=worker_to_scout_ratio, valstep=1)

# Add start button
start_ax = plt.axes([0.45, 0.01, 0.1, 0.05])
start_button = Button(start_ax, 'Start')

# Create invisible rectangles for tooltip detection
tooltip_texts = {
    'decrement': 'Controls the decrement value for pheromone when ants overlap.',
    'decay': 'Sets the rate of pheromone decay.',
    'drop': 'Specifies the amount of pheromone dropped by ants.',
    'ratio': 'Determines the ratio of workers to scouts.',
    'start': 'Starts the simulation.'
}

tooltip_rects = {
    'decrement': ax_decrement_pheromone_if_overlap_value.bbox,
    'decay': ax_pheromone_decay.bbox,
    'drop': ax_drop_pheromone.bbox,
    'ratio': ax_worker_scout_ratio.bbox,
    'start': start_ax.bbox
}

tooltip_annotation = ax.annotate(
    '', xy=(0, 0), xytext=(10, 10), textcoords='offset points',
    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
    arrowprops=dict(arrowstyle='->')
)
tooltip_annotation.set_visible(False)

def on_move(event):
    visibility_changed = False
    for key, rect in tooltip_rects.items():
        if rect.contains(event.x, event.y):
            tooltip_annotation.xy = (event.x, event.y)
            tooltip_annotation.set_text(tooltip_texts[key])
            tooltip_annotation.set_visible(True)
            visibility_changed = True
            break
    if not visibility_changed:
        tooltip_annotation.set_visible(False)
    fig.canvas.draw_idle()

fig.canvas.mpl_connect('motion_notify_event', on_move)

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
    ax.set_xlim(0, environment.width)
    ax.set_ylim(0, environment.height)
    ax.set_title('Ant Simulator')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    fig.canvas.manager.set_window_title('Ant Simulator')

    global food_scat, pheromone_im, frame_text, nest_scat, nest_food_text, timer_text
    scout_scat = ax.scatter([], [], c='red', s=10, label='Scouts')
    worker_scat = ax.scatter([], [], c='blue', s=10, label='Workers')
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
        timer_text.set_text(f'Timer: {int(elapsed_time // 60):02}:{int(elapsed_time % 60):02} min')

        return scout_scat, worker_scat, food_scat, pheromone_im, frame_text, nest_scat, nest_food_text, timer_text

    # Start animation
    start_time = time.time()
    ani = animation.FuncAnimation(fig, update, frames=range(num_steps), interval=100, blit=True, repeat=False)
    plt.draw()

# Connect the start button to initialize_simulation function
start_button.on_clicked(lambda event: initialize_simulation())

plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # Necessary for 3D plotting
from matplotlib.widgets import Slider, Button

# Boid class
class Boid:
    def __init__(self, position, velocity):
        self.position = position  # 3D position
        self.velocity = velocity  # 3D velocity

def update_boids(boids, params):
    positions = np.array([boid.position for boid in boids])
    velocities = np.array([boid.velocity for boid in boids])

    for i, boid in enumerate(boids):
        # Find neighbors within perception radius
        diffs = positions - boid.position
        distances = np.linalg.norm(diffs, axis=1)
        neighbors_mask = (distances > 0) & (distances < params['perception_radius'])
        neighbors = positions[neighbors_mask]
        neighbor_velocities = velocities[neighbors_mask]

        # Initialize steering vectors
        separation = np.zeros(3)
        alignment = np.zeros(3)
        cohesion = np.zeros(3)

        if len(neighbors) > 0:
            # Separation
            separation_vectors = boid.position - neighbors
            separation = np.sum(separation_vectors / distances[neighbors_mask][:, np.newaxis], axis=0)
            separation *= params['separation_weight']

            # Alignment
            avg_velocity = np.mean(neighbor_velocities, axis=0)
            alignment = (avg_velocity - boid.velocity) * params['alignment_weight']

            # Cohesion
            center_of_mass = np.mean(neighbors, axis=0)
            cohesion = (center_of_mass - boid.position) * params['cohesion_weight']

        # Combine steering forces
        boid.velocity += separation + alignment + cohesion

        # Limit speed
        speed = np.linalg.norm(boid.velocity)
        if speed > params['max_speed']:
            boid.velocity = (boid.velocity / speed) * params['max_speed']

        # Update position
        boid.position += boid.velocity

        # Boundary conditions (wrap around)
        boid.position = np.mod(boid.position + params['space_size'], 2 * params['space_size']) - params['space_size']

def animate(i):
    update_boids(boids, params)
    positions = np.array([boid.position for boid in boids])

    scat._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])
    return scat,

def start_simulation(event):
    global params, boids, ani

    # Read parameters from sliders
    params['num_boids'] = int(num_boids_slider.val)
    params['separation_weight'] = separation_slider.val
    params['alignment_weight'] = alignment_slider.val
    params['cohesion_weight'] = cohesion_slider.val
    params['perception_radius'] = perception_slider.val
    params['max_speed'] = max_speed_slider.val

    # Initialize boids
    boids = []
    for _ in range(params['num_boids']):
        position = np.random.uniform(-params['space_size'], params['space_size'], 3)
        velocity = np.random.uniform(-1, 1, 3)
        boids.append(Boid(position, velocity))

    # Reset animation
    ani.event_source.stop()
    ani.event_source.start()

# Parameters
params = {
    'num_boids': 100,
    'separation_weight': 1.5,
    'alignment_weight': 1.0,
    'cohesion_weight': 1.0,
    'perception_radius': 25.0,
    'max_speed': 2.0,
    'space_size': 100.0,
}

# Initialize boids
boids = []
for _ in range(params['num_boids']):
    position = np.random.uniform(-params['space_size'], params['space_size'], 3)
    velocity = np.random.uniform(-1, 1, 3)
    boids.append(Boid(position, velocity))

# Set up plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-params['space_size'], params['space_size'])
ax.set_ylim(-params['space_size'], params['space_size'])
ax.set_zlim(-params['space_size'], params['space_size'])
ax.set_title('3D Starling Flock Simulation')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Plot initial positions
positions = np.array([boid.position for boid in boids])
scat = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='black', s=30)

# Sliders for parameters
axcolor = 'lightgoldenrodyellow'
ax_num_boids = plt.axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor)
ax_separation = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_alignment = plt.axes([0.15, 0.09, 0.65, 0.03], facecolor=axcolor)
ax_cohesion = plt.axes([0.15, 0.13, 0.65, 0.03], facecolor=axcolor)
ax_perception = plt.axes([0.15, 0.17, 0.65, 0.03], facecolor=axcolor)
ax_max_speed = plt.axes([0.15, 0.21, 0.65, 0.03], facecolor=axcolor)

num_boids_slider = Slider(ax_num_boids, 'Number of Birds', 10, 500, valinit=params['num_boids'], valstep=10)
separation_slider = Slider(ax_separation, 'Separation Weight', 0.0, 5.0, valinit=params['separation_weight'], valstep=0.1)
alignment_slider = Slider(ax_alignment, 'Alignment Weight', 0.0, 5.0, valinit=params['alignment_weight'], valstep=0.1)
cohesion_slider = Slider(ax_cohesion, 'Cohesion Weight', 0.0, 5.0, valinit=params['cohesion_weight'], valstep=0.1)
perception_slider = Slider(ax_perception, 'Perception Radius', 5.0, 100.0, valinit=params['perception_radius'], valstep=5.0)
max_speed_slider = Slider(ax_max_speed, 'Max Speed', 0.1, 10.0, valinit=params['max_speed'], valstep=0.1)

# Start button
ax_start = plt.axes([0.8, 0.25, 0.1, 0.04])
start_button = Button(ax_start, 'Start', color=axcolor, hovercolor='0.975')

start_button.on_clicked(start_simulation)

# Animation
ani = FuncAnimation(fig, animate, interval=50, blit=False)

plt.show()

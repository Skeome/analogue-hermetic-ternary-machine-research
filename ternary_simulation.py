import matplotlib
matplotlib.use('TkAgg') # Use TkAgg backend for GUI display
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from config import SIMULATION_PARAMS
import os # Import os module for path operations

def simulate_ternary_machine(params):
    """
    Simulates the ternary machine's state evolution.

    Args:
        params (dict): A dictionary containing simulation parameters:
            - N_DIMENSIONS (int): Dimensionality of the state space.
            - initial_salt_state (np.array): Starting state of Salt.
            - sulfur_vector (np.array): Target state of Sulfur.
            - mercury_matrix (np.array): Tuning matrix for Mercury.
            - num_ticks (int): Number of simulation steps.
            - learning_rate (float): How quickly Salt adjusts towards Sulfur.
            - noise_level (float): Random environmental noise.

    Returns:
        np.array: A NumPy array containing the history of the Salt vector's trajectory.
    """
    N_DIMENSIONS = params['N_DIMENSIONS']
    initial_salt_state = params['initial_salt_state']
    sulfur_vector = params['sulfur_vector']
    mercury_matrix = params['mercury_matrix']
    num_ticks = params['num_ticks']
    learning_rate = params['learning_rate']
    noise_level = params['noise_level']

    salt_vector = initial_salt_state.copy()
    history = [salt_vector.tolist()]

    for tick in range(num_ticks):
        difference_vector = sulfur_vector - salt_vector
        force_vector = np.dot(mercury_matrix, difference_vector)

        noise = np.random.normal(0, noise_level, size=N_DIMENSIONS)
        force_vector += noise

        salt_vector += learning_rate * force_vector
        history.append(salt_vector.tolist())

    return np.array(history)

def visualize_simulation(history_np, params, save_animation_path=None):
    """
    Visualizes the ternary machine simulation results.

    Args:
        history_np (np.array): The trajectory history of the Salt vector.
        params (dict): A dictionary containing simulation parameters for visualization:
            - sulfur_vector (np.array): Target state of Sulfur.
            - mercury_matrix (np.array): Tuning matrix for Mercury.
        save_animation_path (str, optional): Path to save the animation. If None, plot is only shown.
    """
    sulfur_vector = params['sulfur_vector']
    mercury_matrix = params['mercury_matrix']

    plt.style.use('dark_background')
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    def generate_probability_cloud_data(center, num_points=500, spread=3.0):
        x = np.random.normal(center[0], spread, num_points)
        y = np.random.normal(center[1], spread, num_points)
        z = np.random.normal(center[2], spread, num_points)
        return x, y, z

    cloud_x, cloud_y, cloud_z = generate_probability_cloud_data(sulfur_vector, num_points=1000, spread=3.0)
    ax.scatter(cloud_x, cloud_y, cloud_z, c='#22d3ee', alpha=0.05, label='Probability Cloud')

    ax.scatter(sulfur_vector[0], sulfur_vector[1], sulfur_vector[2], c='#f472b6', marker='D', s=100, label='Sulfur (Intent/Target)')

    line, = ax.plot([], [], [], lw=2, c='#22d3ee', label='Salt (Trajectory)')
    point, = ax.plot([], [], [], 'o', c='#22d3ee')

    all_points = np.vstack([history_np, [sulfur_vector]])
    min_vals = all_points.min(axis=0) - 2
    max_vals = all_points.max(axis=0) + 2
    ax.set_xlim(min_vals[0], max_vals[0])
    ax.set_ylim(min_vals[1], max_vals[1])
    ax.set_zlim(min_vals[2], max_vals[2])

    grid_density = 2.5
    x_grid, y_grid, z_grid = np.meshgrid(np.arange(min_vals[0], max_vals[0], grid_density),
                                         np.arange(min_vals[1], max_vals[1], grid_density),
                                         np.arange(min_vals[2], max_vals[2], grid_density))
    u = sulfur_vector[0] - x_grid
    v = sulfur_vector[1] - y_grid
    w = sulfur_vector[2] - z_grid
    vectors = np.vstack([u.ravel(), v.ravel(), w.ravel()])
    transformed_vectors = mercury_matrix @ vectors
    u_transformed = transformed_vectors[0, :].reshape(u.shape)
    v_transformed = transformed_vectors[1, :].reshape(v.shape)
    w_transformed = transformed_vectors[2, :].reshape(w.shape)
    ax.quiver(x_grid, y_grid, z_grid, u_transformed, v_transformed, w_transformed,
              length=0.8, normalize=True, color='#a78bfa', alpha=0.4)
    mercury_legend_artist = Line2D([], [], color='#a78bfa', lw=2, label='Mercury (Medium)')

    ax.set_xlabel('Dimension 1 (Physical)')
    ax.set_ylabel('Dimension 2 (Ethereal)')
    ax.set_zlabel('Dimension 3 (Spiritual)')
    ax.set_title('Ternary Machine Simulation')
    ax.set_facecolor('#0f172a')
    fig.set_facecolor('#1e293b')

    def update(frame):
        line.set_data(history_np[:frame, 0], history_np[:frame, 1])
        line.set_3d_properties(history_np[:frame, 2])
        point.set_data(history_np[frame, 0:1], history_np[frame, 1:2])
        point.set_3d_properties(history_np[frame, 2:3])
        return line, point

    ani = FuncAnimation(fig, update, frames=len(history_np), blit=False, interval=50)

    handles, labels = ax.get_legend_handles_labels()
    handles.append(mercury_legend_artist)
    ax.legend(handles=handles)

    if save_animation_path:
        os.makedirs(os.path.dirname(save_animation_path), exist_ok=True)
        ani.save(save_animation_path, writer='pillow', fps=15)
        print(f"Simulation animation saved to {save_animation_path}")
    
    print("Starting real-time simulation window...")
    plt.show()
    print("Simulation window closed.")

def save_simulation_results(history_np, output_dir="output", filename="simulation_history.csv"):
    """
    Saves the simulation history to a CSV file.

    Args:
        history_np (np.array): The trajectory history of the Salt vector.
        output_dir (str): Directory to save the file.
        filename (str): Name of the CSV file.
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    np.savetxt(filepath, history_np, delimiter=",", header="Dim1,Dim2,Dim3", comments="")
    print(f"Simulation results saved to {filepath}")

def main():
    # Run simulation
    history = simulate_ternary_machine(SIMULATION_PARAMS)

    # Save results
    save_simulation_results(history)

    # By default, the script now saves the animation and does not show the plot window.
    # To show the plot window instead, call visualize_simulation without the save_animation_path argument.
    visualize_simulation(history, SIMULATION_PARAMS, save_animation_path="output/simulation_animation.gif")
    
if __name__ == "__main__":
    main()
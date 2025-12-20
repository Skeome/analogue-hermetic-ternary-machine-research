import numpy as np

# Simulation parameters for the Ternary Machine
SIMULATION_PARAMS = {
    'N_DIMENSIONS': 3,
    # Initial state of the "Salt" (current state of the witness/system)
    # Starting somewhere in the middle
    'initial_salt_state': np.array([0.0, 0.0, 0.0]),
    # Target state of the "Sulfur" (the intent or desired outcome)
    # A specific point in our N-dimensional space
    'sulfur_vector': np.array([5.0, 7.0, 3.0]),
    # The "Mercury" processor (tuning matrix)
    # Modulates the force/direction towards the target.
    # Can introduce biases or amplify certain dimensions.
    # For now, a slightly biased identity matrix.
    'mercury_matrix': np.array([
        [1.1, 0.0, 0.0],
        [0.0, 0.9, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    # Simulation parameters
    'num_ticks': 200,  # Number of simulation steps
    'learning_rate': 0.05,  # How quickly the Salt state adjusts towards Sulfur
    'noise_level': 0.01  # Random environmental noise introduced at each step
}

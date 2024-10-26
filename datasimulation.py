import pandas as pd
import random

def generate_sensor_data():
    """Generates synthetic data for the sensors with variance."""
    # Generate a synthetic load value (e.g., -100 to 1000 grams)
    load_value = random.randint(-100, 1000)
    
    # Generate tilt status (0 for normal, 1 for tilted)
    tilt_status = random.randint(0, 1)
    
    # Generate a synthetic distance measurement (e.g., 0 to 400 cm)
    distance = random.uniform(0, 400)
    
    return load_value, tilt_status, distance

def generate_training_data(num_samples=100000):
    """Generates a dataset for training with varied critical conditions."""
    data = []
    
    for _ in range(num_samples):
        load_value, tilt_status, distance = generate_sensor_data()
        
        # Define a critical condition based on more nuanced criteria
        # Introduce variability in critical conditions
        if (load_value > 600 and distance < 200) or (tilt_status == 1 and load_value > 300) or (distance < 50 and load_value > 400):
            label = 1  # Critical condition
        else:
            label = 0  # Normal condition
        
        # Introduce random noise to distance for realism
        noise = random.uniform(-5, 5)  # Adding noise in the range of -5 to 5 cm
        distance += noise
        
        # Ensuring distance stays within realistic bounds
        distance = max(0, min(400, distance))
        
        data.append([load_value, tilt_status, distance, label])
    
    # Create a DataFrame
    df = pd.DataFrame(data, columns=['load_value', 'tilt_status', 'distance', 'label'])
    return df

# Example usage
training_data = generate_training_data(1000)
training_data.to_csv("sensor_training_data.csv", index=False)

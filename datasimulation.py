import pandas as pd
import random
import datetime

def generate_sensor_data(timestamp):
    """Generates synthetic data for the sensors with variance."""
    # Generate a synthetic load value (e.g., -100 to 1000 grams)
    load_value = random.randint(-100, 1000)
    
    # Generate tilt status as a continuous value between 0 and 1
    tilt_status = random.uniform(0, 1)  # Continuous tilt between 0 and 1
    
    # Generate a synthetic distance measurement (e.g., 0 to 400 cm)
    distance = random.uniform(0, 400)
    
    # Introduce random noise to load_value
    load_noise = random.uniform(-10, 10)  # Adding noise in the range of -10 to 10 grams
    load_value += load_noise
    
    # Ensure load_value stays within realistic bounds
    load_value = max(-100, min(1000, load_value))
    
    # Introduce random noise to distance for realism
    distance_noise = random.uniform(-5, 5)  # Adding noise in the range of -5 to 5 cm
    distance += distance_noise
    
    # Ensuring distance stays within realistic bounds
    distance = max(0, min(400, distance))
    
    return load_value, tilt_status, distance

def generate_training_data(num_samples=50000):
    """Generates a dataset for training with varied critical conditions and timestamps, backwards in time."""
    data = []
    
    # Start the timestamp from the current time and decrement by minute
    timestamp = datetime.datetime.now()  # Starting timestamp
    
    for _ in range(num_samples):
        load_value, tilt_status, distance = generate_sensor_data(timestamp)
        
        # Randomly set thresholds for critical conditions
        load_threshold = random.randint(300, 700)  # Random threshold for load_value
        distance_threshold = random.uniform(0, 250)  # Random threshold for distance
        
        # Define critical conditions with variability
        critical_condition = False
        if (load_value > load_threshold and distance < distance_threshold) or \
           (tilt_status > 0.5 and load_value > load_threshold / 2) or \
           (distance < 50 and load_value > load_threshold / 1.5):
            critical_condition = True
            
        # Assign label based on critical condition
        label = 1 if critical_condition else 0
        
        # Introduce random noise to labels to simulate errors
        if random.random() < 0.05:  # 5% chance to flip the label
            label = 1 - label
            
        # Add timestamp to the data
        data.append([timestamp, load_value, tilt_status, distance, label])
        
        # Decrement the timestamp by one minute for each entry
        timestamp -= datetime.timedelta(minutes=1)
    
    # Create a DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'load_value', 'tilt_status', 'distance', 'label'])
    return df

# Example usage
training_data = generate_training_data()  # Generates data for one week with 1-minute intervals
training_data.to_csv("sensor_testing_data.csv", index=False)

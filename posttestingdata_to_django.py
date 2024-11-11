import pandas as pd
import requests
import datetime

# Define your Django API endpoint
DJANGO_API_ENDPOINT = "http://localhost:8000/apis/pothole-data/"  # Update if needed

def post_data(row):
    """Post a row of data to the Django API endpoint."""
    data = {
        "timestamp": row['timestamp'],
        "load_value": row['load_value'],
        "tilt_status": row['tilt_status'],
        "distance": row['distance'],
        "label": row['label']
    }
    
    try:
        response = requests.post(DJANGO_API_ENDPOINT, json=data)
        if response.status_code == 201:
            print(f"Data posted successfully: {data}")
        else:
            print(f"Failed to post data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error posting data: {e}")

# Load generated sensor data from CSV file
training_data = pd.read_csv("sensor_testing_data.csv")

# Convert timestamp column to ISO 8601 format if it's not already
training_data['timestamp'] = pd.to_datetime(training_data['timestamp']).apply(lambda x: x.isoformat())

# Iterate through each row and post it to the endpoint
for index, row in training_data.iterrows():
    post_data(row)

import numpy as np
import pandas as pd
import tensorflow as tf  # TensorFlow for TFLite interpreter
from datetime import datetime

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="my_model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the test data (replace this with your actual data loading)
test_data = pd.read_csv("sensor_testing_data.csv", parse_dates=['timestamp'])
print(len(test_data))

# Sort data by timestamp to maintain chronological order
test_data = test_data.sort_values(by='timestamp')

# Get user input for the date range
start_date_str = input("Enter the start date (YYYY-MM-DD): ")
end_date_str = input("Enter the end date (YYYY-MM-DD): ")

# Convert user input to datetime objects
try:
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    exit()

# Filter data within the specified time range
time_range_df = test_data[(test_data['timestamp'] >= start_date) & (test_data['timestamp'] <= end_date)]

# Ensure the time range has enough data points for the sequence length
sequence_length = 1440  # 1 day of data (adjust as needed)
if len(time_range_df) < sequence_length:
    print(f"Not enough data points in the specified range ({len(time_range_df)} available).")
    exit()

# Take the last sequence_length data points for prediction
sequence = time_range_df[['load_value', 'tilt_status', 'distance']].iloc[-sequence_length:].values
sequence = np.expand_dims(sequence, axis=0).astype(np.float32)  # Add batch dimension and ensure type is float32

# Set the input tensor for the interpreter
interpreter.set_tensor(input_details[0]['index'], sequence)

# Run inference
interpreter.invoke()

# Get the prediction result
prediction = interpreter.get_tensor(output_details[0]['index'])
prediction = (prediction > 0.5).astype("int32")

# Output the prediction with descriptive status
status = "Critical" if prediction[0][0] == 1 else "Normal"
print(f"Prediction for the period from {start_date_str} to {end_date_str}: {status}")

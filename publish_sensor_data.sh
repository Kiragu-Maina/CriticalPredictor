#!/bin/bash

# Define MQTT broker address and topic
MQTT_BROKER="localhost"  # Update if the broker is on a different host
TOPIC="sensor/data"

# Function to publish a simulated sensor data message
publish_data() {
    load_value=$(awk -v min=100 -v max=900 'BEGIN{srand(); print min+rand()*(max-min)}')
    tilt_status=$(awk -v min=0 -v max=1 'BEGIN{srand(); print min+rand()*(max-min)}')
    distance=$(awk -v min=0 -v max=500 'BEGIN{srand(); print min+rand()*(max-min)}')
    
    # Format the message
    message="$load_value,$tilt_status,$distance"
    
    # Publish to MQTT topic
    mosquitto_pub -h "$MQTT_BROKER" -t "$TOPIC" -m "$message"
    echo "Published: $message"
}

# Publish 10 simulated sensor data messages
for i in {1..10}
do
    publish_data
    sleep 1  # Pause for a second between messages
done

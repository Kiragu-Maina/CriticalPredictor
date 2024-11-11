import pickle
import numpy as np
import paho.mqtt.client as mqtt
import requests
from datetime import datetime

# MQTT setup
MQTT_BROKER = "localhost"  # Change to your broker address if needed
TOPIC_SENSOR_DATA = "sensor/data"
TOPIC_ALERT_ACTIONS = "sensor/alerts"

# Django API endpoint
DJANGO_API_ENDPOINT = "http://localhost:8000/apis/pothole-data/"  # Adjust the URL as needed

def publish_mqtt(client, topic, message):
    """Publish a message to an MQTT topic."""
    client.publish(topic, message)
    print(f"Published to {topic}: {message}")

def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to the topics you need to listen to
    client.subscribe([(TOPIC_SENSOR_DATA, 0), (TOPIC_ALERT_ACTIONS, 0)])

def on_message(client, userdata, msg):
    """Callback when a message is received from MQTT"""
    try:
        if msg.topic == TOPIC_SENSOR_DATA:
            # Decode and split the received sensor data message
            load_value, tilt_status, distance = map(float, msg.payload.decode().split(","))
            process_sensor_data(load_value, int(tilt_status), distance)
        elif msg.topic == TOPIC_ALERT_ACTIONS:
            # Handle alert actions
            action = msg.payload.decode()
            if action == "sound_siren":
                print("Triggering siren via MQTT")
            elif action.startswith("send_sms"):
                message = action.split(":", 1)[1]  # Extract message after 'send_sms:'
                print(f"Sending SMS notification via MQTT: {message}")
            else:
                print("Received unrecognized action")
    except Exception as e:
        print(f"Failed to process MQTT message: {e}")

def process_sensor_data(load_value, tilt_status, distance):
    """Process and send sensor data to Django API with timestamp"""
    data = {
        "timestamp": datetime.now().isoformat(),
        "load_value": load_value,
        "tilt_status": tilt_status,
        "distance": distance,
        "label": 1 if load_value > 500 else 0  # Example logic for label classification
    }
    
    try:
        response = requests.post(DJANGO_API_ENDPOINT, json=data)
        if response.status_code == 201:
            print(f"Data successfully posted to API: {data}")
        else:
            print(f"Failed to post data to API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error posting data to API: {e}")

# MQTT client setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_forever()

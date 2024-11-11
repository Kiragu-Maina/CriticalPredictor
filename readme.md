# Dam Condition Prediction Model

The model in this repository is created by feeding simulated sensor data present in the repository. The data contains simulated values of load, tilt status, and ultrasonic distance (representing water level).

## How the Model Learns

### Data-Driven Learning
The model utilizes the training data generated, which consists of combinations of load values, tilt statuses, and distances along with their corresponding labels. It learns to associate specific feature values with each label, distinguishing between critical conditions and normal conditions.

### Feature Importance
This model is based on the Random Forest algorithm, which creates multiple decision trees from random subsets of the training data. Each tree makes predictions based on the rules it has learned. Through this process, the model identifies patterns such as:
- A load value of 400 with a tilt status of 0 is considered safe.
- A load value of 600 with a tilt status of 0 indicates a critical condition.
- A load value of 300 with a tilt status of 1 is critical, regardless of the distance.

    The data for training is generated using `datasimulation.py`, which incorporates critical conditions based on the following logic:
    ```python
    if (load_value > 600 and distance < 200) or (tilt_status == 1 and load_value > 300) or (distance < 50 and load_value > 400):

### Complex Interactions
The model does not rely solely on fixed thresholds for decision-making. Instead, it learns from interactions between features. For instance, it might find that a low load combined with a tilt condition is more critical than a higher load with no tilt, depending on the training data it analyzes.

## Using the Model

Once trained, this model can be used to predict whether the dam is in a critical condition based on new sensor readings.

### Testing the Model
To test the model, modify the values of load, tilt, and distance in the `testthemodel.py` file. 

- A prediction of **1** indicates that the dam is in a **critical condition**.
- A prediction of **0** indicates that the dam is **not in a critical condition**.

## Getting Started


1. Clone this repository.
2. Create and activate the Python environment:
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt

4. Use the testthemodel.py script to test predictions
   ```bash
   python testthemodel.py


# MQTT-Based Sensor Monitoring System

This project monitors simulated sensor data using an MQTT broker. Sensor data is published to MQTT topics, and actions such as sending SMS notifications or activating alarms can be triggered based on model predictions.

## Features

- **Sensor Data Publishing**: Publishes simulated sensor data (load sensor, tilt sensor, and ultrasonic distance) to an MQTT topic.
- **Alert System**: Processes sensor data using a pre-trained machine learning model and publishes alerts to an MQTT topic when an abnormal condition is detected.
- **Subscriber Actions**: Listens for MQTT messages to trigger actions like sounding an alarm or sending SMS notifications.

## Requirements

- Python 3.x
- MQTT broker (e.g., [Mosquitto](https://mosquitto.org/))
- Python packages:
  - `paho-mqtt`
  - `joblib`
  - `numpy`
  


```bash
Follow the "Getting Started" instructions upto step 3
```

Run the simulation 

```bash
python raspberrycode2.py
```
Here’s a `README.md` file that provides instructions on how to set up and run the Django application API and dashboard:

---

# Django Application API and Dashboard

This project contains a Django application with an API and a dashboard to process sensor data, make predictions using a pre-trained TensorFlow Lite model, and display the results.

## Setup Instructions

Follow these steps to set up the project, run the application, and view the dashboard.

### 1. Create and Activate a Virtual Environment

First, create and activate a virtual environment to manage the dependencies:

#### For Linux/MacOS:
```bash
python3 -m venv env
source env/bin/activate
```

#### For Windows:
```bash
python -m venv env
.\env\Scripts\activate
```

### 2. Install Dependencies

Install the required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Set Up the Database

Change to the `listener` directory where the Django application resides, and apply the migrations to set up the database:

```bash
cd listener
python manage.py migrate
```

### 4. Add Data to the Database

To add the sensor testing data to the database (this may take a while depending on the size of the data), run the following script:

```bash
cd ..
python posttestingdata_to_django.py
```

This will populate your database with synthetic sensor data for testing purposes.

### 5. Run the Django Development Server

Change back to the `listener` directory and start the Django development server:

```bash
cd listener
python manage.py runserver
```

### 6. Access the Dashboard

Once the server is running, go to the dashboard by visiting the following URL in your browser:

```
http://localhost:8000/home/dashboard
```

### 7. Make Predictions

On the dashboard, you will be prompted to enter a **start date** and an **end date**. Input the desired date range, and the system will use the pre-trained model to make predictions based on the sensor data within that time frame.

- **Start Date**: Enter the starting date for the prediction (in `YYYY-MM-DD` format).
- **End Date**: Enter the ending date for the prediction (in `YYYY-MM-DD` format).

The dashboard will display whether the conditions during the selected time range are **"Normal"** or **"Critical"** based on the sensor data and the model’s prediction.

---

## Troubleshooting

### Date Format Error

If you enter the date in an incorrect format, you will be prompted to enter it again in the `YYYY-MM-DD` format.

### Runtime Errors

If you encounter a `FileNotFoundError` or similar errors when loading the model, make sure that the `my_model.tflite` file is correctly placed in the appropriate directory and accessible.

---





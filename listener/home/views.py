import os
from django.conf import settings
from django.shortcuts import render
from apis.models import PotholeData
import numpy as np
import tensorflow as tf
from datetime import datetime, timedelta
# Assuming the model is stored under the 'static/models' directory
model_path = os.path.join(settings.MEDIA_ROOT, 'models', 'my_model.tflite')

if not os.path.exists(model_path):
    raise FileNotFoundError(f"The model file was not found at {model_path}")


# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()


# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def dashboard(request):
    # Retrieve date range from GET request
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    # Default date range (e.g., last 1 day)
    if not start_date_str or not end_date_str:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
    else:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            return render(request, "home/dashboard.html", {
                "error": "Invalid date format. Please use YYYY-MM-DD."
            })

    # Query the database within the specified date range
    data = PotholeData.objects.filter(timestamp__range=[start_date, end_date]).order_by("timestamp")
  

    # Check if there's enough data for prediction
    sequence_length = 1440  # 1 day of data, adjust as needed
    if len(data) < sequence_length:
        return render(request, "home/dashboard.html", {
            "error": f"Not enough data points in the specified range ({len(data)} available)."
        })

    # Prepare the data sequence for prediction
    # Get the last `sequence_length` records by slicing with positive indexing
    data_count = data.count()
    if data_count < sequence_length:
        return render(request, "home/dashboard.html", {
            "error": f"Not enough data points in the specified range ({data_count} available)."
        })
        
    sequence = np.array([[d.load_value, d.tilt_status, d.distance] for d in data[data_count - sequence_length:data_count]])
    print(sequence)

    sequence = np.expand_dims(sequence, axis=0).astype(np.float32)

    # Perform prediction
    interpreter.set_tensor(input_details[0]['index'], sequence)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])
    print(prediction)
    status = "Critical" if (prediction > 0.5).astype("int32")[0][0] == 1 else "Normal"

    # Render the dashboard with prediction result
    return render(request, "home/dashboard.html", {
        "status": status,
        "start_date": start_date_str,
        "end_date": end_date_str,
    })

import tensorflow as tf

# Load your trained Keras model
model = tf.keras.models.load_model("my_model.keras")

# Convert the model to TFLite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
converter._experimental_lower_tensor_list_ops = False  # Avoids lowering tensor list ops
tflite_model = converter.convert()

# Save the TFLite model to a file
with open("my_model.tflite", "wb") as f:
    f.write(tflite_model)
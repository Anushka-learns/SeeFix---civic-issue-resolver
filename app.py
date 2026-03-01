# Import libraries
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

# Create Flask app
app = Flask(__name__)

# Load trained model
model = tf.keras.models.load_model("pothole_model.h5")

# Class labels
class_names = ["garbage", "normal", "potholes"]

# Prediction function
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]

    return predicted_class


# API endpoint
@app.route("/")
def home():
    return "SeeFix AI API is running"
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    result = predict_image(filepath)

    return jsonify({"prediction": result})


# Run server
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)

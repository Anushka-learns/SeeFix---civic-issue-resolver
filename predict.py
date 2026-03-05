import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import os

MODEL_PATH = "pothole_model.h5"
model = load_model(MODEL_PATH)

class_names = ["garbage", "normal", "pothole"]


def predict_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        prediction = model.predict(img_array)

        if prediction is None or len(prediction) == 0:
            return "unknown", "Low", 0.0

        class_index = np.argmax(prediction)
        confidence = float(np.max(prediction))

        if class_index >= len(class_names):
            label = "unknown"
        else:
            label = class_names[class_index]

        # AI severity logic
        if confidence > 0.8:
            severity = "High"
        elif confidence > 0.5:
            severity = "Medium"
        else:
            severity = "Low"

        return label, severity, round(confidence * 100, 2)

    except Exception as e:
        print("Prediction Error:", e)
        return "unknown", "Low", 0.0



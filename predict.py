# Import libraries
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load trained model
model = tf.keras.models.load_model("pothole_model.h5")

# Class names (same order as dataset folders)
class_names = ["garbage", "normal", "potholes"]

# Load image for testing
img_path = "1.jpg"  # put any pothole or garbage image here

img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = img_array / 255.0

# Predict
prediction = model.predict(img_array)
predicted_class = class_names[np.argmax(prediction)]

print("Prediction:", predicted_class)
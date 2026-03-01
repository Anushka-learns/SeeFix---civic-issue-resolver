# Import TensorFlow
import tensorflow as tf

# Import ImageDataGenerator for loading and preprocessing images
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Path to dataset folder
dataset_path = "dataset"

# Target image size for the model
img_size = (224, 224)

# Number of images processed in one batch
batch_size = 16

# Image generator for training + validation split
datagen = ImageDataGenerator(
    rescale=1./255,          # Normalize pixel values (0–255 → 0–1)
    validation_split=0.2     # 80% training, 20% validation
)

# Load training data
train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",   # Multi-class classification
    subset="training"
)

# Load validation data
val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",
    subset="validation"
)

# Load pre-trained MobileNetV2 model (Transfer Learning)
base_model = tf.keras.applications.MobileNetV2(
    weights="imagenet",         # Use ImageNet trained weights
    include_top=False,          # Remove original classifier
    input_shape=(224, 224, 3)
)

# Freeze base model layers (so they don't train again)
base_model.trainable = False

# Add custom layers for our classification task
x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
x = tf.keras.layers.Dense(128, activation="relu")(x)

# Output layer (number of classes from dataset)
output = tf.keras.layers.Dense(train_data.num_classes, activation="softmax")(x)

# Create final model
model = tf.keras.models.Model(inputs=base_model.input, outputs=output)

# Compile model
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Train the model
model.fit(
    train_data,
    validation_data=val_data,
    epochs=5
)

# Save trained model
model.save("pothole_model.h5")

print("Model training completed and saved!")
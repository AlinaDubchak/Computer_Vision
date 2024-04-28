from tensorflow.keras import layers, models
import cv2
import os
import numpy as np

# Function to load data with resizing
def load_data(data_dir, target_size):
    images = []
    labels = []
    for subdir in os.listdir(data_dir):
        if subdir == "open" or subdir == "closed":
            label = 1 if subdir == "open" else 0
            subdir_path = os.path.join(data_dir, subdir)
            # Iterate over images in the subdirectory
            for file in os.listdir(subdir_path):
                img_path = os.path.join(subdir_path, file)
                image = cv2.imread(img_path)
                # Resize image to target size
                image = cv2.resize(image, target_size)
                images.append(image)
                labels.append(label)

    return images, labels

# Function to create model
def create_model(input_shape):
    model = models.Sequential([
        # Convolutional layers to extract features
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        # Flatten layer to convert 2D feature maps to 1D vectors
        layers.Flatten(),
        # Dense layers for classification
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')  # Output layer for binary classification
    ])
    # Compile the model with optimizer, loss function, and metrics
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model


target_size = (100, 100)


data_directories = ["./dataset/train", "./dataset/test"]

# Iterate over each directory
for data_dir in data_directories:
    # Load data with resizing
    images, labels = load_data(data_dir, target_size)

    # Convert images and labels to numpy arrays
    images = np.array(images)
    labels = np.array(labels)

    # Normalize pixel values
    images = images / 255.0

    # Get image dimensions
    image_width, image_height = images[0].shape[1], images[0].shape[0]
    input_shape = (image_height, image_width, 3)

    # Create and train model
    model = create_model(input_shape)
    model.fit(images, labels, epochs=10, batch_size=32, validation_split=0.2)

# Save the trained model
model.save("eyes_detection_model.h5")

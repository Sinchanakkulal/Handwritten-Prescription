import tensorflow as tf # type: ignore
from tensorflow.keras import layers, models # type: ignore

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(1200, 600, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(62, activation='softmax')  # Example output layer for 62 classes (A-Z, 0-9)
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Prepare your dataset for training (resize, normalize, etc.)
model.fit(train_images, train_labels, epochs=10, batch_size=32) # type: ignore

# Save your trained model
model.save('saved_model/handwritten_recognition_model')


import numpy as np
from keras.layers import Conv2D, Flatten, Dense
from keras.models import Sequential

# Instantiate the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(8, 8, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(1, activation='linear')
])

# Print model summary
model.compile(optimizer='adam', loss='mean_squared_error')
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
model.summary()

bitboard_black = np.random.randint(2, size=(8, 8, 1))
bitboard_white = np.random.randint(2, size=(8, 8, 1))
position = np.concatenate((bitboard_black, bitboard_white), axis=-1)  # Combine black and white bitboards
evaluation = model.predict(np.expand_dims(position, axis=0))  # Add a batch dimension
print(evaluation)
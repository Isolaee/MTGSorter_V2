import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Dense  # type: ignore
from tensorflow.keras.utils import to_categorical  # type: ignore
import os
import sys

# -----------------------------------------------
# If you have added new data remember to run cardDataBuilder.py


# Reconfigure stdout to use UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

# -------------------
# Load the dataset
deck_data = pd.read_json("deck_dataset.json", encoding="utf-8", encoding_errors="replace")
card_data = pd.read_json("card_dataset.json", encoding="utf-8", encoding_errors="replace")


# Aggregate card data to deck level
def aggregate_deck_features(deck_id):
    deck_cards = card_data[card_data["deck_name"] == deck_id]
    return deck_cards.mean()


deck_aggregated_features = (
    deck_data["deck_name"].apply(aggregate_deck_features).reset_index()
)
deck_aggregated_features.drop(columns=["index"], inplace=True)

# Combine aggregated features with the target variable
X = deck_aggregated_features
y = deck_data["power_level"]  # Ensure y is a Series

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# Build the model
# Convert labels to categorical one-hot encoding (if necessary)
num_classes = 10
y_train_encoded = to_categorical(
    y_train - 1, num_classes=num_classes
)  # Assuming power level is from 1-10
y_test_encoded = to_categorical(y_test - 1, num_classes=num_classes)

# Build the model
model = Sequential(
    [
        Dense(64, activation="relu", input_shape=(X_train_scaled.shape[1],)),
        Dense(32, activation="relu"),
        Dense(num_classes, activation="softmax"),
    ]
)


# Compile the model
model.compile(optimizer="Adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Print the model summary
model.summary()

# ------------------
# Train the model
history = model.fit(
    X_train_scaled, y_train_encoded, epochs=50, batch_size=8, validation_split=0.2
)

# -------------------------
# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test_scaled, y_test_encoded)
print(f"Test Accuracy: {test_accuracy:.2f}")

# -------------------------------
# Make predictions
predictions = model.predict(X_test_scaled)

# Convert predictions from one-hot encoding to class labels
predicted_classes = (
    tf.argmax(predictions, axis=1) + 1
)  # Adding 1 because power level starts from 1

# Display some results
for i in range(10):
    print(f"True: {y_test.iloc[i]}, Predicted: {predicted_classes[i]}")

print("Dataset size: ", len(deck_data))

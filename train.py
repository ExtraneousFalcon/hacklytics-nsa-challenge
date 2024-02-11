from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
import tensorflow as tf
from sklearn.metrics import classification_report

df = pd.read_csv('netflows_with_features.csv')
df.drop(columns=['pr','src_ip', 'dst_ip', 'src_pt', 'dst_pt', 'cnt','bts', 'flgs','src_asn'], inplace=True)

df = pd.get_dummies(df, columns=['dst_subnet'], drop_first=True)

# Separate features and target
X = df.drop('attacker', axis=1)
y = df['attacker']

# Preprocess the features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model
model = Sequential()
model.add(Dense(32, input_dim=X_train.shape[1], activation='relu'))  # Input layer
model.add(Dense(16, activation='relu'))  # Hidden layer
model.add(Dense(1, activation='sigmoid'))  # Output layer

# Define weights
weight_for_0 = 10.0  # For class 0
weight_for_1 = 1.0  # For class 1, increase the weight if you want to penalize false positives more

# Create a custom weighted loss function
def weighted_binary_crossentropy(y_true, y_pred):
    bce = tf.keras.losses.BinaryCrossentropy()
    y_true = tf.cast(y_true, tf.float32)  # Add this line
    loss = bce(y_true, y_pred, sample_weight=(weight_for_0 * (1 - y_true) + weight_for_1 * y_true))
    return loss
# Compile the model with the custom loss function
model.compile(loss=weighted_binary_crossentropy, optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=1, batch_size=32)


# Predict the test set results
y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5)

# Print the classification report
print(classification_report(y_test, y_pred))

import pprint

# Assume the model has been trained...

# Get the weights
weights = model.get_weights()

# Convert the weights to a list of lists of numbers
weights_list = [w.tolist() for w in weights]

# Create a PrettyPrinter object
pp = pprint.PrettyPrinter(indent=4)

# Use the PrettyPrinter object to generate a string
weights_str = pp.pformat(weights_list)

# Open a file in write mode
with open('weights.txt', 'w') as f:
    # Write the string to the file
    f.write(weights_str)

print(weights.shape)
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# Load the data from the CSV file
data = pd.read_csv("airline_crash_data.csv")

# One-hot encode the categorical features
data = pd.get_dummies(data, columns=["Aircraft Maintenance", "Weather Conditions", "Pilot Experience", "Air Traffic Control", "Human Factors", "Flight Operations", "Security"])

# Split the data into training and testing sets
X = data.drop(columns=["Crash or Not"])
y = data["Crash or Not"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest classifier on the data
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate the model on the test set
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the model to a file
with open("airline_crash_model.pkl", "wb") as f:
    pickle.dump(clf, f)


# Load the trained model from the file
with open("airline_crash_model.pkl", "rb") as f:
    clf = pickle.load(f)

# Prompt the user for input values for each feature
aircraft_maintenance = input("Aircraft Maintenance: ")
weather_conditions = input("Weather Conditions: ")
pilot_experience = input("Pilot Experience: ")
air_traffic_control = input("Air Traffic Control: ")
human_factors = input("Human Factors: ")
flight_operations = input("Flight Operations: ")
security = input("Security: ")

# Create a data frame with the user inputs
user_data = pd.DataFrame({
    "Aircraft Maintenance_" + aircraft_maintenance: [1],
    "Weather Conditions_" + weather_conditions: [1],
    "Pilot Experience_" + pilot_experience: [1],
    "Air Traffic Control_" + air_traffic_control: [1],
    "Human Factors_" + human_factors: [1],
    "Flight Operations_" + flight_operations: [1],
    "Security_" + security: [1]
})

# Encode the user inputs using the same one-hot encoding as the training data
for col in X.columns:
    if col not in user_data.columns:
        user_data[col] = 0
user_data = user_data[X.columns]

# Make a prediction using the trained model
prediction = clf.predict(user_data)

if prediction[0] == 1:
    print("Airline crash is likely.")
else:
    print("Airline crash is not likely.")

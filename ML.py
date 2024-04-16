# Importing necessary libraries
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from flask import Flask, request, jsonify, render_template

# Load dataset
data = load_iris()
X = data.data
y = data.target

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features using Scikit-learn
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)

# Define the neural network using TensorFlow
def create_tf_model():
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
        Dense(64, activation='relu'),
        Dense(3, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Train the TensorFlow model
tf_model = create_tf_model()
tf_model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, verbose=0)

# Define the deep learning model using PyTorch
class PyTorchModel(nn.Module):
    def __init__(self):
        super(PyTorchModel, self).__init__()
        self.fc1 = nn.Linear(X_train_scaled.shape[1], 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 3)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.softmax(self.fc3(x))
        return x

# Instantiate the PyTorch model
pytorch_model = PyTorchModel()

# Define loss function and optimizer for PyTorch
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(pytorch_model.parameters(), lr=0.001)

# Train the PyTorch model
def train_pytorch_model(model, criterion, optimizer, X_train, y_train, epochs=50, batch_size=32):
    dataset = TensorDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    for epoch in range(epochs):
        for inputs, targets in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

train_pytorch_model(pytorch_model, criterion, optimizer, X_train_tensor, y_train_tensor)

# Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    sepal_length = float(request.form['sepal_length'])
    sepal_width = float(request.form['sepal_width'])
    petal_length = float(request.form['petal_length'])
    petal_width = float(request.form['petal_width'])

    # Preprocess the input data
    input_data = scaler.transform([[sepal_length, sepal_width, petal_length, petal_width]])
    
    # Predict with TensorFlow model
    tf_prediction = tf_model.predict(input_data)[0]

    # Predict with PyTorch model
    pytorch_input_tensor = torch.tensor(input_data, dtype=torch.float32)
    pytorch_prediction = pytorch_model(pytorch_input_tensor).detach().numpy()[0]

    return render_template('result.html', 
                           tf_setosa=tf_prediction[0], tf_versicolor=tf_prediction[1], tf_virginica=tf_prediction[2],
                           pt_setosa=pytorch_prediction[0], pt_versicolor=pytorch_prediction[1], pt_virginica=pytorch_prediction[2])

if __name__ == '__main__':
    app.run(debug=True)
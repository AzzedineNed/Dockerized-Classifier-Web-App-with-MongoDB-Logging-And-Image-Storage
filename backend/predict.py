import os
import numpy as np
import random
import cv2
from flask import Flask, request, jsonify
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import preprocess_input
from pymongo import MongoClient
import gridfs
import time

# Set up the Flask application
app = Flask(__name__)

# Set seeds for reproducibility
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(42)
random.seed(42)

# MongoDB connection
MONGO_URI = "mongodb://mongodb:27017"
#MONGO_URI = "mongodb://localhost:27017" #to run locally
client = MongoClient(MONGO_URI)
db = client['predictions_db']
collection = db['logs']
fs = gridfs.GridFS(db)

# Load ResNet50 model without the top classification layer
base_model = ResNet50(weights='imagenet', include_top=False)
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(2, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the layers
for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Preprocessing function
def load_and_preprocess_image(image):
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

# Predict function
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    img_data = file.read()

    # Preprocess the image
    img = load_and_preprocess_image(img_data)

    # Make predictions
    preds = model.predict(img)
    class_idx = np.argmax(preds[0])
    class_names = ['Cat', 'Dog']
    predicted_class = class_names[class_idx]
    confidence = preds[0][class_idx]

    # Convert the confidence score to a native Python float
    confidence = float(confidence) if isinstance(confidence, np.generic) else confidence

    # Save the image to MongoDB using GridFS
    file_id = fs.put(img_data, filename=file.filename)

    # Log prediction to MongoDB
    log_prediction(file_id, file.filename, predicted_class, confidence)

    return jsonify({'prediction': predicted_class, 'confidence': confidence, 'filename': file.filename})

def log_prediction(file_id, file_name, prediction, confidence):
    log_data = {
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        'file_id': file_id,
        'file_name': file_name,
        'prediction': prediction,
        'confidence': confidence
    }
    collection.insert_one(log_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

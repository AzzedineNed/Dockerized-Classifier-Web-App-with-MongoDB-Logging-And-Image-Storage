from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Ensure the uploads folder exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

BACKEND_URL = "http://backend:5001/predict" 
#BACKEND_URL = "http://127.0.0.1:5001/predict"  # to run locally

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    if not file:
        return "No file uploaded", 400

    # Save the uploaded file to static/uploads
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Send the image to the backend for prediction
    with open(file_path, 'rb') as img_file:
        response = requests.post(BACKEND_URL, files={'file': img_file})

    # Handle backend errors
    if response.status_code != 200:
        return "Error from backend", 500

    # Get the JSON response from backend
    result = response.json()

    # Pass the result to the result.html template for rendering
    return render_template('result.html', 
                           predicted_class=result['prediction'], 
                           confidence=result['confidence'], 
                           image_path=url_for('static', filename=f"uploads/{result['filename']}"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

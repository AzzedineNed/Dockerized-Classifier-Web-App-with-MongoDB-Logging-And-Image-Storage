# Dockerized-Classifier-Web-App-with-MongoDB-Logging-And-Image-Storage

This project extends the functionality of the [Dockerized Classifier Web App with MongoDB Logging](https://github.com/AzzedineNed/Dockerized-Classifier-Web-App-with-MongoDB-Logging) by incorporating a dedicated image storage system. The web app classifies uploaded images of cats or dogs using a pre-trained ResNet50 model, logs predictions to MongoDB, and stores the images themselves in MongoDB using GridFS for scalable, efficient storage.

## Features
- **Image Upload via Frontend**: Users can upload an image of a cat or dog through the frontend web interface.
- **Image Classification with ResNet50**: The backend processes the uploaded image using the pre-trained ResNet50 model to classify it as either a cat or a dog.
- **MongoDB Logging**: Classification results, including the image name, predicted label, and confidence score, are logged in MongoDB for analysis and tracking.
- **Image Storage in MongoDB (GridFS)**: Uploaded images are stored in MongoDB using GridFS, ensuring that the system can handle large image files efficiently and that data is stored reliably.
- **Dockerized Multi-Service Application**: The app uses Docker Compose to manage the frontend, backend, and MongoDB services, ensuring a seamless, scalable, and reproducible environment.
- **Prediction Storage**: Prediction details such as image name, predicted label, and confidence score are logged in MongoDB alongside the image itself for easy retrieval and future analysis.
- **Reproducibility**: Docker ensures that the environment can be easily replicated with consistent behavior across all machines.


## Requirements

- **Docker**: Ensure Docker is installed on your system.
- **Docker Compose**: To orchestrate the frontend, backend, and MongoDB services.
- **MongoDB**: Used for logging predictions and storing images with GridFS.


## How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/YourUsername/Dockerized-Classifier-Web-App-with-MongoDB-Logging-And-Image-Storage
```

### CD to the repo

```bash
cd Dockerized-Classifier-Web-App-with-MongoDB-Logging-And-Image-Storage
```

### Step 2: Build and Run using Docker Compose

```bash
docker-compose up --build
```
This command builds all services (frontend, backend, and MongoDB) and starts them. Docker Compose automatically creates a shared network for seamless communication between services.

### Step 3: Access the Application

- **Frontend**: Open your web browser and go to http://localhost:5000 to access the upload interface.
- **MongoDB**: Prediction data and images are stored in the predictions_db database within the predictions collection. Images themselves are stored in GridFS for efficient handling of large files. Use any MongoDB client to query the database using the connection string mongodb://localhost:27017..

### Step 4: Stop the Services

To stop the running services, use the following command:

```bash
docker-compose down
```

### How the System Works

- **Frontend (Flask)**: Users interact with the frontend by uploading an image of a cat or dog.

- **Backend (Flask)**: The frontend sends the uploaded image to the backend, where it is processed and classified using the ResNet50 model.

- **Prediction and Result Display**: The backend returns the classification result, including the predicted label and confidence score, which the frontend then displays to the user.

- **MongoDB Logging**: The backend stores the prediction results and image in MongoDB. Images are stored using GridFS, a specification for storing large files in MongoDB, while classification results (image name, predicted label, confidence score) are stored in the predictions collection for future analysis.

- **Image Storage in MongoDB (GridFS)**: With GridFS, the application can efficiently store and retrieve large images. It breaks the images into smaller chunks and stores them across multiple documents, making it scalable and optimized for large datasets.

### Networking

Docker Compose automatically sets up an internal network, allowing the frontend, backend, and MongoDB services to communicate securely and efficiently. While the services are isolated in containers, they are interconnected, facilitating secure communication and data handling.


### Improvements from Previous Version
- **GridFS Image Storage**: Images are now stored in MongoDB's GridFS, enabling better handling of large images.

- **Enhanced Code Structure**: The project is more modular, making it easier to maintain and extend.

- **Docker-Optimized Architecture**: Ensures fast and reproducible environment setups with Docker, making deployments seamless.

- **Streamlined Logging**: Prediction details and images are now more efficiently logged, improving scalability and future analysis capabilities.


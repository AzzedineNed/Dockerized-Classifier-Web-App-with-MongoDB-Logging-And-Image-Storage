# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set a working directory
WORKDIR /app

# Install system dependencies (for OpenCV and TensorFlow)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the FLASK_APP environment variable
ENV FLASK_APP=predict.py

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire app to the container
COPY . /app/

# Expose port 5001 for the Flask app
EXPOSE 5001

# Set the default command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

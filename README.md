# SeeFix – AI Civic Issue Detection 🚧

SeeFix is an AI-powered system that helps detect civic infrastructure issues like potholes and garbage using images.  
Users can upload an image, and the AI model predicts whether the issue is relevant or not.

This project combines:
- Computer Vision
- Backend API
- Real-world civic problem solving

---

## Project Workflow

User uploads image  
→ Backend API processes request  
→ AI model analyzes image  
→ Prediction returned (pothole / garbage / normal)

---

## System Architecture

Frontend (Upload Image)  
↓  
Flask Backend API  
↓  
Image Preprocessing  
↓  
AI Model (MobileNetV2 Transfer Learning)  
↓  
Prediction (pothole / garbage / normal)

---

## Features

- Detect potholes and garbage using AI
- Image classification model
- Backend API for predictions
- Transfer learning using MobileNetV2
- Scalable smart city application idea

---

## Tech Stack

Machine Learning
- TensorFlow
- Keras
- MobileNetV2

Backend
- Flask
- Python

Tools
- Virtual Environment
- GitHub
- VS Code

---

## Dataset Structure

dataset/
   garbage/
   normal/
   potholes/

Each folder contains images of the respective class.

Classes used:
- Garbage
- Normal
- Potholes

---

## Model Details

Base Model: MobileNetV2  
Training Method: Transfer Learning  
Input Size: 224 x 224  
Output Classes: 3  

The base model is frozen and custom layers are added for classification.

---

## Installation

### Clone Repository
git clone https://github.com/Anushka-learns/seefix
cd seefix

### Create Virtual Environment
python -m venv seefix-env
seefix-env\Scripts\activate

### Install Dependencies
pip install tensorflow flask numpy

---

## Train the Model

python training.py

This will generate:
pothole_model.h5

---

## Run Prediction

python predict.py

Example output:
Prediction: potholes

---

## Run Backend API

python app.py

Server runs on:
http://127.0.0.1:5000

Test route:
http://127.0.0.1:5000/

Prediction endpoint:
POST /predict

---

## Project Status

Completed
- Dataset preparation
- Model training
- Prediction pipeline
- Flask API

In Progress
- Frontend interface
- User login system
- Municipal dashboard
- Deployment

---

## Future Improvements

- GPS-based issue reporting
- Complaint tracking system
- Severity detection of potholes
- Mobile app
- Cloud deployment

---

## Author

Anushka  
B.Tech CSE (AI & ML)

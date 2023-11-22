#!/usr/bin/env python3

from ultralytics import YOLO 

# Load the model
model = YOLO('yolov8n.pt')

# Training 
results = model.train(
    data = 'datasets/data.yaml',
    imgsz = 640,
    epochs = 60,
    batch = 8,
    name = 'moonbot_perception'
)
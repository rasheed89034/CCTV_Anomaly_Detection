# module_2_ai.py
from ultralytics import YOLO
import config

print("Loading AI Model...")
model = YOLO(config.AI_MODEL_PATH)

def process_frame_with_ai(frame):
    # Predict with given threshold
    results = model.predict(frame, conf=config.CONFIDENCE_THRESHOLD, verbose=False)
    
    # Extract detected class names
    detected_classes = []
    for r in results:
        for c in r.boxes.cls:
            detected_classes.append(model.names[int(c)])
            
    # Get the image with bounding boxes
    annotated_frame = results[0].plot()
    
    return annotated_frame, detected_classes
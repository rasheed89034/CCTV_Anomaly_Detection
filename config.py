# config.py

# Module 1 Settings
PHONE_URL = 0
SKIP_FRAMES = 3
RESIZE_DIM = (640, 640)

# Module 2 & 3 Settings
AI_MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.5
ABNORMAL_CLASSES = ["person", "knife", "fire"] # Demo ke liye person rakha hai, baad mein fight/accident se replace karein
COOLDOWN_SECONDS = 10
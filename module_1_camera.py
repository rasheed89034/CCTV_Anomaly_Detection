# module_1_camera.py
import cv2

def get_camera_stream(ip_url):
    cap = cv2.VideoCapture(ip_url)
    if not cap.isOpened():
        print("Error: Camera connection failed!")
        return None
    return cap
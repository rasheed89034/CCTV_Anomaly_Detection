# module_3_logic.py
import time
import config

last_alert_time = 0

def check_for_anomalies(detected_classes):
    global last_alert_time
    
    # Check if any detected object is in our abnormal list
    anomalies = [cls for cls in detected_classes if cls in config.ABNORMAL_CLASSES]
    
    if anomalies:
        current_time = time.time()
        # Cooldown logic check
        if current_time - last_alert_time > config.COOLDOWN_SECONDS:
            last_alert_time = current_time
            return True, anomalies
            
    return False, []
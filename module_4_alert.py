# module_4_alert.py
import threading
from datetime import datetime

def send_sms_alert(anomalies):
    # Yahan Twilio ya SMS API ka code aayega
    time_str = datetime.now().strftime("%H:%M:%S")
    print(f"\n[ALERT SENT] {time_str} - URGENT! Detected: {', '.join(anomalies)}")

def log_to_database(anomalies):
    # Yahan database saving ka code aayega
    pass

def trigger_emergency_protocols(anomalies):
    # Threading use kar rahe hain taake main video stream lag na kare
    threading.Thread(target=send_sms_alert, args=(anomalies,)).start()
    threading.Thread(target=log_to_database, args=(anomalies,)).start()
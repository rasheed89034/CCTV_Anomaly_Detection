# module_5_app.py
import cv2
import streamlit as st
import time
import config

# Importing all previous modules
from module_1_camera import get_camera_stream
from module_2_ai import process_frame_with_ai
from module_3_logic import check_for_anomalies
from module_4_alert import trigger_emergency_protocols

# Streamlit UI Setup
st.set_page_config(page_title="SMART-CCTV", layout="wide")
st.title("🛡️ SMART-CCTV: Real-Time Anomaly Detection")

# Live Alert Box
live_alert_box = st.empty() 

# UI Columns layout
col1, col2 = st.columns([3, 1])
video_placeholder = col1.empty()
alert_history = col2.empty()

# Start Button
if st.button("Start Live Monitoring"):
    cap = get_camera_stream(config.PHONE_URL)
    
    if cap:
        frame_count = 0
        history_list = []
        DISPLAY_DIM = (640, 360) 
        
        # ---> NAYI LOGIC: Alert ko 5 second tak screen par rokne ke liye variables
        alert_end_time = 0
        current_alert_msg = ""
        current_alert_type = ""
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Camera Disconnected!")
                break
                
            frame = cv2.flip(frame, 1) 
            
            frame_count += 1
            if frame_count % config.SKIP_FRAMES != 0:
                continue
                
            frame = cv2.resize(frame, DISPLAY_DIM)
            
            # Module 2 & 3: AI and Logic
            ai_frame, detected_classes = process_frame_with_ai(frame)
            is_critical, anomalies = check_for_anomalies(detected_classes)
            
            # ---> Agar AI koi khatra detect karta hai
            if is_critical:
                trigger_emergency_protocols(anomalies)
                
                detected_item = anomalies[0].lower() 
                current_time = time.strftime('%H:%M:%S')
                
                # Alert ko current time se 5 seconds aage tak screen par freeze kar do
                alert_end_time = time.time() + 5
                current_alert_type = detected_item
                
                # Message Set Karo
                if detected_item == "fire":
                    current_alert_msg = "🔥 URGENT: FIRE DETECTED! Evacuation Protocol Initiated."
                elif detected_item == "fight": 
                    current_alert_msg = "🥊 URGENT: FIGHT / SUSPICIOUS ACTIVITY! Security Dispatched."
                elif detected_item == "knife":
                    current_alert_msg = "🔪 URGENT: WEAPON DETECTED!"
                else:
                    # Yeh dynamic hai, jo detect hoga uska naam aayega (e.g. Person, Cell Phone)
                    current_alert_msg = f"⚠️ ALERT: {detected_item.upper()} DETECTED in the frame!"
                
                # History List ko update karo
                history_list.insert(0, f"**[{current_time}]** {detected_item.upper()} Detected")
                
            # ---> 5 Second Display Logic (Video slow kiye bina message show karna)
            if time.time() < alert_end_time:
                if current_alert_type in ["fire", "knife"]:
                    live_alert_box.error(current_alert_msg) # Lal (Red) Box
                else:
                    live_alert_box.warning(current_alert_msg) # Peela (Yellow) Box
            else:
                live_alert_box.empty() # 5 second baad automatically ghayab
                
            # ---> History Sidebar (Ab brackets ki bajaye saaf list nazar aayegi)
            if history_list:
                history_md = "\n".join([f"- {item}" for item in history_list[:10]])
                alert_history.markdown(f"### 🚨 Alert History\n{history_md}")
            
            # Output to UI Dashboard
            ai_frame = cv2.cvtColor(ai_frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(ai_frame, channels="RGB", use_container_width=True)
            
        cap.release()



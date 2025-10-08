import cv2
import face_recognition
import mediapipe as mp
from flask_socketio import emit

def run_attendance(socketio):
    # Your existing bodylang.py logic here
    # But instead of cv2.imshow, send frames via WebSocket
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process frame (your logic)
        # ...
        
        # Send to frontend
        _, buffer = cv2.imencode('.jpg', frame)
        frame_encoded = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('video_frame', {'frame': frame_encoded, 'status': status})
    
    cap.release()
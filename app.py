import cv2
import mediapipe as mp
import numpy as np
import time

# Aadhaar-Secure: Real-Time Face Liveness Detection
# Developed by: Anish Kanaujiya (B.Tech CSE AI & ML)

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Eye Landmark Indices for EAR Calculation (MediaPipe 468 landmarks)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def calculate_ear(landmarks, eye_indices):
    """Calculate Eye Aspect Ratio (EAR) to detect blinks."""
    # Vertical points
    p2_p6 = np.linalg.norm(np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y]) - 
                           np.array([landmarks[eye_indices[5]].x, landmarks[eye_indices[5]].y]))
    p3_p5 = np.linalg.norm(np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y]) - 
                           np.array([landmarks[eye_indices[4]].x, landmarks[eye_indices[4]].y]))
    # Horizontal point
    p1_p4 = np.linalg.norm(np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y]) - 
                           np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y]))
    
    ear = (p2_p6 + p3_p5) / (2.0 * p1_p4)
    return ear

# Camera Setup
cap = cv2.VideoCapture(0)
EAR_THRESHOLD = 0.22 # Adjust this value based on your lighting
BLINK_COUNT = 0
LIVENESS_STATUS = "SCANNING..."

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip the image for a selfie-view
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Calculate EAR for both eyes
            left_ear = calculate_ear(face_landmarks.landmark, LEFT_EYE)
            right_ear = calculate_ear(face_landmarks.landmark, RIGHT_EYE)
            avg_ear = (left_ear + right_ear) / 2.0

            # Liveness Logic: If EAR drops below threshold, it's a blink (Human)
            if avg_ear < EAR_THRESHOLD:
                BLINK_COUNT += 1
                LIVENESS_STATUS = "LIVENESS: REAL (Human Detected)"
                color = (0, 255, 0) # Green for Success
            else:
                if BLINK_COUNT == 0:
                    LIVENESS_STATUS = "STATUS: SCANNING (Potential Spoof)"
                    color = (0, 0, 255) # Red for Warning
                else:
                    LIVENESS_STATUS = "LIVENESS: REAL"
                    color = (0, 255, 0)

            # Display Status on Frame
            cv2.putText(frame, LIVENESS_STATUS, (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, f"Blinks: {BLINK_COUNT}", (30, 90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Aadhaar-Secure: Liveness Detection', frame)

    if cv2.waitKey(5) & 0xFF == 27: # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()
# Aadhaar-Secure: Real-Time Face Liveness Detection
This project is a specialized security solution developed for the UIDAI Data Hackathon 2026 to prevent biometric spoofing in Aadhaar-based face authentication.
# 📌 Problem Statement
Current facial recognition systems are vulnerable to Presentation Attacks, such as high-resolution photos or digital video replays. This is a major security risk for services like PDS (Ration) distribution and doorstep banking.
# 🚀 Our Solution
Aadhaar-Secure implements an Active Liveness Detection layer. It ensures that the person being authenticated is a live human by detecting real-time eye blinks using computer vision.
# 🛠 How It Works (EAR Logic)
We use MediaPipe Face Mesh to track 468 facial landmarks. The system calculates the Eye Aspect Ratio (EAR) to distinguish between an open and closed eye:
$$EAR = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2||p_1 - p_4||}
$$Liveness: REAL – Detected when the user naturally blinks.
Status: SCANNING/SPOOF – If no blinking is detected (as in a photo or static video), the system flags a potential attack.
# 💻 Tech Stack
Language: Python
Libraries: OpenCV, MediaPipe, NumPy
Architecture: Edge-AI (Local processing for privacy)
# ⚙️ Installation & Usage 
1).Clonethe repository:git clone https://github.com/Anish-114/Aadhaar-Secure-Liveness.
2).Install dependencies:pip install -r requirements.txt
3).Run the application:python app.py
## 🔮 Future Scope
To make **Aadhaar-Secure** more robust, we plan to implement:
* **Deepfake Detection:** Identifying AI-generated faces in real-time.
* **Heart Rate Monitoring:** Confirming human presence through rPPG technology.
* **Offline Optimization:** Ensuring the model runs smoothly on low-end mobile devices in rural areas.

  
## 👨‍💻 AuthorAnish Kanaujiya B.Tech Computer Science Engineering (AI & ML)

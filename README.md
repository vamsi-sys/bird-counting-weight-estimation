# 🐔 Bird Counting & Weight Estimation System

An end-to-end computer vision system for **automatic bird counting and approximate weight estimation** from poultry farm CCTV videos using **YOLOv8, object tracking, and a FastAPI backend**.

This project was built as part of an **ML Intern technical assignment** and focuses on **real-world applicability, clean architecture, and explainability**.

---

## 📌 Problem Statement

Manual bird counting and weight monitoring in poultry farms is:

- Time-consuming  
- Error-prone  
- Not scalable  

This system automates:

- **Unique bird counting** from video streams  
- **Bird count over time (timestamp → count)**  
- **Approximate weight estimation using a video-based proxy**  
- **Annotated video generation**  
- **Structured JSON output for analytics**

---

## 🚀 Features

- 🎯 YOLOv8-based bird detection  
- 🔁 Object tracking with unique IDs to avoid double counting  
- 📊 Bird count over time using tracking IDs  
- ⚖️ Heuristic weight estimation per bird (proxy-based)  
- 🎥 Annotated output video with bounding boxes, IDs, and live count  
- 🌐 REST API built with FastAPI  
- 📄 Clean JSON response for downstream analytics  
- ⚡ Performance optimizations (model warm-up, frame skipping, resizing)

---

## 🗂️ Project Structure

<img width="462" height="673" alt="image" src="https://github.com/user-attachments/assets/4cfbc700-12f4-4dd3-991f-11d2b3463c85" />

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/vamsi-sys/bird-counting-weight-estimation.git
cd bird-counting-weight-estimation
```
###2️⃣ Create and activate virtual environmen
```bash
python -m venv venv

Windows

venv\Scripts\activate


Linux / Mac

source venv/bin/activate
```
###3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
##▶️ Running the Application
```bash
Start the FastAPI server:

python -m uvicorn app.main:app --reload


Server will run at:

http://127.0.0.1:8000
```
##🔌 API Usage
```bash
Health Check
GET /health


Response:

{
  "status": "ok"
}

Analyze Video
POST /analyze-video

Request

Content-Type: multipart/form-data

Key: file

Value: CCTV video file (.mp4, .avi, .mov)

Example (curl):

curl -X POST "http://127.0.0.1:8000/analyze-video" \
-F "file=@poultry.mp4"
```
##📤 Sample JSON Response
```bash
{
  "frames_processed": 1243,
  "unique_birds": 56,
  "counts_over_time": [
    { "time_sec": 0, "count": 12 },
    { "time_sec": 5, "count": 21 }
  ],
  "tracks_sample": [
    { "id": 3, "bbox": [120.5, 45.2, 200.1, 180.6] }
  ],
  "weight_estimation": {
    "average_grams": 1450,
    "min_grams": 1200,
    "max_grams": 1800
  },
  "annotated_video": "outputs/annotated_video.mp4"
}
```
##🧠 How It Works
```bash
Detection

YOLOv8 detects birds frame-by-frame from the input video.

Tracking & Counting

Detected birds are assigned unique tracking IDs, which allows:

Stable tracking across frames

Avoidance of double counting

Accurate bird count over time

Weight Estimation

Weight estimation is heuristic and proxy-based, using bounding-box area as an indicator of bird size.

Actual gram-level accuracy would require camera calibration or labeled training data.

Output

Annotated video with bounding boxes, IDs, and live count

Structured JSON analytics response
```
##⚡ Performance Optimizations
```bash
Model warm-up at application startup to avoid first-request latency

Frame skipping to reduce inference load

Frame resizing for faster processing while maintaining accuracy
```
##📦 Outputs
```bash
🎥 outputs/annotated_video.mp4 → Annotated video output

📄 sample_response.json → Example analytics response
```
##🧪 Limitations & Assumptions
```bash
Weight estimation is approximate and proxy-based

Designed for fixed-camera poultry farm videos

Accuracy depends on video quality, angle, and lighting
```
##🔮 Future Improvements
```bash
Camera calibration for accurate weight estimation

Support for live RTSP camera feeds

Model fine-tuning on poultry-specific datasets

Database integration for long-term analytics

Dockerized deployment
```
##🧾 License

This project is released under the MIT License.
You are free to use, modify, and distribute it.

###👤 Author

Vamsikrishna Sirimalla
GitHub: https://github.com/vamsi-sys

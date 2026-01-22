🐔 Bird Counting & Weight Estimation System

A computer vision–based system for automatic bird counting and approximate weight estimation from poultry farm videos using YOLOv8, object tracking, and a FastAPI backend.

This project was built as part of an ML Intern technical assignment and focuses on real-world applicability, clean architecture, and explainability.

📌 Problem Statement

Manual bird counting and weight monitoring in poultry farms is:

Time-consuming

Error-prone

Not scalable

This system automates:

Unique bird counting from video streams

Approximate weight estimation

Annotated video generation

Structured JSON output for analytics

🚀 Features

📊 Aggregated weight statistics (average / min / max) to avoid misleading per-frame weight noise

🎯 YOLOv8-based bird detection

🔁 Object tracking to avoid double counting

⚖️ Heuristic weight estimation per bird

🎥 Annotated output video

🌐 REST API built with FastAPI

📄 Clean JSON response for downstream usage

• Bird count over time (timestamp → count) using tracking IDs
Instead of counting per frame, the system tracks unique bird IDs and records population count at fixed time intervals.

🗂️ Project Structure
bird-counting-weight-estimation/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI entry point
│   ├── detector.py      # YOLOv8 detection logic
│   ├── tracker.py       # Bird tracking & counting
│   └── weight.py        # Weight estimation logic
│
│
├── models/
│   └── yolov8n.pt       # YOLOv8 model weights
│
├── outputs/
│   ├── annotated_video.mp4
│   └── sample_response.json
│
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/vamsi-sys/bird-counting-weight-estimation.git
cd bird-counting-weight-estimation

2️⃣ Create and activate virtual environment
python -m venv venv


Windows

venv\Scripts\activate


Linux / Mac

source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ Running the Application

Start the FastAPI server:

uvicorn app.main:app --reload


Server will run at:

http://127.0.0.1:8000

🔌 API Usage
Endpoint: Analyze Video

POST /analyze-video

Example using curl
curl -X POST "http://127.0.0.1:8000/analyze-video" \
     -F "file=@data/poultry.mp4"
     
🎗️🎗️### Health Check
GET /health

Response:
{
  "status": "ok"
}

📤 Sample JSON Response
{
  "frames_processed": 1243,
  "unique_birds": 56,
  "counts_over_time": [
    { "time_sec": 0, "count": 12 },
    { "time_sec": 5, "count": 21 },
    { "time_sec": 10, "count": 34 }
  ],
  "tracks_sample": [
    { "id": 3, "bbox": [120.5, 45.2, 200.1, 180.6] },
    { "id": 7, "bbox": [310.4, 90.8, 420.2, 230.1] }
  ],
  "weight_estimation": {
    "average_grams": 1450.3,
    "min_grams": 1200.7,
    "max_grams": 1805.9
  },
  "processing_time_sec": 289.4,
  "fps": 4.3,
  "annotated_video": "outputs/annotated_video.mp4"
}
Note: Weight values are proxy-based estimates derived from bounding-box area and represent relative scale, not calibrated physical measurements.

🧠 How It Works

Detection

YOLOv8 detects birds frame-by-frame

Tracking

Tracks objects across frames to ensure unique counting

Weight Estimation

Uses bounding-box area heuristics for approximate weight

Output

Annotated video + structured JSON result

📌 Weight Estimation Design Note

Bird weight is estimated using bounding-box area as a proxy, which varies across frames due to movement and camera angle.
Weight estimation is heuristic and based on bounding-box area as a proxy for bird size.
Actual gram-level accuracy requires camera calibration or labeled training data.

To avoid misleading precision, the system reports **aggregated statistics**:
- Average estimated weight
- Minimum estimated weight
- Maximum estimated weight

Per-bird or per-frame weights are intentionally not exposed, as they are unstable without camera calibration.
• ⭐⭐ Individual bird weights are not exported to avoid frame-level estimation noise

## Performance Optimizations
- Model warm-up at startup to avoid first-request latency
- Frame skipping to reduce inference load
- Frame resizing for faster processing

📦 Outputs

🎥 outputs/annotated_video.mp4
→ Video with bounding boxes, IDs, and counts

📄 outputs/sample_response.json
→ Machine-readable analytics output

🧪 Limitations & Assumptions

Weight estimation is approximate, not medical-grade

Designed for top-view or angled farm videos

Model accuracy depends on video quality and lighting

🔮 Future Improvements

Calibration-based weight estimation

Support for live RTSP camera feeds

Model fine-tuning on poultry-specific datasets

Database integration for long-term analytics

Dockerized deployment

🧾 License

This project is released under the MIT License.
You are free to use, modify, and distribute it.

👤 Author

Vamsikrishna Sirimalla
GitHub: https://github.com/vamsi-sys

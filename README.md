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

🎯 YOLOv8-based bird detection

🔁 Object tracking to avoid double counting

⚖️ Heuristic weight estimation per bird

🎥 Annotated output video

🌐 REST API built with FastAPI

📄 Clean JSON response for downstream usage

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
├── data/
│   └── poultry.mp4      # Sample input video
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

📤 Sample JSON Response
{
  "frames_processed": 620,
  "unique_birds_detected": 47,
  "average_weight_kg": 2.1,
  "bird_weights": [
    { "id": 1, "estimated_weight": 2.0 },
    { "id": 2, "estimated_weight": 2.3 }
  ],
  "output_video": "outputs/annotated_video.mp4"
}

🧠 How It Works

Detection

YOLOv8 detects birds frame-by-frame

Tracking

Tracks objects across frames to ensure unique counting

Weight Estimation

Uses bounding-box area heuristics for approximate weight

Output

Annotated video + structured JSON result

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

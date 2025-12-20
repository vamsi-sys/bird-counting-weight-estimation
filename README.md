# Bird Counting & Weight Estimation from CCTV Video

## Overview
This project is a prototype system that analyzes fixed-camera poultry CCTV videos to:
- Count birds over time using detection and tracking
- Estimate bird weight from video using a proxy method
- Generate annotated video outputs
- Expose results via a minimal FastAPI service

The solution is designed for ML evaluation and demonstrates practical handling of detection, tracking, analytics, and API design.

---

## Features
- Bird detection using YOLOv8
- Stable bird tracking with unique IDs (prevents double counting)
- Bird count over time (timestamp → count)
- Weight estimation using bounding-box area proxy
- Annotated output video with bounding boxes, IDs, and count overlay
- FastAPI-based inference service
- Performance optimizations (frame skipping, resizing, model warm-up)

---

## Tech Stack
- Python 3.10
- Ultralytics YOLOv8
- ByteTrack (via YOLO tracking)
- OpenCV
- FastAPI

---

## Setup Instructions

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Run the API
bash
Copy code
python -m uvicorn app.main:app --reload
The server will start at:

cpp
Copy code
http://127.0.0.1:8000
API Endpoints
Health Check
bash
Copy code
GET /health
Response:

json
Copy code
{ "status": "ok" }
Analyze Video
bash
Copy code
POST /analyze-video
Request

Content-Type: multipart/form-data

Key: file

Value: CCTV video file (.mp4, .avi, .mov)

Sample Response

json
Copy code
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
  "processing_time_sec": 289.4,
  "fps": 4.3,
  "annotated_video": "outputs/annotated_video.mp4"
}


Bird Counting Method
Birds are detected in each frame using YOLOv8.

Tracking IDs are assigned using ByteTrack.

Unique tracking IDs ensure birds are not double-counted.

Occlusions and temporary disappearances are handled via tracker persistence.

Weight Estimation Method
Weight is estimated using bounding-box area as a proxy for bird body size.

Larger bounding box → larger estimated weight.

This produces a relative weight index.

To convert estimates to true grams accurately, additional data is required:

Camera calibration (distance, height, focal length), or

Labeled bird weights to train a regression model.

Outputs
Annotated video with bounding boxes, tracking IDs, and live count overlay

JSON response with counts, tracks sample, and weight estimates

Notes
This is a prototype ML system designed for evaluation purposes.
Accuracy can be improved using depth estimation, multi-camera setups, or supervised weight regression models.
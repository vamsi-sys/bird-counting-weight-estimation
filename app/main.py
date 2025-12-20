from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import time

from .tracker import BirdTracker

app = FastAPI(title="Bird Counting & Weight Estimation API")

tracker = BirdTracker()

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------- HEALTH CHECK ----------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------- MODEL WARM-UP ----------------
@app.on_event("startup")
def warmup_model():
    print("Warming up YOLO model...")
    tracker.load_model()
    print("YOLO model ready.")


# ---------------- ANALYZE VIDEO ----------------
@app.post("/analyze-video")
def analyze_video(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".mp4", ".avi", ".mov")):
        raise HTTPException(status_code=400, detail="Unsupported video format")

    video_path = UPLOAD_DIR / file.filename

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    start_time = time.time()

    result = tracker.analyze_video(
        video_path=str(video_path),
        output_dir=str(OUTPUT_DIR)
    )

    elapsed = time.time() - start_time

    return {
        "frames_processed": result["frames_processed"],
        "unique_birds": result["unique_birds"],
        "counts_over_time": result["counts_over_time"],
        "tracks_sample": result["tracks_sample"],
        "weight_estimation": result["weight_estimation"],
        "processing_time_sec": round(elapsed, 2),
        "fps": round(result["frames_processed"] / elapsed, 2),
        "annotated_video": str(OUTPUT_DIR / "annotated_video.mp4")
    }

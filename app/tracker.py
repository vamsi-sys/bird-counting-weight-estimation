import cv2
from ultralytics import YOLO
from pathlib import Path

from .weight import WeightEstimator


class BirdTracker:
    def __init__(self):
        self.model = None
        self.weight_estimator = WeightEstimator()

        # Performance settings
        self.frame_skip = 2        # process every 2nd frame
        self.resize_width = 640    # resize for faster inference

    def load_model(self):
        if self.model is None:
            self.model = YOLO("models/yolov8n.pt")

    def analyze_video(self, video_path: str, output_dir: str):
        self.load_model()

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError("Unable to open video")

        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        output_video_path = output_dir / "annotated_video.mp4"

        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25

        writer = cv2.VideoWriter(
            str(output_video_path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (original_width, original_height)
        )

        frame_idx = 0
        processed_frames = 0
        unique_ids = set()
        bird_boxes = {}

        # ---- count over time ----
        counts_over_time = []
        sample_interval_sec = 5
        last_recorded_sec = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx += 1

            if frame_idx % self.frame_skip != 0:
                writer.write(frame)
                continue

            processed_frames += 1

            current_time_sec = int(frame_idx / fps)
            if current_time_sec - last_recorded_sec >= sample_interval_sec:
                counts_over_time.append({
                    "time_sec": current_time_sec,
                    "count": len(unique_ids)
                })
                last_recorded_sec = current_time_sec

            scale = self.resize_width / frame.shape[1]
            resized = cv2.resize(
                frame,
                (self.resize_width, int(frame.shape[0] * scale))
            )

            results = self.model.track(
                resized,
                persist=True,
                conf=0.4,
                verbose=False
            )

            if not results or results[0].boxes.id is None:
                writer.write(frame)
                continue

            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy()

            for box, track_id in zip(boxes, track_ids):
                track_id = int(track_id)
                box = box / scale

                if track_id not in bird_boxes:
                    bird_boxes[track_id] = box
                    unique_ids.add(track_id)

                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"Bird {track_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            cv2.putText(
                frame,
                f"Count: {len(unique_ids)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )

            writer.write(frame)

        cap.release()
        writer.release()

        # ---- weight estimation ----
        weights = []
        for bbox in bird_boxes.values():
            weights.append(self.weight_estimator.estimate_weight(bbox))

        weight_stats = self.weight_estimator.aggregate(weights)

        # ---- tracks sample ----
        tracks_sample = []
        for track_id, bbox in list(bird_boxes.items())[:10]:
            tracks_sample.append({
                "id": track_id,
                "bbox": [round(float(x), 2) for x in bbox]
            })

        return {
            "frames_processed": processed_frames,
            "unique_birds": len(unique_ids),
            "counts_over_time": counts_over_time,
            "tracks_sample": tracks_sample,
            "weight_estimation": weight_stats
        }

import numpy as np


class WeightEstimator:
    def __init__(self):
        # Calibration constants (heuristic)
        self.base_area = 5000        # pixels
        self.base_weight = 1200      # grams

    def estimate_weight(self, bbox):
        """
        Estimate weight from bounding box.
        bbox: (x1, y1, x2, y2)
        """
        x1, y1, x2, y2 = bbox
        area = max((x2 - x1) * (y2 - y1), 1)

        weight = (area / self.base_area) * self.base_weight
        return round(weight, 2)

    def aggregate(self, weights):
        if not weights:
            return None

        return {
            "average_grams": round(float(np.mean(weights)), 2),
            "min_grams": round(float(np.min(weights)), 2),
            "max_grams": round(float(np.max(weights)), 2),
        }

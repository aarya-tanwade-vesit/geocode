import time
import json
import math
import numpy as np

class PerformanceEvaluator:
    """Calculates PAT tracking metrics, latency, and exports logs."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = time.time()
        self.acquisition_time = None
        self.errors = []
        self.frame_times = []
        self.lock_count = 0
        self.total_count = 0

    def update(self, detected: bool, error_x: float, error_y: float, frame_time_ms: float):
        """Updates frame metrics."""
        self.total_count += 1
        self.frame_times.append(frame_time_ms)
        
        radial_error = math.sqrt(error_x**2 + error_y**2)
        self.errors.append(radial_error)

        if detected:
            self.lock_count += 1
            if self.acquisition_time is None and radial_error < 15.0:
                self.acquisition_time = time.time() - self.start_time

    def get_summary(self):
        """Returns performance metrics summary."""
        mean_err = float(np.mean(self.errors)) if self.errors else 0.0
        max_err = float(np.max(self.errors)) if self.errors else 0.0
        lock_rate = float((self.lock_count / max(1, self.total_count)) * 100.0)
        avg_fps = float(1000.0 / max(0.1, np.mean(self.frame_times))) if self.frame_times else 0.0

        return {
            "acquisition_time_s": round(self.acquisition_time, 3) if self.acquisition_time else "N/A",
            "mean_pointing_error_px": round(mean_err, 2),
            "max_pointing_error_px": round(max_err, 2),
            "lock_retention_rate_pct": round(lock_rate, 1),
            "avg_fps": round(avg_fps, 1),
            "total_frames": self.total_count
        }

    def save_log(self, filepath: str):
        """Saves evaluation metrics summary to JSON log."""
        summary = self.get_summary()
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        return summary

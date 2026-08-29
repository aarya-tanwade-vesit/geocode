import math
import numpy as np

class PlatformDisturbance:
    """Base class for platform and camera orientation/position disturbances."""
    def get_offset(self, t: float) -> np.ndarray:
        raise NotImplementedError

class VibrationGenerator(PlatformDisturbance):
    """High-frequency sinusoidal and jitter vibration model (pan/tilt or position)."""
    def __init__(self, frequency_hz=15.0, amplitude=0.05, harmonics=3, seed=42):
        self.freq = float(frequency_hz)
        self.amp = float(amplitude)
        self.harmonics = harmonics
        self.rng = np.random.default_rng(seed)
        # Random phases for x, y, z harmonics
        self.phases = self.rng.uniform(0, 2 * math.pi, size=(harmonics, 3))

    def get_offset(self, t: float) -> np.ndarray:
        offset = np.zeros(3, dtype=np.float64)
        for h in range(1, self.harmonics + 1):
            w = 2 * math.pi * self.freq * h
            amplitude = self.amp / h
            offset[0] += amplitude * math.sin(w * t + self.phases[h-1, 0])
            offset[1] += amplitude * math.cos(w * t + self.phases[h-1, 1])
            offset[2] += (amplitude * 0.5) * math.sin(w * t + self.phases[h-1, 2])
        return offset

class MotionDisturbance(PlatformDisturbance):
    """Low-frequency wind sway or platform drift disturbance."""
    def __init__(self, drift_freq=0.2, drift_amp=0.2):
        self.drift_freq = float(drift_freq)
        self.drift_amp = float(drift_amp)

    def get_offset(self, t: float) -> np.ndarray:
        w = 2 * math.pi * self.drift_freq
        dx = self.drift_amp * math.sin(w * t)
        dy = self.drift_amp * math.sin(w * 0.7 * t + 0.5)
        dz = (self.drift_amp * 0.2) * math.cos(w * 0.5 * t)
        return np.array([dx, dy, dz], dtype=np.float64)

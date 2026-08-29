import cv2
import numpy as np

class ImageDegradation:
    """Base class for visual camera frame disturbances."""
    def apply(self, frame: np.ndarray) -> np.ndarray:
        raise NotImplementedError

class AdditiveGaussianNoise(ImageDegradation):
    """Synthetic sensor electronic noise (Gaussian)."""
    def __init__(self, std_dev=10.0, seed=None):
        self.std_dev = float(std_dev)
        self.rng = np.random.default_rng(seed)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        if self.std_dev <= 0:
            return frame
        noise = self.rng.normal(0, self.std_dev, frame.shape).astype(np.float32)
        noisy_frame = np.clip(frame.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        return noisy_frame

class SaltAndPepperNoise(ImageDegradation):
    """Impulsive salt-and-pepper noise simulating bad camera sensor pixels."""
    def __init__(self, prob=0.005, seed=None):
        self.prob = float(prob)
        self.rng = np.random.default_rng(seed)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        if self.prob <= 0:
            return frame
        out = frame.copy()
        num_salt = int(np.ceil(self.prob * frame.size * 0.5))
        # Salt (white pixels)
        coords = [self.rng.integers(0, i - 1, num_salt) for i in frame.shape[:2]]
        out[tuple(coords)] = 255
        # Pepper (black pixels)
        coords = [self.rng.integers(0, i - 1, num_salt) for i in frame.shape[:2]]
        out[tuple(coords)] = 0
        return out

class VibrationBlur(ImageDegradation):
    """Linear/directional motion blur simulating camera vibration."""
    def __init__(self, kernel_size=5, angle_deg=45.0):
        self.kernel_size = max(1, int(kernel_size))
        if self.kernel_size % 2 == 0:
            self.kernel_size += 1
        self.angle_deg = angle_deg

    def apply(self, frame: np.ndarray) -> np.ndarray:
        if self.kernel_size <= 1:
            return frame
        # Create directional motion blur kernel
        kernel = np.zeros((self.kernel_size, self.kernel_size), dtype=np.float32)
        center = self.kernel_size // 2
        rad = np.deg2rad(self.angle_deg)
        dx = np.cos(rad)
        dy = np.sin(rad)
        for i in range(self.kernel_size):
            offset = i - center
            x = int(round(center + offset * dx))
            y = int(round(center + offset * dy))
            if 0 <= x < self.kernel_size and 0 <= y < self.kernel_size:
                kernel[y, x] = 1.0
        kernel /= np.sum(kernel)
        blurred_frame = cv2.filter2D(frame, -1, kernel)
        return blurred_frame

class AtmosphericTurbulence(ImageDegradation):
    """Approximation of atmospheric optical turbulence (thermal distortion + scintillation)."""
    def __init__(self, strength=0.3, seed=None):
        self.strength = float(strength)
        self.rng = np.random.default_rng(seed)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        if self.strength <= 0:
            return frame
        h, w = frame.shape[:2]
        # Generate low-frequency random displacement field
        grid_x, grid_y = np.meshgrid(np.arange(w), np.arange(h))
        disp_scale = self.strength * 5.0
        
        # Sub-sampled noise map for smooth spatial phase perturbation
        low_res = (max(4, h // 32), max(4, w // 32))
        dx_low = self.rng.normal(0, disp_scale, low_res).astype(np.float32)
        dy_low = self.rng.normal(0, disp_scale, low_res).astype(np.float32)
        
        dx = cv2.resize(dx_low, (w, h), interpolation=cv2.INTER_CUBIC)
        dy = cv2.resize(dy_low, (w, h), interpolation=cv2.INTER_CUBIC)
        
        map_x = (grid_x + dx).astype(np.float32)
        map_y = (grid_y + dy).astype(np.float32)
        
        distorted = cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return distorted

class VisibilityDegradation(ImageDegradation):
    """Simulates fog/cloud contrast attenuation and temporary occlusion dropouts."""
    def __init__(self, visibility=1.0, occlusion=False):
        self.visibility = float(visibility)  # 1.0 = clear, 0.0 = total fog
        self.occlusion = occlusion

    def apply(self, frame: np.ndarray) -> np.ndarray:
        if self.occlusion:
            # Completely black out / occlude target frame
            return np.zeros_like(frame)
        if self.visibility >= 1.0:
            return frame
        # Blend frame towards mid-gray (fog simulation)
        gray = np.full_like(frame, 128, dtype=np.uint8)
        alpha = self.visibility
        degraded = cv2.addWeighted(frame, alpha, gray, 1.0 - alpha, 0)
        return degraded

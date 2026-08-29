import math
import cv2
import numpy as np

class Virtual3DEnvironment:
    """
    Standalone 3D Virtual FSOC Simulator Engine.
    Renders 3D optical beacon projection on virtual camera focal plane.
    """
    def __init__(self, width=640, height=480, fov_deg=60.0):
        self.width = width
        self.height = height
        self.fov_deg = fov_deg

        # Camera Intrinsic Matrix (Pinhole model)
        focal_length = (width / 2.0) / math.tan(math.radians(fov_deg / 2.0))
        self.cx = width / 2.0
        self.cy = height / 2.0
        self.K = np.array([
            [focal_length, 0, self.cx],
            [0, focal_length, self.cy],
            [0, 0, 1]
        ], dtype=np.float64)

        # Camera Gimbal state (Pan, Tilt in degrees)
        self.pan_deg = 0.0
        self.tilt_deg = 0.0
        self.camera_pos = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    def update_gimbal(self, delta_pan: float, delta_tilt: float):
        """Applies Pan/Tilt control inputs."""
        self.pan_deg += delta_pan
        self.tilt_deg += delta_tilt
        # Clamp tilt between -85 and +85 deg
        self.tilt_deg = max(-85.0, min(85.0, self.tilt_deg))

    def render_frame(self, target_3d_pos: np.ndarray, platform_offset: np.ndarray = None) -> np.ndarray:
        """
        Projects 3D beacon position onto camera 2D image plane.
        """
        # Create dark atmospheric background frame
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # Deep space / sky background
        frame[:, :] = (15, 10, 25)

        # Apply platform vibration / motion offset to camera position
        cam_pos = self.camera_pos.copy()
        if platform_offset is not None:
            cam_pos += platform_offset

        # Vector from camera to target in world coordinates
        rel_pos = target_3d_pos - cam_pos

        # Rotation matrices for Pan (heading) and Tilt (pitch)
        pan_rad = math.radians(self.pan_deg)
        tilt_rad = math.radians(self.tilt_deg)

        R_pan = np.array([
            [math.cos(pan_rad), 0, math.sin(pan_rad)],
            [0, 1, 0],
            [-math.sin(pan_rad), 0, math.cos(pan_rad)]
        ])

        R_tilt = np.array([
            [1, 0, 0],
            [0, math.cos(tilt_rad), -math.sin(tilt_rad)],
            [0, math.sin(tilt_rad), math.cos(tilt_rad)]
        ])

        R_cam = R_tilt @ R_pan
        
        # Transform position to camera space
        pos_cam = R_cam @ rel_pos
        x_c, y_c, z_c = pos_cam[0], pos_cam[1], pos_cam[2]

        # Target is behind camera
        if z_c <= 0.1:
            return frame

        # Perspective projection onto 2D focal plane
        uv = self.K @ np.array([x_c, y_c, z_c])
        u = uv[0] / uv[2]
        v = uv[1] / uv[2]

        u_pixel = int(round(u))
        v_pixel = int(round(v))

        # Check if beacon is inside FOV frame
        if 0 <= u_pixel < self.width and 0 <= v_pixel < self.height:
            # Draw bright laser optical beacon spot with outer glow halo
            intensity = max(50, min(255, int(255 * (100.0 / z_c))))
            
            # Halo glow
            cv2.circle(frame, (u_pixel, v_pixel), 12, (0, int(intensity * 0.4), int(intensity * 0.8)), -1)
            cv2.circle(frame, (u_pixel, v_pixel), 6, (100, 200, 255), -1)
            # Bright central core
            cv2.circle(frame, (u_pixel, v_pixel), 2, (255, 255, 255), -1)

        # Render crosshair reference at camera center
        center_x, center_y = int(self.cx), int(self.cy)
        cv2.line(frame, (center_x - 15, center_y), (center_x + 15, center_y), (0, 255, 0), 1)
        cv2.line(frame, (center_x, center_y - 15), (center_x, center_y + 15), (0, 255, 0), 1)

        return frame

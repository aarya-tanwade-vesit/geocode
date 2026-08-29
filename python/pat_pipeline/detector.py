import cv2
import numpy as np

class BeaconDetector:
    """OpenCV Beacon Detector for FSOC Optical Terminals."""
    def __init__(self, lower_hsv=(0, 0, 200), upper_hsv=(180, 50, 255), min_area=5):
        self.lower_hsv = np.array(lower_hsv, dtype=np.uint8)
        self.upper_hsv = np.array(upper_hsv, dtype=np.uint8)
        self.min_area = min_area

    def detect(self, frame: np.ndarray):
        """
        Detects bright optical beacon in frame.
        Returns:
            dict containing:
                detected (bool)
                x (float)
                y (float)
                confidence (float)
                bbox (tuple)
        """
        if frame is None or frame.size == 0:
            return {"detected": False, "x": 0.0, "y": 0.0, "confidence": 0.0, "bbox": None}

        # Convert to HSV and grayscale for intensity blob detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        
        # Additional brightness thresholding for bright beacon spots
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, bright_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
        combined_mask = cv2.bitwise_or(mask, bright_mask)

        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return {"detected": False, "x": 0.0, "y": 0.0, "confidence": 0.0, "bbox": None}

        # Find largest contour
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area < self.min_area:
            return {"detected": False, "x": 0.0, "y": 0.0, "confidence": 0.0, "bbox": None}

        M = cv2.moments(c)
        if M["m00"] == 0:
            return {"detected": False, "x": 0.0, "y": 0.0, "confidence": 0.0, "bbox": None}

        cx = float(M["m10"] / M["m00"])
        cy = float(M["m01"] / M["m00"])
        x, y, w, h = cv2.boundingRect(c)

        # Confidence based on blob area and intensity ratio
        confidence = min(1.0, float(area / 100.0) + 0.5)

        return {
            "detected": True,
            "x": cx,
            "y": cy,
            "confidence": confidence,
            "bbox": (x, y, w, h)
        }

import cv2
import numpy as np

class KalmanTracker:
    """Constant Velocity 2D/3D Kalman Filter for smooth target prediction and recovery."""
    def __init__(self, dt=0.033):
        self.dt = dt
        # State vector [x, y, vx, vy]
        self.kf = cv2.KalmanFilter(4, 2)
        
        # State Transition Matrix (A)
        self.kf.transitionMatrix = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1,  0],
            [0, 0, 0,  1]
        ], dtype=np.float32)

        # Measurement Matrix (H)
        self.kf.measurementMatrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=np.float32)

        # Process Noise Covariance (Q)
        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 1e-2
        
        # Measurement Noise Covariance (R)
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 1e-1

        # Post Error Covariance (P)
        self.kf.errorCovPost = np.eye(4, dtype=np.float32)

        self.initialized = False
        self.missed_frames = 0

    def update(self, detected: bool, measured_x: float, measured_y: float):
        """
        Predicts and corrects target position.
        Returns:
            estimated_x, estimated_y, predicted_vx, predicted_vy
        """
        # 1. Prediction step
        prediction = self.kf.predict()
        pred_x, pred_y = float(prediction[0][0]), float(prediction[1][0])
        pred_vx, pred_vy = float(prediction[2][0]), float(prediction[3][0])

        if not detected:
            self.missed_frames += 1
            # Return prediction during target loss
            return pred_x, pred_y, pred_vx, pred_vy

        # Reset missed frames on detection
        self.missed_frames = 0

        measurement = np.array([[np.float32(measured_x)], [np.float32(measured_y)]])

        if not self.initialized:
            self.kf.statePost = np.array([
                [np.float32(measured_x)],
                [np.float32(measured_y)],
                [0.0],
                [0.0]
            ], dtype=np.float32)
            self.initialized = True
            return measured_x, measured_y, 0.0, 0.0

        # 2. Correction step
        corrected = self.kf.correct(measurement)
        est_x, est_y = float(corrected[0][0]), float(corrected[1][0])
        est_vx, est_vy = float(corrected[2][0]), float(corrected[3][0])

        return est_x, est_y, est_vx, est_vy

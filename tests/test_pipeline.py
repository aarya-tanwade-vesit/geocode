import unittest
import numpy as np
import cv2

from python.simulator3d import Virtual3DEnvironment
from python.pat_pipeline import BeaconDetector, KalmanTracker, PIDController
from evaluation.metrics import PerformanceEvaluator
from python.disturbances import ScenarioManager

class TestFullPATPipeline(unittest.TestCase):

    def test_detector(self):
        detector = BeaconDetector()
        # Blank dark image
        blank = np.zeros((480, 640, 3), dtype=np.uint8)
        res_blank = detector.detect(blank)
        self.assertFalse(res_blank["detected"])

        # Image with bright white spot at center (320, 240)
        spot_img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.circle(spot_img, (320, 240), 10, (255, 255, 255), -1)
        res_spot = detector.detect(spot_img)
        self.assertTrue(res_spot["detected"])
        self.assertAlmostEqual(res_spot["x"], 320.0, delta=2.0)
        self.assertAlmostEqual(res_spot["y"], 240.0, delta=2.0)

    def test_kalman_tracker(self):
        tracker = KalmanTracker(dt=0.033)
        x1, y1, _, _ = tracker.update(True, 100.0, 100.0)
        self.assertEqual(x1, 100.0)
        self.assertEqual(y1, 100.0)

        # Loss of detection - prediction step
        x2, y2, _, _ = tracker.update(False, 0.0, 0.0)
        self.assertIsNotNone(x2)
        self.assertIsNotNone(y2)

    def test_pid_controller(self):
        controller = PIDController(kp=0.1, ki=0.01, kd=0.01)
        pan, tilt = controller.compute(10.0, -5.0, dt=0.033)
        self.assertNotEqual(pan, 0.0)
        self.assertNotEqual(tilt, 0.0)

    def test_3d_simulator_render(self):
        sim = Virtual3DEnvironment()
        target_pos = np.array([0.0, 0.0, 100.0])
        frame = sim.render_frame(target_pos)
        self.assertEqual(frame.shape, (480, 640, 3))

    def test_evaluator(self):
        evaluator = PerformanceEvaluator()
        evaluator.update(True, 2.0, 3.0, 10.0)
        summary = evaluator.get_summary()
        self.assertEqual(summary["total_frames"], 1)
        self.assertGreater(summary["lock_retention_rate_pct"], 0)

    def test_full_loop(self):
        sim = Virtual3DEnvironment()
        detector = BeaconDetector()
        tracker = KalmanTracker()
        controller = PIDController()
        evaluator = PerformanceEvaluator()
        scen_mgr = ScenarioManager()

        scen = scen_mgr.load_scenario("moving_target")
        motion = scen["motion"]

        for step in range(10):
            t = step * 0.033
            pos = motion.get_position(t)
            frame = sim.render_frame(pos)
            det = detector.detect(frame)
            est_x, est_y, _, _ = tracker.update(det["detected"], det["x"], det["y"])
            err_x = est_x - sim.cx if det["detected"] else 0.0
            err_y = est_y - sim.cy if det["detected"] else 0.0
            pan, tilt = controller.compute(err_x, err_y)
            sim.update_gimbal(pan, tilt)
            evaluator.update(det["detected"], err_x, err_y, 15.0)

        summary = evaluator.get_summary()
        self.assertEqual(summary["total_frames"], 10)

if __name__ == "__main__":
    unittest.main()

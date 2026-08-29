import unittest
import numpy as np

from python.disturbances.target_motion import LinearMotion, CircularMotion, WaypointMotion, SuddenManeuver
from python.disturbances.platform_disturbances import VibrationGenerator, MotionDisturbance
from python.disturbances.image_degradation import (
    AdditiveGaussianNoise, 
    SaltAndPepperNoise, 
    VibrationBlur, 
    AtmosphericTurbulence,
    VisibilityDegradation
)
from python.disturbances.scenarios import ScenarioManager

class TestMotionAndDisturbances(unittest.TestCase):

    def test_linear_motion(self):
        motion = LinearMotion(initial_position=(0, 0, 100), velocity=(1, 2, 3))
        pos_t0 = motion.get_position(0.0)
        pos_t2 = motion.get_position(2.0)
        
        np.testing.assert_array_almost_equal(pos_t0, [0, 0, 100])
        np.testing.assert_array_almost_equal(pos_t2, [2, 4, 106])

    def test_circular_motion(self):
        motion = CircularMotion(center=(0, 0, 50), radius=10.0, angular_velocity=np.pi)
        pos_t0 = motion.get_position(0.0)
        pos_t1 = motion.get_position(1.0)
        
        np.testing.assert_array_almost_equal(pos_t0, [10, 0, 50])
        np.testing.assert_array_almost_equal(pos_t1, [-10, 0, 50], decimal=5)

    def test_waypoint_motion(self):
        waypoints = [(0, 0, 0), (10, 0, 0), (10, 10, 0)]
        speeds = [5.0, 5.0]
        motion = WaypointMotion(waypoints, speeds)
        
        pos_t0 = motion.get_position(0.0)
        pos_t1 = motion.get_position(1.0)  # midpoint of segment 1
        pos_t2 = motion.get_position(2.0)  # end of segment 1 / start of 2
        
        np.testing.assert_array_almost_equal(pos_t0, [0, 0, 0])
        np.testing.assert_array_almost_equal(pos_t1, [5, 0, 0])
        np.testing.assert_array_almost_equal(pos_t2, [10, 0, 0])

    def test_sudden_maneuver(self):
        base = LinearMotion(initial_position=(0, 0, 0), velocity=(1, 0, 0))
        maneuver = SuddenManeuver(base, maneuver_time=2.0, impulse_vector=(0, 5, 0))
        
        pos_before = maneuver.get_position(1.0)
        pos_after = maneuver.get_position(3.0)
        
        np.testing.assert_array_almost_equal(pos_before, [1, 0, 0])
        np.testing.assert_array_almost_equal(pos_after, [3, 5, 0])

    def test_vibration_generator(self):
        vib = VibrationGenerator(frequency_hz=10.0, amplitude=0.5, seed=123)
        off_t0 = vib.get_offset(0.0)
        off_t05 = vib.get_offset(0.05)
        
        self.assertEqual(len(off_t0), 3)
        self.assertFalse(np.array_equal(off_t0, off_t05))

    def test_image_degradation(self):
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 128
        
        noise_filter = AdditiveGaussianNoise(std_dev=15.0, seed=42)
        sp_filter = SaltAndPepperNoise(prob=0.01, seed=42)
        blur_filter = VibrationBlur(kernel_size=5, angle_deg=45.0)
        turb_filter = AtmosphericTurbulence(strength=0.3, seed=42)
        vis_filter = VisibilityDegradation(visibility=0.5)
        occl_filter = VisibilityDegradation(occlusion=True)
        
        noisy_frame = noise_filter.apply(frame)
        sp_frame = sp_filter.apply(frame)
        blurred_frame = blur_filter.apply(frame)
        turbulent_frame = turb_filter.apply(frame)
        foggy_frame = vis_filter.apply(frame)
        occluded_frame = occl_filter.apply(frame)
        
        self.assertEqual(noisy_frame.shape, frame.shape)
        self.assertEqual(sp_frame.shape, frame.shape)
        self.assertEqual(blurred_frame.shape, frame.shape)
        self.assertEqual(turbulent_frame.shape, frame.shape)
        self.assertEqual(foggy_frame.shape, frame.shape)
        self.assertEqual(occluded_frame.shape, frame.shape)
        
        self.assertFalse(np.array_equal(frame, noisy_frame))
        self.assertFalse(np.array_equal(frame, sp_frame))
        self.assertTrue(np.all(occluded_frame == 0))

    def test_scenario_manager(self):
        manager = ScenarioManager()
        scen_vib = manager.load_scenario("high_vibration")
        scen_loss = manager.load_scenario("target_loss_and_recovery")
        
        self.assertIn("motion", scen_vib)
        self.assertIn("platform", scen_vib)
        self.assertIn("image_filters", scen_vib)
        self.assertIn("motion", scen_loss)

if __name__ == "__main__":
    unittest.main()

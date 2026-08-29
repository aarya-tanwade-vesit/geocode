import json
import numpy as np

from .target_motion import LinearMotion, CircularMotion, WaypointMotion, SuddenManeuver
from .platform_disturbances import VibrationGenerator, MotionDisturbance
from .image_degradation import AdditiveGaussianNoise, SaltAndPepperNoise, VibrationBlur, AtmosphericTurbulence, VisibilityDegradation

class ScenarioManager:
    """Manages predefined test scenarios for PAT testing."""
    def __init__(self, config_path=None):
        self.config = {}
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load config {config_path}: {e}")

    def load_scenario(self, scenario_name: str):
        """Returns target motion, platform disturbance, and image pipeline for scenario."""
        scenario_name = scenario_name.lower()
        if scenario_name == "no_disturbance":
            motion = LinearMotion(velocity=(1.0, 0.5, 0.0))
            platform = None
            image_filters = []

        elif scenario_name == "moving_target":
            motion = CircularMotion(radius=15.0, angular_velocity=0.8)
            platform = MotionDisturbance(drift_freq=0.1, drift_amp=0.1)
            image_filters = []

        elif scenario_name == "high_noise":
            motion = LinearMotion(velocity=(1.5, -0.5, 0.0))
            platform = None
            image_filters = [
                AdditiveGaussianNoise(std_dev=25.0),
                SaltAndPepperNoise(prob=0.01),
                AtmosphericTurbulence(strength=0.6)
            ]

        elif scenario_name == "high_vibration":
            motion = LinearMotion(velocity=(0.5, 0.5, 0.0))
            platform = VibrationGenerator(frequency_hz=20.0, amplitude=0.15)
            image_filters = [
                VibrationBlur(kernel_size=9, angle_deg=30.0)
            ]

        elif scenario_name == "sudden_maneuver":
            base_motion = LinearMotion(velocity=(1.0, 0.0, 0.0))
            motion = SuddenManeuver(base_motion, maneuver_time=3.0, impulse_vector=(5.0, -4.0, 0.0))
            platform = VibrationGenerator(frequency_hz=10.0, amplitude=0.05)
            image_filters = [
                AdditiveGaussianNoise(std_dev=10.0)
            ]

        elif scenario_name in ("target_loss_and_recovery", "target_loss"):
            motion = LinearMotion(velocity=(1.0, 0.5, 0.0))
            platform = MotionDisturbance(drift_freq=0.2, drift_amp=0.1)
            image_filters = [
                VisibilityDegradation(visibility=0.4, occlusion=False),
                AdditiveGaussianNoise(std_dev=12.0)
            ]

        else:
            raise ValueError(f"Unknown scenario preset: {scenario_name}")

        return {
            "motion": motion,
            "platform": platform,
            "image_filters": image_filters
        }

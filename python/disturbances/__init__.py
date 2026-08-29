"""
Disturbances and Motion Module for FSOC Virtual Camera PAT System.
Developed by Tanay.
"""

from .target_motion import TargetMotion, LinearMotion, CircularMotion, WaypointMotion, SuddenManeuver
from .platform_disturbances import PlatformDisturbance, VibrationGenerator, MotionDisturbance
from .image_degradation import (
    ImageDegradation, 
    AdditiveGaussianNoise, 
    SaltAndPepperNoise,
    VibrationBlur, 
    AtmosphericTurbulence,
    VisibilityDegradation
)
from .scenarios import ScenarioManager

__all__ = [
    'TargetMotion',
    'LinearMotion',
    'CircularMotion',
    'WaypointMotion',
    'SuddenManeuver',
    'PlatformDisturbance',
    'VibrationGenerator',
    'MotionDisturbance',
    'ImageDegradation',
    'AdditiveGaussianNoise',
    'SaltAndPepperNoise',
    'VibrationBlur',
    'AtmosphericTurbulence',
    'VisibilityDegradation',
    'ScenarioManager'
]

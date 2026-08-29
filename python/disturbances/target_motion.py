import math
import numpy as np

class TargetMotion:
    """Base class for target kinematics."""
    def __init__(self, initial_position=(0.0, 0.0, 100.0)):
        self.initial_position = np.array(initial_position, dtype=np.float64)

    def get_position(self, t: float) -> np.ndarray:
        raise NotImplementedError

class LinearMotion(TargetMotion):
    """Linear target motion with configurable velocity."""
    def __init__(self, initial_position=(0.0, 0.0, 100.0), velocity=(1.0, 0.5, 0.0)):
        super().__init__(initial_position)
        self.velocity = np.array(velocity, dtype=np.float64)

    def get_position(self, t: float) -> np.ndarray:
        return self.initial_position + self.velocity * t

class CircularMotion(TargetMotion):
    """Circular trajectory around a focal center point."""
    def __init__(self, center=(0.0, 0.0, 100.0), radius=10.0, angular_velocity=0.5):
        super().__init__(center)
        self.radius = float(radius)
        self.w = float(angular_velocity)

    def get_position(self, t: float) -> np.ndarray:
        x = self.initial_position[0] + self.radius * math.cos(self.w * t)
        y = self.initial_position[1] + self.radius * math.sin(self.w * t)
        z = self.initial_position[2]
        return np.array([x, y, z], dtype=np.float64)

class WaypointMotion(TargetMotion):
    """3D trajectory interpolating across specified waypoints."""
    def __init__(self, waypoints, speeds):
        if len(waypoints) < 2:
            raise ValueError("At least 2 waypoints required.")
        self.waypoints = [np.array(wp, dtype=np.float64) for wp in waypoints]
        self.speeds = speeds

    def get_position(self, t: float) -> np.ndarray:
        # Linear piece-wise traversal
        total_time = 0.0
        for i in range(len(self.waypoints) - 1):
            p1 = self.waypoints[i]
            p2 = self.waypoints[i+1]
            dist = np.linalg.norm(p2 - p1)
            seg_time = dist / max(self.speeds[i], 1e-5)
            if t <= total_time + seg_time:
                alpha = (t - total_time) / seg_time
                return p1 + alpha * (p2 - p1)
            total_time += seg_time
        return self.waypoints[-1]

class SuddenManeuver(TargetMotion):
    """Base motion with sudden impulse step displacement at maneuver_time."""
    def __init__(self, base_motion: TargetMotion, maneuver_time: float, impulse_vector=(5.0, -3.0, 0.0)):
        self.base_motion = base_motion
        self.maneuver_time = float(maneuver_time)
        self.impulse = np.array(impulse_vector, dtype=np.float64)

    def get_position(self, t: float) -> np.ndarray:
        pos = self.base_motion.get_position(t)
        if t >= self.maneuver_time:
            # Add sudden step offset simulating abrupt evasive maneuver
            pos = pos + self.impulse * (t - self.maneuver_time)
        return pos

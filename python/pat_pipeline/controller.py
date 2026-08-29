class PIDController:
    """Proportional-Integral-Derivative Controller for Gimbal Pan/Tilt alignment."""
    def __init__(self, kp=0.1, ki=0.01, kd=0.02, max_output=10.0):
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        self.max_output = float(max_output)

        self.integral_x = 0.0
        self.integral_y = 0.0
        self.prev_error_x = 0.0
        self.prev_error_y = 0.0

    def compute(self, error_x: float, error_y: float, dt: float = 0.033):
        """
        Computes pan and tilt correction commands given pointing errors.
        """
        if dt <= 0:
            dt = 0.033

        # Proportional term
        p_x = self.kp * error_x
        p_y = self.kp * error_y

        # Integral term with anti-windup clamp
        self.integral_x += error_x * dt
        self.integral_y += error_y * dt
        self.integral_x = max(-self.max_output, min(self.max_output, self.integral_x))
        self.integral_y = max(-self.max_output, min(self.max_output, self.integral_y))
        
        i_x = self.ki * self.integral_x
        i_y = self.ki * self.integral_y

        # Derivative term
        d_x = self.kd * (error_x - self.prev_error_x) / dt
        d_y = self.kd * (error_y - self.prev_error_y) / dt

        self.prev_error_x = error_x
        self.prev_error_y = error_y

        pan_cmd = p_x + i_x + d_x
        tilt_cmd = p_y + i_y + d_y

        # Output saturation limits
        pan_cmd = max(-self.max_output, min(self.max_output, pan_cmd))
        tilt_cmd = max(-self.max_output, min(self.max_output, tilt_cmd))

        return pan_cmd, tilt_cmd

    def reset(self):
        self.integral_x = 0.0
        self.integral_y = 0.0
        self.prev_error_x = 0.0
        self.prev_error_y = 0.0

import sys
import time
import math
import cv2
import numpy as np

from PySide6 import QtCore, QtGui, QtWidgets

from python.disturbances import ScenarioManager
from python.simulator3d import Virtual3DEnvironment
from python.pat_pipeline import BeaconDetector, KalmanTracker, PIDController
from evaluation.metrics import PerformanceEvaluator

class PATDashboard(QtWidgets.QMainWindow):
    """Interactive Graphical Interface for FSOC PAT System Simulation."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI FSOC Virtual Camera PAT Simulator")
        self.resize(1100, 700)

        # Initialize Simulation Subsystems
        self.sim_engine = Virtual3DEnvironment(width=640, height=480, fov_deg=60.0)
        self.scenario_mgr = ScenarioManager()
        self.detector = BeaconDetector()
        self.tracker = KalmanTracker(dt=0.033)
        self.controller = PIDController(kp=0.05, ki=0.005, kd=0.01, max_output=5.0)
        self.evaluator = PerformanceEvaluator()

        self.scenario_name = "no_disturbance"
        self.load_current_scenario()

        self.sim_time = 0.0
        self.is_running = False

        self.setup_ui()

        # Animation Loop Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_simulation)

    def load_current_scenario(self):
        scen_data = self.scenario_mgr.load_scenario(self.scenario_name)
        self.target_motion = scen_data["motion"]
        self.platform_dist = scen_data["platform"]
        self.image_filters = scen_data["image_filters"]

    def setup_ui(self):
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QHBoxLayout(main_widget)

        # Left Column: Video Feed & Metrics
        left_layout = QtWidgets.QVBoxLayout()
        
        # Camera Feed Display Label
        self.feed_label = QtWidgets.QLabel()
        self.feed_label.setFixedSize(640, 480)
        self.feed_label.setStyleSheet("background-color: black; border: 2px solid #333;")
        left_layout.addWidget(self.feed_label)

        # Status & Metrics Display Bar
        self.metrics_label = QtWidgets.QLabel("Status: Stopped | Error: 0.0 px | Lock: 0.0% | FPS: 0")
        self.metrics_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00FFCC; padding: 5px;")
        left_layout.addWidget(self.metrics_label)

        main_layout.addLayout(left_layout, stretch=2)

        # Right Column: Controls & Dashboard Panels
        right_layout = QtWidgets.QVBoxLayout()

        # Controls Box
        ctrl_group = QtWidgets.QGroupBox("Simulation Controls")
        ctrl_layout = QtWidgets.QVBoxLayout()

        # Scenario Selector
        scen_h_layout = QtWidgets.QHBoxLayout()
        scen_h_layout.addWidget(QtWidgets.QLabel("Scenario Preset:"))
        self.scen_combo = QtWidgets.QComboBox()
        self.scen_combo.addItems([
            "no_disturbance",
            "moving_target",
            "high_noise",
            "high_vibration",
            "sudden_maneuver",
            "target_loss_and_recovery"
        ])
        self.scen_combo.currentTextChanged.connect(self.on_scenario_changed)
        scen_h_layout.addWidget(self.scen_combo)
        ctrl_layout.addLayout(scen_h_layout)

        # Action Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_start = QtWidgets.QPushButton("Start Simulation")
        self.btn_start.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 8px;")
        self.btn_start.clicked.connect(self.toggle_simulation)
        btn_layout.addWidget(self.btn_start)

        self.btn_reset = QtWidgets.QPushButton("Reset")
        self.btn_reset.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold; padding: 8px;")
        self.btn_reset.clicked.connect(self.reset_simulation)
        btn_layout.addWidget(self.btn_reset)
        ctrl_layout.addLayout(btn_layout)

        ctrl_group.setLayout(ctrl_layout)
        right_layout.addWidget(ctrl_group)

        # Telemetry Display Box
        telemetry_group = QtWidgets.QGroupBox("Live Telemetry")
        tele_layout = QtWidgets.QFormLayout()

        self.lbl_target_pos = QtWidgets.QLabel("[0.0, 0.0, 100.0]")
        self.lbl_cam_pan = QtWidgets.QLabel("0.0°")
        self.lbl_cam_tilt = QtWidgets.QLabel("0.0°")
        self.lbl_acq_time = QtWidgets.QLabel("N/A")
        self.lbl_mean_err = QtWidgets.QLabel("0.0 px")

        tele_layout.addRow("Target 3D Pos (x,y,z):", self.lbl_target_pos)
        tele_layout.addRow("Camera Pan Angle:", self.lbl_cam_pan)
        tele_layout.addRow("Camera Tilt Angle:", self.lbl_cam_tilt)
        tele_layout.addRow("Acquisition Time:", self.lbl_acq_time)
        tele_layout.addRow("Mean Pointing Error:", self.lbl_mean_err)

        telemetry_group.setLayout(tele_layout)
        right_layout.addWidget(telemetry_group)

        # Export Button
        self.btn_export = QtWidgets.QPushButton("Export Performance Logs")
        self.btn_export.clicked.connect(self.export_logs)
        right_layout.addWidget(self.btn_export)

        right_layout.addStretch()
        main_layout.addLayout(right_layout, stretch=1)

    def on_scenario_changed(self, text):
        self.scenario_name = text
        self.load_current_scenario()

    def toggle_simulation(self):
        if self.is_running:
            self.timer.stop()
            self.btn_start.setText("Start Simulation")
            self.btn_start.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 8px;")
            self.is_running = False
        else:
            self.timer.start(33)  # ~30 FPS
            self.btn_start.setText("Pause Simulation")
            self.btn_start.setStyleSheet("background-color: #ffc107; color: black; font-weight: bold; padding: 8px;")
            self.is_running = True

    def reset_simulation(self):
        self.timer.stop()
        self.is_running = False
        self.btn_start.setText("Start Simulation")
        self.btn_start.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 8px;")
        
        self.sim_time = 0.0
        self.sim_engine.pan_deg = 0.0
        self.sim_engine.tilt_deg = 0.0
        self.tracker = KalmanTracker(dt=0.033)
        self.controller.reset()
        self.evaluator.reset()
        self.load_current_scenario()
        
        self.update_simulation()

    def update_simulation(self):
        t_start = time.time()
        dt = 0.033
        self.sim_time += dt

        # 1. Compute 3D target motion & platform disturbances
        target_pos = self.target_motion.get_position(self.sim_time)
        plat_offset = self.platform_dist.get_offset(self.sim_time) if self.platform_dist else None

        # 2. Render 3D virtual camera frame
        raw_frame = self.sim_engine.render_frame(target_pos, plat_offset)

        # 3. Apply environmental & noise filters
        noisy_frame = raw_frame.copy()
        for filter_op in self.image_filters:
            noisy_frame = filter_op.apply(noisy_frame)

        # 4. Beacon Detection
        det_res = self.detector.detect(noisy_frame)

        # 5. Position Estimation & Kalman Filtering
        est_x, est_y, _, _ = self.tracker.update(det_res["detected"], det_res["x"], det_res["y"])

        # 6. Pointing Error Calculation relative to camera center
        center_x, center_y = self.sim_engine.cx, self.sim_engine.cy
        if det_res["detected"]:
            error_x = est_x - center_x
            error_y = est_y - center_y
        else:
            error_x, error_y = 0.0, 0.0

        # 7. PID Gimbal Control
        pan_cmd, tilt_cmd = self.controller.compute(error_x, error_y, dt)
        self.sim_engine.update_gimbal(pan_cmd, tilt_cmd)

        frame_ms = (time.time() - t_start) * 1000.0

        # 8. Evaluation & Metrics
        self.evaluator.update(det_res["detected"], error_x, error_y, frame_ms)
        summary = self.evaluator.get_summary()

        # 9. Draw visual tracking overlays on frame
        if det_res["detected"]:
            # Estimated target centroid marker
            cv2.circle(noisy_frame, (int(est_x), int(est_y)), 5, (0, 255, 255), -1)
            if det_res["bbox"]:
                bx, by, bw, bh = det_res["bbox"]
                cv2.rectangle(noisy_frame, (bx, by), (bx + bw, by + bh), (0, 255, 0), 2)
            cv2.putText(noisy_frame, f"LOCK ({det_res['confidence']:.2f})", (int(est_x)+10, int(est_y)-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Update GUI Telemetry & Labels
        self.lbl_target_pos.setText(f"[{target_pos[0]:.1f}, {target_pos[1]:.1f}, {target_pos[2]:.1f}]")
        self.lbl_cam_pan.setText(f"{self.sim_engine.pan_deg:.2f}°")
        self.lbl_cam_tilt.setText(f"{self.sim_engine.tilt_deg:.2f}°")
        self.lbl_acq_time.setText(str(summary["acquisition_time_s"]))
        self.lbl_mean_err.setText(f"{summary['mean_pointing_error_px']} px")

        self.metrics_label.setText(
            f"Scenario: {self.scenario_name} | "
            f"Error: {summary['mean_pointing_error_px']} px | "
            f"Lock: {summary['lock_retention_rate_pct']}% | "
            f"FPS: {summary['avg_fps']}"
        )

        # Convert OpenCV BGR frame to Qt QImage for display
        rgb_frame = cv2.cvtColor(noisy_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_img = QtGui.QImage(rgb_frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.feed_label.setPixmap(QtGui.QPixmap.fromImage(qt_img))

    def export_logs(self):
        log_path = "evaluation/performance_report.json"
        summary = self.evaluator.save_log(log_path)
        QtWidgets.QMessageBox.information(
            self, "Report Exported",
            f"Performance report saved to {log_path}\n\n"
            f"Acquisition Time: {summary['acquisition_time_s']} s\n"
            f"Mean Error: {summary['mean_pointing_error_px']} px\n"
            f"Lock Rate: {summary['lock_retention_rate_pct']}%\n"
            f"Avg FPS: {summary['avg_fps']}"
        )

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PATDashboard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

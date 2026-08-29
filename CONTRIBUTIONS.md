# Team Contributions

## Project

**Development of an AI-Based Virtual Camera Tracking System for Coarse Alignment of Mobile Free Space Optical Communication (FSOC) Terminals**

---

# 1. Project Goal

Build a standalone application that can simulate a virtual FSOC environment and autonomously acquire, detect and continuously track a moving optical beacon using a virtual camera.

### Core Flow

Virtual Environment
        ↓
Virtual Camera
        ↓
Camera Frame
        ↓
Beacon Detection
        ↓
Position Estimation
        ↓
Tracking / Prediction
        ↓
Pointing Error (ΔX, ΔY)
        ↓
Pan / Tilt Control
        ↓
Virtual Camera
        ↺

---

# 2. Team Responsibilities

## Tajmir — Simulation Lead

### Godot / Simulation

- [ ] Create virtual FSOC environment
- [ ] Create FSOC terminal / optical beacon
- [ ] Create virtual camera
- [ ] Implement camera FOV
- [ ] Implement camera orientation
- [ ] Implement target position and movement
- [ ] Implement virtual pan / tilt
- [ ] Generate camera frames
- [ ] Provide ground-truth target/camera data
- [ ] Integrate simulation with UDP

### Main Goal
A working virtual environment where the beacon moves and the camera can be controlled.

---

## Srikrishna — Godot + UDP Integration

### Communication

- [ ] Set up Godot ↔ Python UDP communication
- [ ] Send camera frames from Godot → Python
- [ ] Receive pan / tilt commands from Python → Godot
- [ ] Define communication/data format
- [ ] Handle packet errors / dropped packets if required
- [ ] Test communication latency and reliability
- [ ] Assist Tajmir with Godot integration

### Main Goal
Reliable two-way communication between the simulator and Python pipeline.

---

## Aarya — Python / Vision / Tracking / Control

### Detection

- [ ] Receive frames from Godot
- [ ] Implement beacon detection using OpenCV
- [ ] Identify target position `(x, y)`
- [ ] Calculate detection confidence/status

### Tracking

- [ ] Calculate target position relative to camera centre
- [ ] Calculate `ΔX` and `ΔY`
- [ ] Implement Kalman filter / prediction
- [ ] Handle noisy detections
- [ ] Handle temporary target loss if possible

### Control

- [ ] Implement proportional / PID controller
- [ ] Convert pointing error → pan / tilt command
- [ ] Send pan / tilt commands to Godot
- [ ] Test closed-loop tracking

### Main Goal
A working pipeline:

Frame → Detection → Tracking → Error → Control → Pan/Tilt

---

## Tanay — Motion + Disturbances

### Target Motion

- [x] Implement configurable target velocity
- [x] Implement different target trajectories
- [x] Implement direction changes
- [x] Implement sudden target movement

### Disturbances

- [x] Camera/platform vibration
- [x] Camera motion disturbance
- [x] Image noise
- [x] Blur / visibility degradation
- [x] Atmospheric turbulence approximation
- [x] Adjustable disturbance intensity

### Test Scenarios

- [x] No disturbance
- [x] Moving target
- [x] High noise
- [x] High vibration
- [x] Sudden disturbance
- [x] Target loss and recovery

### Main Goal
Make the simulation configurable and difficult enough to properly test the PAT system.

---

## Rishika — GUI + Evaluation

### GUI

- [ ] Parameter configuration
- [ ] Start / Stop controls
- [ ] Reset simulation
- [ ] Display camera feed
- [ ] Display target/detection status
- [ ] Display pan / tilt values
- [ ] Display tracking error
- [ ] Display FPS
- [ ] Add basic telemetry

### Performance Metrics

- [ ] Acquisition time
- [ ] Average tracking error
- [ ] Maximum tracking error
- [ ] Lock retention rate
- [ ] FPS
- [ ] Processing time
- [ ] Save performance results

### Main Goal
Make the application easy to configure, run and evaluate.

---

## Udit — AI / Detection Support

### AI Detection

- [ ] Research suitable AI-based detection method
- [ ] Test YOLO or another suitable detector
- [ ] Compare AI detection with OpenCV detection
- [ ] Test detection under noise/disturbances
- [ ] Improve detection robustness where practical

### Main Goal
Improve beacon detection using AI without making the MVP dependent on it.

---

# 3. Common MVP Checklist

The following must work before moving to optional features:

- [ ] Virtual beacon exists
- [ ] Virtual camera exists
- [ ] Beacon can move
- [ ] Camera FOV works
- [ ] Godot → Python frame transfer works
- [ ] Python detects beacon
- [ ] Target position is estimated
- [ ] Pointing error is calculated
- [ ] Pan / tilt command is generated
- [ ] Python → Godot control works
- [ ] Closed-loop tracking works
- [ ] Beacon can be acquired
- [ ] At least basic disturbance can be introduced
- [ ] Tracking performance is measured
- [ ] Results can be displayed/logged

---

# 4. Integration Milestones

### M1 — Simulation
- [ ] Virtual target
- [ ] Virtual camera
- [ ] Target movement

### M2 — Communication
- [ ] Godot → Python frame
- [ ] Python → Godot pan/tilt

### M3 — Vision
- [ ] Beacon detection
- [ ] Position estimation

### M4 — Control
- [ ] Error calculation
- [ ] Pan/tilt control
- [ ] Closed-loop tracking

### M5 — Robustness
- [ ] Noise
- [ ] Vibration
- [ ] Target motion
- [ ] Recovery

### M6 — Evaluation
- [ ] Metrics
- [ ] Performance log
- [ ] GUI

### M7 — Final MVP
- [ ] End-to-end system tested
- [ ] Standalone executable generated
- [ ] Demo scenario prepared

---

# 5. Module Interfaces

### Godot → Python

    Camera frame
    Timestamp

### Detector → Tracker

    target_x
    target_y
    confidence
    detected

### Tracker → Controller

    estimated_x
    estimated_y
    error_x
    error_y

### Python → Godot

    pan
    tilt

### Ground Truth

Used only for evaluation.

The PAT algorithm must NOT directly use ground-truth target coordinates.

---

# 6. Development Priority

Always prioritize:

1. Working end-to-end system
2. Reliable acquisition and tracking
3. Disturbances and robustness
4. Performance metrics
5. GUI / visualization
6. AI improvements
7. Extra features

**Working MVP > Extra Features > Visual Polish**

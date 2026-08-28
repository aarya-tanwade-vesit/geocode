# Team Geocode
Development of an AI-Based Virtual Camera Tracking System for Coarse Alignment of Mobile Free Space Optical Communication (FSOC) Terminals

# FSOC Virtual Camera

## Problem Statement

**Development of an AI-Based Virtual Camera Tracking System for Coarse Alignment of Mobile Free Space Optical Communication (FSOC) Terminals**

## Objective

Develop a standalone software system that can:

* Generate a configurable virtual FSOC environment
* Simulate a moving optical beacon
* Simulate a movable virtual camera
* Detect and identify the beacon
* Continuously track the beacon
* Control the virtual camera using pan/tilt
* Introduce disturbances such as noise, vibration and camera motion
* Display tracking performance in real time
* Generate performance logs

## Technical Approach

```text
Godot Simulation
       ↓
Virtual Camera Frame
       ↓
      UDP
       ↓
Python PAT Pipeline
       ↓
OpenCV / AI
       ↓
Detection & Tracking
       ↓
PID Controller
       ↓
Pan / Tilt Command
       ↓
      UDP
       ↓
Godot Virtual Camera
```

## Project Structure

```text
FSOC-Virtual-Camera/
│
├── simulation/     # Godot virtual environment
├── python/         # Detection, tracking and control
├── evaluation/     # Metrics and performance logging
├── gui/            # Application interface
├── config/         # Simulation parameters
└── tests/          # Testing
```

## Team

| Member     | Responsibility                       |
| ---------- | ------------------------------------ |
| Tajmir     | Godot Simulation                     |
| Srikrishna | Godot + UDP Integration              |
| Aarya      | Python / OpenCV / Tracking / Control |
| Tanay      | Target Motion + Disturbances         |
| Rishika    | GUI + Evaluation                     |
| Udit       | AI / Detection Support               |

## Status

🚧 **In Development — SIH 2026 Internal Hackathon**

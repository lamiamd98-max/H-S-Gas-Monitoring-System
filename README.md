# H-S-Gas-Monitoring-System
# Autonomous H2S Gas Monitoring Drone System

This project is an integrated intelligent system using Unmanned Aerial Vehicles (UAVs) to conduct precise aerial surveys for monitoring Hydrogen Sulfide (H2S) gas leaks in industrial facilities, significantly reducing human exposure risks.

## Key Features
* **Autonomy:** Fully autonomous flight through pre-defined waypoint navigation.
* **Real-time Detection:** Monitoring and analyzing gas concentration levels in real-time.
* **Intelligent Response:** Automatic activation of emergency protocols (RTL - Return to Launch) when safety thresholds are exceeded.
* **High-Fidelity Simulation:** Comprehensive testing in the Gazebo environment powered by the PX4 Autopilot.

## Technologies Used
* **Simulation:** Gazebo / SITL.
* **Autopilot:** PX4 Autopilot.
* **Control & Communication:** MAVSDK (Python).
* **Algorithms:** Asynchronous processing (Asyncio) for real-time data handling.

## Decision Matrix (Emergency System)
| Gas Concentration (PPM) | Status | Action |
| :--- | :--- | :--- |
| < 10 | Safe | Continue Mission |
| 10 - 49 | Warning | Alert Operator |
| ≥ 50 | Critical | Return to Launch (RTL) |

## Technical Challenges
1. Modeling gas dispersion and wind effects.
2. Developing custom Gazebo plugins.
3. Synchronizing communication channels via MAVSDK.
4. Balancing computational resource (CPU) usage.

## How to Run
1. Ensure PX4-Autopilot and Gazebo are installed.
2. Launch the simulation environment: `make px4_sitl gazebo`
3. Execute the control script: `python3 monitoring_script.py`

---
*Developed as part of an advanced graduation research project in UAV systems.*

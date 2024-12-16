# SVR Robotics Motor Controller
This Repo contains Motor Driver Controller

### Motor
Moon Motor
Specification - 48V, Brushed DC Motor

### Motor Driver
MBDV DC Motor Driver [Or Rename]
Specification - Modbus

## Project Plan
1. Python Package - Modbus and motor functionality wrapper
2. Testing Script - Test script
3. ROS2 Package based on python package - 
    Node Structure -
    1. cmd_vel to RPM Node
    2. Odometry Node
    3. Motor Error & monitoring
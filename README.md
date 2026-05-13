# ROS 2 Data Collection Pipeline

A 3-node ROS 2 pipeline for a 3-DOF robotic arm that generates mock joint data,
computes forward kinematics, and records episodes to JSON.

## Nodes

| Node | Role |
|---|---|
| `mock_publisher` | Publishes fake joint angles at 10 Hz, hosts `/set_recording` service |
| `fk_node` | Computes end-effector (x, y, z) from joint angles using FK |
| `data_collector` | Records data to JSON when recording is ON |

## Forward Kinematics

r = a2·cos(θ2) + a3·cos(θ2+θ3)
x = cos(θ1)·r,  y = sin(θ1)·r
z = d1 + a2·sin(θ2) + a3·sin(θ2+θ3)
Link lengths: d1=0.5m, a2=0.4m, a3=0.3m

## Build & Run

```bash
colcon build
source install/setup.bash
ros2 launch ros_pipeline pipeline.launch.py
```

## Record an Episode

```bash
# start recording
ros2 service call /set_recording ros_pipeline_interfaces/srv/SetRecording "{record: true}"

# stop and save
ros2 service call /set_recording ros_pipeline_interfaces/srv/SetRecording "{record: false}"

# view saved file
cat ~/episodes/episode_*.json
```

## Output Format

```json
[
  {"joint_states": [θ1, θ2, θ3], "ee_position": [x, y, z]},
  ...
]
```

Files are saved to `~/episodes/` with timestamps in the filename for chronological sorting.

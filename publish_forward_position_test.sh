#colcon build --symlink-install
source install/setup.bash
ros2 launch forward_position_controller publish_forward_position_test.launch.py

#ros2 topic pub /forward_position_controller/commands std_msgs/msg/Float64MultiArray "data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"
#ros2 topic echo /joint_states
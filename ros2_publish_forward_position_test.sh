#colcon build --symlink-install
source install/setup.bash
ros2 launch ros2_control_demo_example_9 test_forward_position_controller.launch.py

#ros2 topic pub /forward_position_controller/commands std_msgs/msg/Float64MultiArray "data:
#- 0.5
#- 0.5
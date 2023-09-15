colcon build --symlink-install
source install/setup.bash
ros2 launch simu_bipo gazebo_sim.launch.py

# sudo killall -9 gazebo gzserver gzclient

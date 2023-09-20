import launch
import launch.actions
import launch_ros.actions

from launch import LaunchDescription

def generate_launch_description():

    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='simu_bipo',
            executable='joint_trajectory_client_node',
            name='joint_trajectory_client',
            namespace='my_bot',
            output='screen'
        ),
    ])

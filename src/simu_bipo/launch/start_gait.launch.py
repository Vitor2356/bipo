import launch.actions
import launch_ros.actions

from launch import LaunchDescription


def generate_launch_description():

    return LaunchDescription([
        launch_ros.actions.Node(
            package='simu_bipo',
            executable='start_gait.py',
            output='screen',
            arguments=["0.5"]),
    ])
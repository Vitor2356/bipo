import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='forward_position_controller',
            executable='publisher_forward_position_controller.py',
            name='publisher_forward_position_controller',
            output='screen',
            parameters=[
                os.path.join(
                    get_package_share_directory('forward_position_controller'),
                    'config',
                    'publisher_test.yaml'
                )
            ]
        )
    ])

import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    joint_trajectory_action_client = Node(
        package='joint_trajectory_action_client',
        executable='testwalk_position',
        output='screen',
    )

    return LaunchDescription([
        joint_trajectory_action_client
    ])
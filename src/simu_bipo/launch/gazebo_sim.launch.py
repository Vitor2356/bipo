import os
import xacro
import launch
import launch_ros

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Nome do pacote e arquivo de mundo
    package_name = 'simu_bipo'
    world_file_name = 'empty.world'

    # Caminho para o arquivo de mundo
    world_path = os.path.join(get_package_share_directory(package_name), 'worlds', world_file_name)
    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_path,
        description='Full path to the world model file to load'
    )
    world = LaunchConfiguration('world')

    # Inclui o launch file do robot_state_publisher
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Inclui o launch file do Gazebo com o plugin correto
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    # Spawner do robô no Gazebo
    spawn_entity = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        output='screen',
        arguments=['-topic', 'robot_description', '-entity', 'my_bot'] 
    )

    # Nó do joint_state_publisher
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # Nó do RViz
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(get_package_share_directory(package_name), 'config', 'config_file.rviz')]
    )

    # Spawner do Joint State Broadcaster
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    # Spawner do Forward Position Controller
    controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_position_controller", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    # Registrar um Event Handler para iniciar o Forward Position Controller após o Joint State Broadcaster ser iniciado
    event_handler = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[controller_spawner],
        )
    )

    return LaunchDescription([
        declare_world_cmd,
        gazebo,
        rsp,
        spawn_entity,
        joint_state_publisher_node,
        rviz_node,
        joint_state_broadcaster_spawner,
        event_handler,
    ])

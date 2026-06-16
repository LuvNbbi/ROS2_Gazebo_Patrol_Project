import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory

from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch_ros.actions import Node

# launch
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

#
from launch.actions import TimerAction


def generate_launch_description():
    #model name
    TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']

    #get package file path
    pkg_share = get_package_share_directory('test_world_robot_control')

    #get world file in package
    world_path = os.path.join(pkg_share, 'worlds', 'test_world.world')

    #===== robot_state_publisher =====
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    urdf_file_name = 'turtlebot3_' + TURTLEBOT3_MODEL + '.urdf'
    frame_prefix = LaunchConfiguration('frame_prefix', default='')

    print('urdf_file_name : {}'.format(urdf_file_name))

    urdf_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'urdf',
        urdf_file_name)

    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()
    #====== /robot_state_publisher ====
    #====== navigation.launch.py =====
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('turtlebot3_navigation2'),
                'launch',
                'navigation2.launch.py'
            )   
        ),
        launch_arguments={
            'map': os.path.join(
                pkg_share,
                'maps',
                'test_world_map.yaml'
            ),
            'use_sim_time':'true',
        }.items()
    )
    #====== /navigation.launch.py =====
    #====== spawn robot =====
    model_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'models',
        'turtlebot3_burger',
        'model.sdf'
    )
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-file', model_path,
            '-entity', 'turtlebot3',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.01',
            '-Y', '0.0'
        ],
        output='screen'
    )
    #===== /spawn robot=====
    #===== initial robot pose =====
    initial_pose = Node(
        package='test_world_robot_control',
        executable='initial_pose_publisher',
        output='screen'
    )

    return LaunchDescription([
        ExecuteProcess(
            cmd=[
                'gazebo', 
                '--verbose',
                world_path,
                #spawn_entity 
                '-s', 'libgazebo_ros_init.so',
                '-s', 'libgazebo_ros_factory.so'
                ],
            output = 'screen'
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'robot_description': robot_desc,
                'frame_prefix': PythonExpression(["'", frame_prefix, "/'"])
            }],
        ),
        TimerAction(
            period=5.0,
            actions=[spawn_robot]
        ),
        TimerAction(
            period=7.0,
            actions=[nav2_launch]
        ),
        TimerAction(
            period=25.0,
            actions=[initial_pose]
        ),
        TimerAction(
            period=30.0,
            actions=[
                Node(
                    package='test_world_robot_control',
                    executable='test_world_robot_patrol',
                    output='screen'
                )
            ]
        )
        ],)


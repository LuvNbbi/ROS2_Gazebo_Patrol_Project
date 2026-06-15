# ROS2_Gazebo_Patrol_Project

#실행 방법
1. 저장한 월드 실행
gazebo worlds/test_world.world

2. 터틀봇 스폰 (맵에 있어서 안해도 됨)
export TURTLEBOT3_MODEL=burger

ros2 run gazebo_ros spawn_entity.py -file /opt/ros/humble/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf -entity turtlebot3

3. robot_state_publisher 실행
ros2 launch turtlebot3_gazebo robot_state_publisher.launch.py

4. Nav2 실행
ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=maps/test_world_map.yaml use_sim_time:=true

5. RViz 열리면 2D Pose Estimate로 위치 클릭 후 방향 드래그

6. 패트롤 실행
ros2 run test_world_robot_control test_world_robot_patrol

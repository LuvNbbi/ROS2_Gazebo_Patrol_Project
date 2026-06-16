# ROS2_Gazebo_Patrol_Project

ROS2 Humble, Gazebo Classic, Nav2를 이용한 자율 순찰 로봇 프로젝트입니다.

커스텀 Gazebo 환경에서 Turtlebot3를 동적으로 생성하고, AMCL 기반 위치 추정 후 지정된 경유지를 자동 순찰합니다.

## Tech stack

- ROS2 Humble
- Gazebo Classic
- Nav2
- AMCL
- TurtleBot3
- Python

## Features

- Custom Gazebo World
- Dynamic TurtleBot3 Spawn
- AMCL Localization
- Nav2 Path Planning
- Autonomous Patrol
- One-click Launch System
  
## Run

-launch로 한번에 실행하기
export TURTLEBOT3_MODEL=burger

source install/setup.bash

ros2 launch test_world_robot_control test_world_launch.py

-하나씩 실행하기

1. 저장한 월드 실행
gazebo worlds/test_world.world

2. 터틀봇 스폰
export TURTLEBOT3_MODEL=burger

ros2 run gazebo_ros spawn_entity.py -file /opt/ros/humble/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf -entity turtlebot3

3. robot_state_publisher 실행
ros2 launch turtlebot3_gazebo robot_state_publisher.launch.py

4. Nav2 실행
ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=maps/test_world_map.yaml use_sim_time:=true

5. RViz 열리면 2D Pose Estimate로 위치 클릭 후 방향 드래그

## 최근 업데이트
### 2026-06-16 

-launch 파일 생성하여 한번에 실행

7. 패트롤 실행
ros2 run test_world_robot_control test_world_robot_patrol

cmake_minimum_required(VERSION 3.8)
project(joint_trajectory_action_client)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# new dependencies
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(action_msgs REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# Adicione os diretórios de inclusão
include_directories(include)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# Crie um executavel para o Action Client
add_executable(testwalk_position scripts/testwalk_position.py)

# Configure o Action Client como um ROS 2 node
ament_target_dependencies(
  testwalk_position
  rclcpp
  rclpy
  action_msgs
)

install(
  TARGETS
    testwalk_position
  DESTINATION
    lib/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/testwalk_position.py
  DESTINATION
    lib/${PROJECT_NAME}
)

install(
  DIRECTORY
    launch
    scripts
  DESTINATION
    share/${PROJECT_NAME}
)


ament_package()
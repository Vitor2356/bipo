cmake_minimum_required(VERSION 3.8)
project(simu_bipo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Encontrar dependências
find_package(ament_cmake REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(rviz2 REQUIRED)
find_package(ros2_controllers REQUIRED)
find_package(xacro REQUIRED)
find_package(urdf REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # As seguintes linhas evitam que o linter verifique certas coisas
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# Instalar diretórios
install(
  DIRECTORY
    config
    description
    launch
    meshes
    worlds
  DESTINATION
    share/${PROJECT_NAME}
)

ament_package()

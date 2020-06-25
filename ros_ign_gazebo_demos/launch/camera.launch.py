 # Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    pkg_ros_ign_gazebo_demos = get_package_share_directory('ros_ign_gazebo_demos')
    pkg_ros_ign_gazebo = get_package_share_directory('ros_ign_gazebo')

    # Ignition Gazebo
    ign_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_ign_gazebo, 'launch', 'ign_gazebo.launch.py'),
        )
    )

    # RViz
    rviz = Node(
        package='rviz2',
        node_executable='rviz2',
        arguments=['-d', os.path.join(pkg_ros_ign_gazebo_demos, 'rviz', 'camera.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    # Bridge
    bridge = Node(
        package='ros_ign_bridge',
        node_executable='parameter_bridge',
        arguments=['/camera@sensor_msgs/msg/Image@ignition.msgs.Image',
                   '/camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo'],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
          'ign_args',
          default_value=['-r camera_sensor.sdf'],
          description='Ignition Gazebo arguments'),
        DeclareLaunchArgument('rviz', default_value='true',
                             description='Open RViz.'),
        ign_gazebo,
        bridge,
        rviz
    ])

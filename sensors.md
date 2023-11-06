# Devices useful repositories

- RealSense ROS [[repo]](https://github.com/IntelRealSense/realsense-ros)
- RealSense SDK [[sdk]](https://www.intelrealsense.com/sdk-2/)
- Orbbec Astra ROS [[repo]](https://github.com/ros2/ros_astra_camera)
- Orbbec SDK [[sdk]](https://orbbec3d.com/index/download.html)
- Raspberry Pi 4 RT image [[pi]](https://github.com/ros-realtime/ros-realtime-rpi4-image)

# FRAMOS D435e camera
[Main page](https://www.framos.com/en/industrial-depth-cameras) where to find datasheet, quick-start guide and user manual

[Solution home](https://support.framos.com/support/solutions/48000449987) with some interesting links and F.A.Q.s

How to [setup a basic Docker](https://support.framos.com/support/solutions/articles/48001203635-how-to-setup-a-basic-docker-container-with-the-framos-d400e-cameras-) Container (needs Docker compose)

[ROS2 Wrapper](https://github.com/AltoRobotics/realsense-ros/tree/FramosPlusHumble) realsense-ros for FRAMOS camera with Humble

### Quick testing
- Plug the power supply and the camera ethernet cable to a port on your laptop
- Download the software package from the main page (link above) and follow the instructions in the ReadMe.txt file to install the FRAMOS Camera Suite software and the custom librealsense SDK
- Launch _/usr/src/framos/camerasuite/Tools/ConfigureIp_ to set the correct IP for the camera (the default one is not in the correct network)
- Run _realsense-viewer_ to check that the camera is on and working correctly
- [ROS2] If you're using ROS2 Humble and want to install realsense-ros, follow the instructions at the link above, moving to the branch _FramosPlusHumble_

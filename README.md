# AI-self-driving-fork-lift 

Hardware로는 Turtlebot3을 이용하였습니다.
상단에 주변 환경 정보를 수집하는 Lidar가 위치하고 있고, 그 아래 로봇의 controller인 opencr보드와, sensor data를 처리하는 RaspberryPi가 있습니다. 저희는 성능을 강화하기 위해 RaspberryPi를 Jetson nano로 교체해주었으며, 객체를 인식하기 위한 카메라와, 물건을 운반하기 위한 fork 또한 부착해주었습니다. 

![image](https://github.com/parseyoung/AI-self-driving-fork-lift/assets/104110839/aa143451-b869-4d1e-9270-5da646a28b09)

## remotePC에 ROS-Melodic 설치
$ sudo apt update $ sudo apt upgrade <br/>
$ wget https://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master/install_ros_melodic.sh <br/>
$ chmod 755 ./install_ros_melodic.sh <br/>
$ bash ./install_ros_melodic.sh <br/>

## 종속 ROS 패키지 설치
$ sudo apt-get install ros-melodic-joy ros-melodic-teleop-twist-joy \
  ros-melodic-teleop-twist-keyboard ros-melodic-laser-proc \
  ros-melodic-rgbd-launch ros-melodic-depthimage-to-laserscan \
  ros-melodic-rosserial-arduino ros-melodic-rosserial-python \
  ros-melodic-rosserial-server ros-melodic-rosserial-client \
  ros-melodic-rosserial-msgs ros-melodic-amcl ros-melodic-map-server \
  ros-melodic-move-base ros-melodic-urdf ros-melodic-xacro \
  ros-melodic-compressed-image-transport ros-melodic-rqt* \
  ros-melodic-gmapping ros-melodic-navigation ros-melodic-interactive-markers

  ## Turtlebot3 패키지 설치
$ sudo apt-get install ros-melodic-dynamixel-sdk  <br/>
$ sudo apt-get install ros-melodic-turtlebot3-msgs  <br/>
$ sudo apt-get install ros-melodic-turtlebot3  <br/>


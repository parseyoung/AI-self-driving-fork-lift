# AI-self-driving-fork-lift 

Hardware로는 Turtlebot3을 이용하였습니다.
상단에 주변 환경 정보를 수집하는 Lidar가 위치하고 있고, 그 아래 로봇의 controller인 opencr보드와, sensor data를 처리하는 RaspberryPi가 있습니다. 저희는 성능을 강화하기 위해 RaspberryPi를 Jetson nano로 교체해주었으며, 객체를 인식하기 위한 카메라와, 물건을 운반하기 위한 fork 또한 부착해주었습니다. 

![image](https://github.com/parseyoung/AI-self-driving-fork-lift/assets/104110839/aa143451-b869-4d1e-9270-5da646a28b09)

## remotePC에 ROS-Melodic 설치
$ sudo apt update
$ sudo apt upgrade
$ wget https://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master
/install_ros_melodic.sh
$ chmod 755 ./install_ros_melodic.sh 
$ bash ./install_ros_melodic.sh

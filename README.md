# AI-self-driving-fork-lift 

Hardware로는 Turtlebot3을 이용하였습니다.
상단에 주변 환경 정보를 수집하는 Lidar가 위치하고 있고, 그 아래 로봇의 controller인 opencr보드와, sensor data를 처리하는 RaspberryPi가 있습니다. 저희는 성능을 강화하기 위해 RaspberryPi를 Jetson nano로 교체해주었으며, 객체를 인식하기 위한 카메라와, 물건을 운반하기 위한 fork 또한 부착해주었습니다. 

![image](https://github.com/parseyoung/AI-self-driving-fork-lift/assets/104110839/aa143451-b869-4d1e-9270-5da646a28b09)

## YOLO 환경 설정 
### JetPack-4.6 Jetston Nano 설정 후 tensorRT실행
CUDA 관련 환경 변수 설정   <br/>
$ sudo jetson_clocks   <br/>
$ sudo apt update  <br/>
$ mkdir ${HOME}/project  <br/>
$ cd ${HOME}/project  <br/>
$ git clone https://github.com/jkjung-avt/jetson_nano.git  <br/>
$ cd jetson_nano  <br/>
$ ./install_basics.sh  <br/>
$ source ${HOME}/.bashrc  <br/>

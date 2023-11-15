#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""trt_yolo.py

This script demonstrates how to do real-time object detection with
TensorRT optimized YOLO engine.
"""

import os
import argparse
import socket
import RPi.GPIO as GPIO
from time import sleep
import time




import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver

from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO


WINDOW_NAME = 'TrtYOLODemo'
HOST = '192.168.43.227'  # IP 주소
PORT = 10004  # 포트 번호

GPIO.setmode(GPIO.BOARD)

servo_pin = 33

GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)
servo.start(0)

servo_min_duty = 3
servo_max_duty = 12

def set_servo(degree):
    if degree > 180:
        degree = 180
    elif degree < 0:
        degree = 0
       
    duty = servo_min_duty + (degree * (servo_max_duty - servo_min_duty) / 180.0)
    servo.ChangeDutyCycle(duty)


def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time object detection with TensorRT optimized '
            'YOLO model on Jetson')
    parser = argparse.ArgumentParser(description=desc)
    parser = add_camera_args(parser)
    parser.add_argument(
        '-c', '--category_num', type=int, default=80,
        help='number of object categories [80]')
    parser.add_argument(
        '-t', '--conf_thresh', type=float, default=0.3,
        help='set the detection confidence threshold')
    parser.add_argument(
        '-m', '--model', type=str, required=True,
        help=('[yolov3-tiny|yolov3|yolov3-spp|yolov4-tiny|yolov4|'
              'yolov4-csp|yolov4x-mish|yolov4-p5]-[{dimension}], where '
              '{dimension} could be either a single number (e.g. '
              '288, 416, 608) or 2 numbers, WxH (e.g. 416x256)'))
    parser.add_argument(
        '-l', '--letter_box', action='store_true',
        help='inference with letterboxed image [False]')
    args = parser.parse_args()
    return args


def create_socket():
    """Create a socket and connect to the server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s


def send_socket_data(sock, message):
    """Send data via socket."""
    try:
        # 데이터 전송
        sock.sendall(message.encode('utf-8'))
    except ConnectionRefusedError:
        print('ERROR: Failed to connect to the server.')

def receive_socket_data(sock):
    """Receive data from socket."""
    try:
        # 데이터 수신
        data = sock.recv(1024).decode('utf-8')
        return data
    except ConnectionRefusedError:
        print('ERROR: Failed to receive data from the server.')


def loop_and_detect(cam, trt_yolo, conf_th, vis, sock):
    """Continuously capture images from camera and do object detection.

    # Arguments
      cam: the camera instance (video source).
      trt_yolo: the TRT YOLO object detector instance.
      conf_th: confidence/score threshold for object detection.
      vis: for visualization.
      sock: the socket for sending data.
    """
    full_scrn = False
    fps = 0.0
    tic = time.time()
    while True:
        

        if cv2.getWindowProperty(WINDOW_NAME, 0) < 0:
            break
        img = cam.read()
        if img is None:
            break
        boxes, confs, clss = trt_yolo.detect(img, conf_th)
        img = vis.draw_bboxes(img, boxes, confs, clss)
        img = show_fps(img, fps)
        cv2.imshow(WINDOW_NAME, img)
        toc = time.time()
        curr_fps = 1.0 / (toc - tic)
        # calculate an exponentially decaying average of fps number
        fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
        tic = toc
        key = cv2.waitKey(1)
        if key == 27:  # ESC key: quit program
            break
        elif key == ord('F') or key == ord('f'):  # Toggle fullscreen
            full_scrn = not full_scrn
            set_display(WINDOW_NAME, full_scrn)
       
        class_names = [str(cls) for cls in clss]

        if len(class_names) > 0:
            if class_names[0] == '39.0':
                send_socket_data(sock, '객체')

        
def main():
    args = parse_args()
    if args.category_num <= 0:
        raise SystemExit('ERROR: bad category_num (%d)!' % args.category_num)
    if not os.path.isfile('yolo/%s.trt' % args.model):
        raise SystemExit('ERROR: file (yolo/%s.trt) not found!' % args.model)

    cam = Camera(args)
    if not cam.isOpened():
        raise SystemExit('ERROR: failed to open camera!')

    cls_dict = get_cls_dict(args.category_num)
    vis = BBoxVisualization(cls_dict)
    trt_yolo = TrtYOLO(args.model, args.category_num, args.letter_box)

    open_window(
        WINDOW_NAME, 'Camera TensorRT YOLO Demo',
        cam.img_width, cam.img_height)

    # Create the socket and establish the connection
    sock = create_socket()

    loop_and_detect(cam, trt_yolo, args.conf_thresh, vis=vis, sock=sock)

    cam.release()
    cv2.destroyAllWindows()

    # Close the socket after sending the message
    sock.close()


if __name__ == '__main__':
    main()
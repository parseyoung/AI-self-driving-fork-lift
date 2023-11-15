import RPi.GPIO as GPIO
from time import sleep
import socket

GPIO.setwarnings(False)
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

# Socket configuration
HOST = '192.168.43.227'  # Replace with the IP address of your server
PORT = 10000

try:
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((HOST, PORT))

        while True:
            # Receive data from the server
            data = s.recv(1024)
            if not data:
                continue

            received_data = data.decode().strip()
            print(received_data)
            if received_data == 'Goal Reached!':
                set_servo(180)
                sleep(1)
                set_servo(90)
                sleep(1)

except KeyboardInterrupt:
    print('KeyboardInterrupt')

finally:
    # Clean up GPIO settings
    servo.stop()
    GPIO.cleanup()

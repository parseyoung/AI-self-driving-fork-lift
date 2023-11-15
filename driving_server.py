#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from actionlib_msgs.msg import GoalStatusArray
import socket
import select

class WaypointNavigation:
    def __init__(self):
        rospy.init_node('waypoint_navigation')
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

        self.goal_reached_sub = rospy.Subscriber('/move_base/status', GoalStatusArray, self.goal_status_callback)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 10006))
        self.sock.listen(2)
        self.connections = []  # List to store client connections
        rospy.loginfo('Waiting for clients to connect...')

        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.twist = Twist()

        self.waypoints = [
            [
                Pose(Point(0.0, 2.8, 0), Quaternion(0, 0, 0, 1)),   # Waypoint 1
            ],
            [
                Pose(Point(0.8, 2.8, 0), Quaternion(0, 0, 0, 1)),   # Waypoint 2
            ],
            [
                Pose(Point(1.6, 2.8, 0), Quaternion(0, 0, 0, 1)),   # Waypoint 3
            ],
            [
                Pose(Point(0, 0, 0), Quaternion(0, 0, 0, 1))        # Waypoint 4
            ]
        ]

        self.goal_reached = False  # Flag to track if goal is reached

    def receive_data(self, conn, timeout=1.0):
        conn.settimeout(timeout)
        try:
            data = conn.recv(1024)
            return data
        except socket.timeout:
            return None

    def goal_status_callback(self, msg):
        # Reset the goal reached flag
        for status in msg.status_list:
            if status.status == 3:  # Goal reached status
                rospy.sleep(0.1)
                self.goal_reached = True
                break

    def send_message_to_all_clients(self, message):
        for conn in self.connections:
            conn.send(message.encode())

    def move_to_waypoints(self, waypoints):
        conn = self.connections[0]  # Get the connection from the first client
        for waypoint in waypoints:
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "map"
            goal.target_pose.pose = waypoint

            rospy.loginfo("Moving to waypoint...")

            self.client.cancel_goal()
            self.goal_reached = False  # Reset the goal reached flag

            while not rospy.is_shutdown():
                data = self.receive_data(conn)  # Receive data from the first client
                rospy.sleep(0.1)
                if data == '객체':
                    rospy.loginfo('객체가 인식되었습니다. 목표 이동을 취소합니다.')
                    self.client.cancel_goal()
                    rospy.sleep(3)
                elif data is None:
                    # Check if the previous goal has been reached
                    if self.goal_reached:
                        self.goal_reached = False  # Reset the goal reached flag
                    else:
                        rospy.loginfo('이전 목표 이동이 완료되지 않았습니다.')
                    self.client.send_goal(goal)
                    rospy.sleep(0.1)
                if self.goal_reached:
                    rospy.loginfo('Goal reached. Exiting...')
                    self.send_message_to_all_clients('Goal Reached!')
                    rospy.sleep(0.1)
                    break

            self.goal_reached = False  # Reset the goal reached flag

    def run(self):
        while not rospy.is_shutdown():
            readable, _, _ = select.select([self.sock], [], [], 0)
            for sock in readable:
                conn, addr = sock.accept()
                rospy.loginfo('소켓 연결됨: {}'.format(addr))
                self.connections.append(conn)

            if len(self.connections) == 2:  # Accept only two clients
                user_input = int(input("Enter the waypoint number (1, 2, 3, or 4): "))

                if user_input >= 1 and user_input <= 4:
                    self.move_to_waypoints(self.waypoints[user_input - 1])
                else:
                    rospy.logwarn("Invalid waypoint number.")

        # Close all client connections
        for conn in self.connections:
            conn.close()
        self.sock.close()

if __name__ == '__main__':
    try:
        waypoint_navigation = WaypointNavigation()
        waypoint_navigation.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation finished.")
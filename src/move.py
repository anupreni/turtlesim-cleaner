#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow,sqrt,atan2, degrees


#Definin global parameters
length = 5
width  = 2.5
PI = 3.1415926535897
ang_speed = 0.2
speed = 1

class turtle:
    def __init__(self):
	#Starts a new node
	rospy.init_node('robot_cleaner', anonymous=True)
	self.vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_sub = rospy.Subscriber('/turtle1/pose', Pose, self.callback_pose)
	self.vel_msg = Twist()
	#self.rate = rospy.Rate(10)
	self.pose = Pose()
	self.xpose = 0
	self.ypose = 0
 
	#callback to get current turtle position
    def callback_pose(self,data):
	self.pose = data
	self.xpose = self.pose.x
	self.ypose = self.pose.y
	
	#function for rotating the turtle 
    def rotate(self,angle_deg, orientation):
	angle = angle_deg*PI/180
        self.vel_msg.linear.x = 0
        t0 = rospy.Time.now().to_sec()
	if orientation == 'C':
	    self.vel_msg.angular.z = -abs(ang_speed)
	if orientation == 'CC':
	    self.vel_msg.angular.z = abs(ang_speed)
	curr_angle = 0
	while(curr_angle < angle):
	    self.vel_pub.publish(self.vel_msg)
	    #self.rate.sleep()		
	    t1 = rospy.Time.now().to_sec()
	    curr_angle = ang_speed*(t1-t0)
	self.vel_msg.angular.z = 0
	self.vel_pub.publish(self.vel_msg)

	#function for moving the turtle to desired waypoint
    def go_to_waypoint(self,x1,y1,r):

	#Clockwise or Counter Clockwise
	if (r == 2 or r == 3):
	    self.rotate(90, 'CC')
	if(r == 4 or r == 5 ):
	    self.rotate(90, 'C')
	#Euclidean distance
	distance = sqrt((self.xpose - x1)**2 + (self.ypose - y1)**2)
	self.vel_msg.linear.x = abs(speed)
        self.vel_msg.angular.z = 0
	curr_distance = 0
	t0 = rospy.Time.now().to_sec()
	while(curr_distance < distance):
	     self.vel_pub.publish(self.vel_msg)	
	     #self.rate.sleep()
	     rospy.loginfo("Current X %s",self.xpose)
	     t1 = rospy.Time.now().to_sec()
	     curr_distance = speed*(t1-t0)
	self.vel_msg.linear.x = 0
	self.vel_pub.publish(self.vel_msg)
		
	#function for moving the turtle to home position
    def go_to_home(self):
	angle = degrees(atan2(length,2*width))
	self.rotate(angle+90,'C')
	#Euclidean distance
        distance = sqrt((self.xpose - 5.44445)**2 + (self.ypose - 5.44445)**2)
	self.vel_msg.linear.x = abs(speed)
        self.vel_msg.angular.z = 0
	curr_distance = 0
	t0 = rospy.Time.now().to_sec()
	while(curr_distance < distance):
	     self.vel_pub.publish(self.vel_msg)	
	     #self.rate.sleep()
	     rospy.loginfo("Current X %s",self.xpose)
	     t1 = rospy.Time.now().to_sec()
	     curr_distance = speed*(t1-t0)
	self.vel_msg.linear.x = 0
	self.vel_pub.publish(self.vel_msg)		

	
    def clean(self):
	rospy.loginfo("Turtle is starting")
	self.go_to_waypoint(self.xpose + length, self.ypose,1)
	self.go_to_waypoint(self.xpose, self.ypose + width,2)
	self.go_to_waypoint(self.xpose-length, self.ypose,3)
	self.go_to_waypoint(self.xpose, self.ypose+ width,4)
	self.go_to_waypoint(self.xpose+ length, self.ypose,5)
	self.go_to_home()
	rospy.loginfo("Work is completed :)")


if __name__ == '__main__':
    try:
        #Testing our function
	turtlesim = turtle()
        while not rospy.is_shutdown():
	     turtlesim.clean()
	     break
    except rospy.ROSInterruptException: passposition_topic = '/turtle1/Pose'


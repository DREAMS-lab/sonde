"""
Jnaneshwar Das
Offboard velocity control with MAVROS for following position setpoints on Robo-boat-o repeatedly 
"""

import rospy
from mavros_msgs.msg import State
from geometry_msgs.msg import PoseStamped, Point, Quaternion, Twist
import math
import numpy




class OffbPosCtl:
    curr_pose = PoseStamped()
    waypointIndex = 0
    sim_ctr = 1

    des_vel = Twist()
    isReadyToFly = False

    WIDTH = 20
    THR_FACTOR = 2
    distThreshold = 1

    locations = numpy.matrix([[WIDTH, 0, 0, 0, 0, -0.48717451, -0.87330464],
                              [0, WIDTH, 1, 0, 0, 0, 1],
                              [-WIDTH, 0, 1, 0., 0., 0.99902148, -0.04422762],
                              [0, -WIDTH, 1, 0, 0, 0, 0],
                              ])


    def __init__(self):
        rospy.init_node('offboard_velocity_test', anonymous=True)
        vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=10)
        mocap_sub = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, callback=self.mocap_cb)
        state_sub = rospy.Subscriber('/mavros/state', State, callback=self.state_cb)

        rate = rospy.Rate(10)  # Hz
        rate.sleep()
        shape = self.locations.shape


        while not rospy.is_shutdown():
            print(self.sim_ctr, shape[0], self.waypointIndex)
            if self.waypointIndex is shape[0]:
                self.waypointIndex = 0
                self.sim_ctr += 1

            if self.isReadyToFly:
                des_x = self.locations[self.waypointIndex, 0]
                des_y = self.locations[self.waypointIndex, 1]
                self.des_x = des_x
                self.des_y = des_y


                curr_x = self.curr_pose.pose.position.x
                curr_y = self.curr_pose.pose.position.y

                dist = math.sqrt((curr_x - des_x)*(curr_x - des_x) + (curr_y - des_y)*(curr_y - des_y))
                norm = math.sqrt((curr_x - des_x)*(curr_x - des_x) + (curr_y - des_y)*(curr_y - des_y))
                norm_throttled = norm*self.THR_FACTOR
                self.des_vel.linear.x = (des_x - curr_x)/norm_throttled
                self.des_vel.linear.y = (des_y - curr_y)/norm_throttled

                if dist < self.distThreshold:
                    self.waypointIndex += 1
                    print(dist, curr_x, curr_y, self.waypointIndex)

            vel_pub.publish(self.des_vel)
            rate.sleep()

    def copy_pose(self, pose):
        pt = pose.pose.position
        quat = pose.pose.orientation
        copied_pose = PoseStamped()
        copied_pose.header.frame_id = pose.header.frame_id
        copied_pose.pose.position = Point(pt.x, pt.y, pt.z)
        copied_pose.pose.orientation = Quaternion(quat.x, quat.y, quat.z, quat.w)
        return copied_pose

    def mocap_cb(self, msg):
        # print msg
        self.curr_pose = msg

    def state_cb(self,msg):
        print(msg.mode)
        if(msg.mode=='OFFBOARD'):
            self.isReadyToFly = True
            print("readyToFly")


if __name__ == "__main__":
    OffbPosCtl()

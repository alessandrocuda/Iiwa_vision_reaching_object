#!/usr/bin/python3
import rospy
import rospkg
import random
import numpy as np
from gazebo_msgs.srv import GetLinkState
from gazebo_msgs.msg import LinkState


#cancella
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

def iiwa_ee_pos():
    rospy.wait_for_service('/gazebo/get_link_state')
    try:
        while True:
            state_msg_l = LinkState()

            state_msg_l.link_name = "iiwa_gripper::left_cube"
            state_msg_l.reference_frame = ''

            set_state_l = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
            state_msg_l = set_state_l(state_msg_l.link_name, state_msg_l.reference_frame)
            #print(state_msg_l)

            print()

            state_msg_r = LinkState()

            state_msg_r.link_name = "iiwa_gripper::right_cube"
            state_msg_r.reference_frame = ''

            set_state_r = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
            state_msg_r = set_state_r(state_msg_r.link_name, state_msg_r.reference_frame)
            #print(state_msg_r)
            print(state_msg_l.link_state.pose.position.x)
            print(state_msg_r.link_state.pose.position.x)
            xmed = (state_msg_r.link_state.pose.position.x + state_msg_l.link_state.pose.position.x)/2
            ymed = (state_msg_r.link_state.pose.position.y + state_msg_l.link_state.pose.position.y)/2
            zmed = (state_msg_r.link_state.pose.position.z + state_msg_l.link_state.pose.position.z)/2

            print(f"x = {xmed} y = {ymed} z = {zmed}")

            # rospy.wait_for_service('/gazebo/set_model_state')

            # state_msg = ModelState()

            # state_msg.model_name = "unit_sphere"
            # state_msg.pose.position.x = xmed
            # state_msg.pose.position.y = ymed 
            # state_msg.pose.position.z = zmed 

            # set_state = rospy.ServiceProxy(
            #     '/gazebo/set_model_state', SetModelState)
            # resp = set_state(state_msg)
            # print(state_msg)

            rospy.sleep(delay)  

    except rospy.ServiceException as e:
        print( f"Service call failed: {e}")

if __name__ == "__main__":
    delay = 0.1       #modificare se serve più tempo per catturare immagini da camera
    print(f"Ogni {delay} secondi ritornerà la posizione dell'ee")
    iiwa_ee_pos()
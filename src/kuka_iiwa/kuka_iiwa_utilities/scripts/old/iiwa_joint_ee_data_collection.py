#!/usr/bin/python3
import rospy
import rospkg
import random
import numpy as np
from itertools import product

from gazebo_msgs.srv import GetLinkState
from gazebo_msgs.msg import LinkState

from std_msgs.msg import String,Int32,Int32MultiArray, Float64MultiArray, MultiArrayDimension
from  sensor_msgs.msg import JointState

#cancella
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

joints_velocity = []
pub = rospy.Publisher('/iiwa/pos_effort_controller/command', Float64MultiArray, queue_size=10)

def callback(data):
    #rospy.loginfo(data.name)
    global joints_velocity
    joints_velocity = np.array(data.velocity)

def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in product(*vals):
        yield dict(zip(keys, instance))

def iiwa_ee_pos():
    global joints_velocity
    rospy.wait_for_service('/gazebo/get_link_state')
    grid = {
        "joint1": np.linspace(-1.5707, 1.5707, 4),
        "joint2": np.linspace(-1.5707, 1.5707, 4),
        "joint3": np.linspace(-1.5707, 1.5707, 4),
        "joint4": np.linspace(-1.5707, 1.5707, 4),
        "joint5": np.linspace(-1.5707, 1.5707, 4),
        "joint6": np.linspace(-1.5707, 1.5707, 4),
        #"joint7": np.linspace(-1.5707, 1.5707, 4)
    }
    
    dataset_nn = {"joints_status": [],
                  "ee_position":   []}

    joints_grid = list(product_dict(**grid))    
    total_combination = len(joints_grid)

    command = Float64MultiArray()
    print("Joints combination to generate: {}".format(total_combination))
    i = 0
    try:
        for current_joints in joints_grid:
            #3 - scriviemere il valore dei giunti nel topic command
            i = i+1
            print("Combination {}/{}".format(i, total_combination))
            joints_command = [current_joints["joint1"], current_joints["joint2"], current_joints["joint3"], current_joints["joint4"], current_joints["joint5"], current_joints["joint6"], 0.0] 
            command.data = joints_command
            print(command.data)
            rospy.loginfo(command)
            pub.publish(command)
            rospy.sleep(0.1) 
            # print(all(joints_velocity < 1e-4))

            # #4 - attendere con un while che le velocità scandano sotto una T (giunti fermi)
            # while(not all(joints_velocity < 1e-4)):
            #     print(joints_velocity)
            #     rospy.sleep(0.1) 
            # print("stable")

            #5 - leggere EE position
            
            state_msg_l = LinkState()
            state_msg_r = LinkState()

            state_msg_l.link_name, state_msg_r.link_name = "iiwa_gripper::left_cube", "iiwa_gripper::right_cube"
            state_msg_l.reference_frame, state_msg_r.reference_frame = '', ''

            set_state_l = rospy.ServiceProxy(
                '/gazebo/get_link_state', GetLinkState)
            state_msg_l = set_state_l(state_msg_l.link_name, state_msg_l.reference_frame)

            set_state_r = rospy.ServiceProxy(
                '/gazebo/get_link_state', GetLinkState)
            state_msg_r = set_state_r(state_msg_r.link_name, state_msg_r.reference_frame)

            x_ee = (state_msg_r.link_state.pose.position.x + state_msg_l.link_state.pose.position.x)/2
            y_ee= (state_msg_r.link_state.pose.position.y + state_msg_l.link_state.pose.position.y)/2
            z_ee = (state_msg_r.link_state.pose.position.z + state_msg_l.link_state.pose.position.z)/2

            print([x_ee, y_ee, z_ee])
            dataset_nn["joints_status"].append(joints_command)
            dataset_nn["ee_position"].append([x_ee, y_ee, z_ee])
            rospy.sleep(delay)  

    except rospy.ServiceException as e:
        print( f"Service call failed: {e}")

if __name__ == "__main__":
    delay = 1       #modificare se serve più tempo per catturare immagini da camera
    print(f"Ogni {delay} secondi ritornerà la posizione dell'ee")
    rospy.init_node('data_colletion', anonymous=True)
    rospy.Subscriber("/iiwa/joint_states", JointState, callback)
    command = Float64MultiArray()
    command.data = [0,0,0,0,0,0,0]
    print(command)
    pub.publish(command)
    iiwa_ee_pos()
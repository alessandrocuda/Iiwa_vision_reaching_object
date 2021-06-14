#!/usr/bin/python3
import rospy
import rospkg
import random
import numpy as np
import pickle

from itertools import product

from gazebo_msgs.srv import GetLinkState
from gazebo_msgs.msg import LinkState

from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

def save_object(obj):
    try:
        with open("data2.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)
 

def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in product(*vals):
        yield dict(zip(keys, instance))

grid = {
    "joint1": np.linspace(-1, 1, 10),
    "joint2": np.linspace(0.1, 1.2, 9),
    #"joint3": np.linspace(-1.5707, 1.5707, 4),
    "joint4": np.linspace(-2.6, 0, 8),
    #"joint5": np.linspace(-1.5707, 1.5707, 4),
    "joint6": np.linspace(0, 1.5707, 7),
    #"joint7": np.linspace(-1.5707, 1.5707, 4)
}

dataset_nn = {"joints_status": [],
              "ee_position":   []}

joints_grid = list(product_dict(**grid))   
current_joints_i = 0
current_joints = [0,0,0,0,0,0,0,0]
total_joints_combination = len(joints_grid)
pub = rospy.Publisher('/iiwa/pos_effort_controller/command', Float64MultiArray, queue_size=10)

stop_collecting_data = False

def myhook():
    print("shutdown time!")

def data_collection_callback(data):
    #print(data.velocity)
    global current_joints_i
    global current_joints
    global stop_collecting_data
    
    command = Float64MultiArray()
    joints = joints_grid[current_joints_i]
    current_joints = [joints["joint1"], joints["joint2"], 0, joints["joint4"], 0, joints["joint6"], 1.57] 
    command.data = current_joints
    #print(command.data)
    #rospy.loginfo(command)
    pub.publish(command)
    if all(np.array(data.velocity[2:]) < 8e-3) and all(np.abs(np.cos(data.position[2:])-np.cos(current_joints)) < 5e-2) and all(np.abs(np.sin(data.position[2:])-np.sin(current_joints)) < 5e-2):
        print("Combination {}/{}".format(current_joints_i+1, total_joints_combination))
        if current_joints_i < total_joints_combination-1:
            print("cambio")
            current_joints_i += 1
        else:
         stop_collecting_data = True

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
        print(current_joints)
        print([x_ee, y_ee, z_ee])
        dataset_nn["joints_status"].append(data.position[2:])
        dataset_nn["ee_position"].append([x_ee, y_ee, z_ee])
        print("saved")
    
    if stop_collecting_data:
        print("spengo")
        save_object(dataset_nn)
        rospy.signal_shutdown("fine raccolta dati")



def data_collection():
    global current_joints
    rospy.init_node('data_collection', anonymous=True)
    rospy.Subscriber('/iiwa/joint_states', JointState, data_collection_callback)
    # Initial movement.
    command = Float64MultiArray()
    command.data = current_joints
    pub.publish(command)
    rospy.on_shutdown(myhook)
    rospy.spin()


if __name__ == '__main__':
    try:
        data_collection()
    except rospy.ROSInterruptException:
        pass
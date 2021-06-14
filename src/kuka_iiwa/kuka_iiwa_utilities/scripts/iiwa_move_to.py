#!/usr/bin/python3
# rosrun kuka_iiwa_utilities iiwa_camera_service.py
# rosrun kuka_iiwa_utilities iiwa_move_to.py

import numpy as np
import random
import rospy

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD

from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from sensor_msgs.msg import Image

from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from kuka_iiwa_utilities.srv import *
import time

import cv2
from cv_bridge import CvBridge, CvBridgeError

pub = rospy.Publisher('/iiwa/pos_effort_controller/command', Float64MultiArray, queue_size=10)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(0.6) # 10hz

from scipy.interpolate import griddata

def get_centre(img): 
    #Convert ROS image to OpenCV image
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(img, "rgb8")
    #Blur the image (BGR), and convert it to the HSV color space
    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #Construct a mask for the color "green"
    greenLower = np.array([111,189,93])
    greenUpper = np.array([179,255,255])
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    #Convert the mask to binary image
    ret,thresh = cv2.threshold(mask,127,255,0)
    #Calculate moments of binary image
    M = cv2.moments(thresh)
    #Calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return [cX, cY]


def create_model():
    model = Sequential()
    model.add(Dense(64, activation="relu"))
    model.add(Dense(7))
    sgd = tf.optimizers.SGD(0.001, momentum = 0.3, nesterov = True)
    adam = tf.optimizers.Adam(learning_rate=0.001)
    model.compile(loss="mean_squared_error", optimizer=adam)
    return model

def create_model_vision():
    model = Sequential()
    model.add(Dense(128, activation="relu"))
    model.add(Dense(3))
    sgd = tf.optimizers.SGD(0.001, momentum = 0.3, nesterov = True)
    adam = tf.optimizers.Adam(learning_rate=0.001)
    model.compile(loss="mean_squared_error", optimizer=adam)
    return model

def move_it(model, model_vision):

    while not rospy.is_shutdown():
        state_msg = ModelState()

        randx = 1 + random.randint(20,50)/100            #basso 1.1 alto 1.7
        randy = -0.7 + random.randint(0,70)/100          #sinistra 0.3 destra -1

        state_msg.model_name = "unit_sphere"
        state_msg.pose.position.x = randx
        state_msg.pose.position.y = randy
        state_msg.pose.position.z = 1.062500

        set_state = rospy.ServiceProxy(
            '/gazebo/set_model_state', SetModelState)
        resp = set_state(state_msg)
        print(state_msg)
        print([randx,randy,1.062500])

        rospy.sleep(1)

        rospy.wait_for_service('/iiwa/utils/get_camera')
        get_camera_image = rospy.ServiceProxy('/iiwa/utils/get_camera', GetCameraImg)
        resp = get_camera_image()
        print("center of the ball")
        resp = get_centre(resp.camera_image)
        print(resp)

        xyz_final = model_vision.predict(np.array(resp).reshape(1,2)).tolist()[0]
        print(xyz_final)
        t_max = 40
        grid_x = np.mgrid[0:t_max:1]
        grid_z1 = griddata(np.array([0, t_max-1]), np.array([[0.6966, -0.33,  2.260], [xyz_final[0], xyz_final[1], 1.18]]), grid_x, method='linear')

        for t in range(t_max):
            joints = model.predict(grid_z1[t].reshape(1,3)).tolist()[0]
            command = Float64MultiArray()
            current_joints = joints
            command.data = current_joints
            #print(command.data)
            #rospy.loginfo(command)
            pub.publish(command)

        rospy.sleep(2)
        command = Float64MultiArray()
        command.data = [0,0,0,0,0,0,0]
        #print(command.data)
        #rospy.loginfo(command)
        pub.publish(command)
        rate.sleep()

if __name__ == "__main__":
    model = create_model()
    model_vision = create_model_vision()
    model.load_weights('./checkpoints/nn_checkpoint_inverse_k')
    model_vision.load_weights('./checkpoints_vision/nn_checkpoint_vision')
    move_it(model, model_vision)

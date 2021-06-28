#!/usr/bin/python3
import numpy as np
import random
import rospy

from sensor_msgs.msg import Image
from kuka_iiwa_utilities.srv import *

img = None

def handle_get_img(req):
    #return the current direction
    global img
    return img

def setup_services():
    set_direction = rospy.Service('/iiwa/utils/get_camera', GetCameraImg, handle_get_img) 

def myhook():
    print("shutdown time!")

def data_collection_callback(data):
    global img
    img = data

def data_collection():
    rospy.init_node('camera_data_collection', anonymous=True)
    rospy.Subscriber('/eye/camera/image_raw', Image, data_collection_callback)
    setup_services()
    rospy.spin()

if __name__ == '__main__':
    try:
        data_collection()
    except rospy.ROSInterruptException:
        pass
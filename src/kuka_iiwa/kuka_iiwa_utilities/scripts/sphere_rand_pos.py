#!/usr/bin/python3
import rospy
import rospkg
import random
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

def sphere_rand_pos():
    rospy.wait_for_service('/gazebo/set_model_state')
    try:
        while True:
            state_msg = ModelState()

            randx = 1 + random.randint(1,70)/100            #basso 1.1 alto 1.7
            randy = -1 + random.randint(0,130)/100          #sinistra 0.3 destra -1

            state_msg.model_name = "unit_sphere"
            state_msg.pose.position.x = randx
            state_msg.pose.position.y = randy
            state_msg.pose.position.z = 1.062500

            set_state = rospy.ServiceProxy(
                '/gazebo/set_model_state', SetModelState)
            resp = set_state(state_msg)
            print(state_msg)

            rospy.sleep(delay)      
    except rospy.ServiceException as e:
        print( f"Service call failed: {e}")

if __name__ == "__main__":
    delay = 1           #modificare se serve più tempo per catturare immagini da camera
    print(f"Ogni {delay} secondi cambierà la posizione della sfera rossa sul tavolo")
    sphere_rand_pos()

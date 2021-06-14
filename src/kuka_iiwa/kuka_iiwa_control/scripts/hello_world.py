#!/usr/bin/env python  

#NOTE: you may need to write #!/usr/bin/env python3 to run this script, depending on your system setting! 
import rospy
if __name__ == '__main__':
    try:
        NODE_NAME='hello_world'
        HZ = rospy.get_param('/iiwa/hello_world/hz', default=2)
        rospy.init_node(NODE_NAME)

        rate = rospy.Rate(HZ)

        while not rospy.is_shutdown():

            rospy.loginfo("Hello world, printed at %dHZ" % HZ)

            #
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
    rospy.spin()
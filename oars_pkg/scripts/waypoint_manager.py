#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16, Float32, Bool, String
from geometry_msgs.msg import Pose2D, Vector3

class WaypointManager:
    def __init__(self):
        self.waypoint_queue = []

        rospy.init_node('waypoint_manager')

        new_waypoint = rospy.Subscriber('new_waypoint', Pose2D, self.new_waypoint_callback)
        clear_waypoints = rospy.Subscriber('clear_waypoints', Bool, self.clear_waypoints_callback)
        rm_waypoint = rospy.Subscriber('rm_waypoint', Bool, self.rm_waypoint_callback)
        reached_waypoint = rospy.Subscriber('reached_waypoint', Bool, self.reached_waypoint_callback)

        self.next_waypoint = rospy.Publisher('next_waypoint', Pose2D, queue_size=1)
        self.has_waypoint = rospy.Publisher('has_waypoint', Bool, queue_size=1)

    def run(self):
        r = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.manage()
            r.sleep()

    def new_waypoint_callback(self, waypoint):
        self.waypoint_queue.append(waypoint)

    def clear_waypoints_callback(self, msg):
        if msg.data:
            self.waypoint_queue = []

    def rm_waypoint_callback(self, msg):
        if len(self.waypoint_queue) == 0:
            return
        if msg.data:
            self.waypoint_queue.pop()

    def reached_waypoint_callback(self, msg):
        if len(self.waypoint_queue) == 0:
            return

        if msg.data:
            self.waypoint_queue.pop(0)

    def manage(self):
        if self.waypoint_queue:
            self.next_waypoint.publish(self.waypoint_queue[0])
        self.has_waypoint.publish(bool(self.waypoint_queue))

if __name__ == '__main__':
    manager = WaypointManager()
    manager.run()

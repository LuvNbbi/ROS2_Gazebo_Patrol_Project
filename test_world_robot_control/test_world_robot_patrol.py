import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
import math

class TestWorldRobotPatrol(Node):
    def __init__(self):
        super().__init__('test_world_robot_patrol')
        self.client = ActionClient(
            self,
            NavigateToPose,
            '/navigate_to_pose'
        )
        
        self.waypoints = [
            (11.258322, 2.370551),
            (11.462446, -4.571676),
            (5.149115, 2.174214),
            (5.031324, -4.86247),
            (-0.80037, 2.077277),
            (-0.91204, -5.02523)
        ]
                
        self.index = 0

        self.timer = self.create_timer(2.0, self.send_goal)
        self.sent = False
    
    def send_goal(self):
        if self.sent:
            return
    

        if not self.client.wait_for_server(timeout_sec=0.5):
            return
        
        x, y = self.waypoints[self.index]

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()

        goal_msg.pose.header.frame_id = "map"

        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y

        self.client.send_goal_async(goal_msg).add_done_callback(
            self.goal_response_callback
        )

        self.get_logger().info(f'Going to waypoint {self.index}')

        self.sent = True
    
    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            self.sent = False
            return
        
        self.get_logger().info("Goal accepted")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        self.get_logger().info("Goal reached")

        self.index +=1

        if self.index >= len(self.waypoints):
            self.index = 0
        
        self.sent = False

def main():
    rclpy.init()
    node = TestWorldRobotPatrol()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
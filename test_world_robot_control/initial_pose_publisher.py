import rclpy

from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped


class InitialPosePublisher(Node):

    def __init__(self):
        super().__init__('initial_pose_publisher')

        self.publisher = self.create_publisher(
            PoseWithCovarianceStamped,
            '/initialpose',
            10
        )

        self.timer = self.create_timer(
            2.0,
            self.publish_pose
        )

        self.published = False

    def publish_pose(self):

        if self.published:
            return

        msg = PoseWithCovarianceStamped()

        msg.header.frame_id = 'map'

        msg.pose.pose.position.x = 0.0
        msg.pose.pose.position.y = 0.0
        msg.pose.pose.position.z = 0.0

        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = 0.0
        msg.pose.pose.orientation.w = 1.0

        # RViz 2D Pose Estimate와 비슷하게
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.0685

        self.publisher.publish(msg)

        self.get_logger().info('Initial Pose Published')

        self.published = True


def main(args=None):

    rclpy.init(args=args)

    node = InitialPosePublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
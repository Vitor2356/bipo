import rclpy
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory

# ros2 run simu_bipo joint_trajectory_client.py

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("joint_trajectory_action_client")

    # Crie um cliente de ação
    action_client = ActionClient(node, FollowJointTrajectory, "joint_trajectory_controller/follow_joint_trajectory")

    # Espere até que o servidor de ação esteja pronto
    if not action_client.wait_for_server(timeout_sec=10.0):
        node.get_logger().error("Servidor de ação não está disponível.")
        return

    # Crie uma mensagem de meta e preencha-a com sua trajetória desejada
    goal_msg = FollowJointTrajectory.Goal()
    # Preencha a mensagem de meta com a trajetória desejada

    # Envie a meta para o servidor de ação
    send_goal_future = action_client.send_goal_async(goal_msg)

    # Espere pelo resultado
    rclpy.spin_until_future_complete(node, send_goal_future)

    if send_goal_future.result() is not None:
        goal_handle = send_goal_future.result()
        if goal_handle.accepted:
            node.get_logger().info("Meta aceita pelo servidor de ação.")
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(node, result_future)
            if result_future.result():
                node.get_logger().info(f"Resultado da ação: {result_future.result().result_message}")
            else:
                node.get_logger().error("Falha ao obter o resultado da ação.")
        else:
            node.get_logger().error("Meta rejeitada pelo servidor de ação.")
    else:
        node.get_logger().error("Falha ao enviar a meta para o servidor de ação.")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

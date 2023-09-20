import rclpy
from rclpy.action import ActionClient
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from action_msgs.msg import GoalStatus

def main():
    rclpy.init()

    action_client = ActionClient(
        rclpy.create_node('testwalk_position_client'),
        JointTrajectory,
        'nome_da_sua_acao'  # Substitua pelo nome da sua ação
    )

    goal_msg = JointTrajectory()
    goal_msg.joint_names = ['j1', 'j2']  # Substitua pelos nomes das suas juntas

    point = JointTrajectoryPoint()
    point.positions = [0.5, 0.7]  # Substitua pelas posições desejadas para j1 e j2
    point.time_from_start = rclpy.time.Duration(seconds=5)  # Tempo de duração para atingir as posições

    goal_msg.points.append(point)

    action_client.wait_for_server()
    send_goal_future = action_client.send_goal_async(goal_msg)

    rclpy.spin_until_future_complete(rclpy.create_node('testwalk_position_client'), send_goal_future)

    if send_goal_future.result() is not None:
        goal_handle = send_goal_future.result()
        if goal_handle.accepted:
            print("Ação aceita. Movendo as juntas para as posições desejadas.")
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(rclpy.create_node('testwalk_position_client'), result_future)
            if result_future.result().status == GoalStatus.STATUS_SUCCEEDED:
                print("Ação concluída com sucesso.")
            else:
                print("Ação não foi bem-sucedida.")
        else:
            print("Ação não aceita.")
    else:
        print("Falha ao enviar ação.")

    rclpy.shutdown()

if __name__ == '__main__':
    main()
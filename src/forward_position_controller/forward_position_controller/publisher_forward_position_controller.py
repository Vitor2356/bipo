#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import yaml
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

class PublisherForwardPosition(Node):
    def __init__(self):
        super().__init__("publisher_forward_position_controller")
        self.declare_parameter("yaml_file", "config/publisher_test.yaml")
        yaml_file = self.get_parameter("yaml_file").get_parameter_value().string_value

        self.get_logger().info(f"Carregando trajetória do arquivo: {yaml_file}")

        # Carregar a trajetória do arquivo YAML
        self.trajectory = self.load_trajectory(yaml_file)

        if not self.trajectory:
            self.get_logger().error("Trajetória vazia ou arquivo inválido. Verifique o arquivo YAML.")
            return
        else:
            self.get_logger().info("Trajetória carregada com sucesso.")

        # Criar publisher único para o controlador
        self.publisher = self.create_publisher(Float64MultiArray, '/forward_position_controller/commands', 10)
        self.get_logger().info("Criado publisher no tópico /forward_position_controller/commands")

        # Variáveis de controle para publicar a trajetória com tempos definidos
        self.current_goal = 0
        self.current_time = 0.0
        self.next_publish_time = self.trajectory['points'][0]['time_from_start']
        self.timer = self.create_timer(0.01, self.publish_trajectory)

    def load_trajectory(self, yaml_file):
        package_share = get_package_share_directory('forward_position_controller')
        yaml_path = Path(package_share) / yaml_file

        if not yaml_path.exists():
            self.get_logger().error(f"Arquivo YAML não encontrado: {yaml_path}")
            return None

        with yaml_path.open('r') as file:
            data = yaml.safe_load(file)

        # Exibir o conteúdo do YAML carregado para depuração
        self.get_logger().info(f"Conteúdo do YAML carregado: {data}")

        # Verificar se a estrutura esperada está presente
        if 'publisher_forward_position_controller' not in data:
            self.get_logger().error("Chave 'publisher_forward_position_controller' não encontrada no YAML.")
            return None

        trajectory = data['publisher_forward_position_controller']['ros__parameters']

        # Verificar se as chaves esperadas existem dentro do arquivo
        if 'joint_names' not in trajectory or 'points' not in trajectory:
            self.get_logger().error("Chaves 'joint_names' ou 'points' faltando no YAML.")
            return None

        return trajectory

    def publish_trajectory(self):
        if self.current_goal >= len(self.trajectory['points']):
            self.current_goal = 0
            self.current_time = 0.0

        self.current_time += 0.01
        if self.current_time >= self.next_publish_time:
            point = self.trajectory['points'][self.current_goal]
            msg = Float64MultiArray()
            msg.data = point['positions']  # Todas as posições em um array
            self.publisher.publish(msg)  # Publica no único tópico

            self.get_logger().info(f'Publicando {msg.data} no tópico /forward_position_controller/commands')

            self.current_goal += 1
            if self.current_goal < len(self.trajectory['points']):
                self.next_publish_time = self.trajectory['points'][self.current_goal]['time_from_start']

def main(args=None):
    rclpy.init(args=args)
    publisher_forward_position_controller = PublisherForwardPosition()
    try:
        rclpy.spin(publisher_forward_position_controller)
    except KeyboardInterrupt:
        pass
    finally:
        publisher_forward_position_controller.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

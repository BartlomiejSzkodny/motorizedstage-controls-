from programFiles.stage import Stage
from serial.tools import list_ports
from programFiles.DAOs.prior_connector import PriorConnector
from programFiles.DAOs.yaml.yaml_manager import YamlData


class StageCli():
    def __init__(self):
        self.__yaml = YamlData()
        self.__prior_connector = PriorConnector(self.__yaml.get_stage_ddl_path(), BUFFER_SIZE)
        self.__stage = Stage(self.__prior_connector)
        print("*\n"*20)
        print("Cli is now running")
        print("Please enter a command")
        print("Type help to see the list of commands")

    def run_command(self, command: str):
        if command == "help":
            print("*\n"*5)
            print("List of commands:")
            print("help - shows the list of commands")
            print("velmove - moves the stage at a specific velocity")
            print("goto - moves the stage")
            print("exit - exits the program")
            print("connect - connects to the stage")

        if command == "connect":
            print("Available COM ports:")
            ports = list_ports.comports()
            ports_sanitized = [
                port for port in ports if "n/a" not in port.description.lower()]
            if not ports_sanitized:
                print("No COM ports found.")
            else:
                for i, port in enumerate(ports_sanitized):
                    print(f"{i}->{port.device} - {port.description}")
                k = input("Enter the COM port: ")
                self.__stage.init_prior(ports[int(k)])

        if command == "velmove":
            x = input("Enter the x position: ")
            y = input("Enter the y position: ")
            speed = input("Enter the speed: ")
            self.__stage.move_at_velocity(x, y, speed)

        if command == "goto":
            x = input("Enter the x position: ")
            y = input("Enter the y position: ")
            speed = input("Enter the speed: ")
            self.__stage.goto_position(x, y, speed)

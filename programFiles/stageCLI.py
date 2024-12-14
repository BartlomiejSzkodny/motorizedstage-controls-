from programFiles.stage import Stage

class StageCli():
    def __init__(self):
        self.stage = Stage()
        print("*\n"*20)
        print("Cli is now running")
        print("Please enter a command")
        print("Type help to see the list of commands")
    
    def run_command(self, command: str):
        if command == "help":
            print("*\n"*5)
            print("List of commands:")
            print("help - shows the list of commands")
            print("exit - exits the program")
        if command == "velmove":
            x = input("Enter the x position: ")
            y = input("Enter the y position: ")
            speed = input("Enter the speed: ")
            self.stage.move_at_velocity(x, y, speed)
        if command == "goto":
            x = input("Enter the x position: ")
            y = input("Enter the y position: ")
            speed = input("Enter the speed: ")
            self.stage.goto_position(x, y, speed)
        
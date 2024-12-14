class StageCli:
    def __init__(self):
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
        
from programFiles.stage import Stage
from programFiles.stageCLI import StageCli


class LaserStageControll(Stage) :
    def __init__(self):
        print("LaserStageControll initialized")
        self._stage = Stage()
        print("Stage initialized")
        self._stageCli = StageCli()
        print("StageCLI initialized")
        self.LaserComPort = ""
        self.Exit = False

    def run(self):
        print("LaserStageControll is now running")
        while not self.Exit:
            command = input("Enter a command: ")
            self._stageCli.run_command(command)
            if command == "exit":
                self.Exit = True
            

        
        
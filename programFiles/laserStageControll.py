from programFiles.stage import Stage
from programFiles.stageCLI import StageCli
from programFiles.DAOs.prior_connector import PriorConnector


class LaserStageControll(Stage) :
    def __init__(self):
        self._stage = Stage()
        self._stageCli = StageCli()
        self.LaserComPort = ""
        self.Exit = False

    def run(self):
        while not self.Exit:
            command = input("Enter a command: ")
            if command == "exit":
                self.Exit = True
                break
            self._stageCli.run_command(command)
            
            

        
        
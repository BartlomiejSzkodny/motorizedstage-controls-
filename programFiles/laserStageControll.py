from stage import Stage


class LaserStageControll(Stage) :
    def __init__(self):
        self._stage = Stage()

    def run(self):
        self._stage.init_prior("COM3")
        
import logging
from typing import List
from threading import Lock
from programFiles.errors.service_errors import ServiceError
from programFiles.DAOs.prior_connector import PriorConnector
from programFiles.errors.errors import StageExecuteError
from programFiles.factories.commands_factory import CommandsFactory
from programFiles.models.stage_models import DaoResponse, DaoError

"""_summary_: Class that represents the stage DAO
"""
class StageDAO:
    """_summary_: Constructor for the StageDAO class
    :param prior_connector: PriorConnector
    """
    def __init__(self, prior_connector: PriorConnector):
        self.__logger = logging.getLogger(__name__)
        self.__stage = prior_connector
        self.__actual_speed = 1000#default speed for the stage
        self.running = False
        self.position = [0, 0] #default position for the stage
        self.__running_lock = Lock()

        """_summary_: function to move the stage to a specific position
        :param x: int
        :param y: int
        :param speed: int
        :return: DaoResponse it contains the response from the stage
        """
    def goto_position(self, x: int, y: int, speed: int) -> DaoResponse:
        try:
            if self.__actual_speed != speed:
                set_speed_command = CommandsFactory.set_max_speed(speed)
                self.__stage.execute(set_speed_command)
                self.__actual_speed = speed
            command = CommandsFactory.goto_position(x, y)
            response = self.__stage.execute(command)
            return DaoResponse[str](data=response, error=DaoError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return DaoResponse[str](data="", error=DaoError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                            return_status=err.msg))

        """_summary_: function to move the stage at a specific velocity
        :param x_speed: int
        :param y_speed: int
        :return: DaoResponse it contains the response from the stage
        """
    def move_at_velocity(self, x_speed: int, y_speed: int) -> DaoResponse:
        try:
            command = CommandsFactory.move_at_velocity(x_speed, y_speed)
            return_status = self.__stage.execute(command)
            return DaoResponse[str](data=return_status, error=DaoError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return DaoResponse[str](data="", error=DaoError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                            return_status=err.msg))

        """_summary_: function to check the stage limits
        :return: DaoResponse it contains the response from the stage
        """
    def check_stage_limits(self) -> DaoResponse:
        try:
            command = CommandsFactory.get_limits()
            stage_limits = int(self.__stage.execute(command))
            return DaoResponse[int](data=stage_limits, error=DaoError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return DaoResponse[str](data="", error=DaoError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                            return_status=err.msg))

        """_summary_: function to set the stage position, for example to calibrate the stage
        """
    def set_position(self, x: int, y: int) -> DaoResponse:
        try:
            command = CommandsFactory.set_position(x, y)
            return_status = self.__stage.execute(command)
            return DaoResponse[str](data=return_status, error=DaoError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return DaoResponse[str](data="", error=DaoError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                            return_status=err.msg))

        """_summary_: function to get the stage position
        """
    def get_position(self) -> DaoResponse[List]:
        try:
            command = CommandsFactory.get_position()
            position = self.__stage.execute(command)
            self.__logger.info('**************************')
            position = [int(coordinate) for coordinate in position.split(',')]
            self.position = position
            self.__logger.info(position)
            return DaoResponse[List](data=position, error=DaoError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return DaoResponse[List](data=[], error=DaoError(error=ServiceError.STAGE_ERROR,
                                                             description=str(err),
                                                             return_status=err.msg))

        """_summary_: function to get the stage name
        """
    def get_running(self) -> DaoResponse[bool]:
        try:
            command = CommandsFactory.get_busy()
            running = self.__stage.execute(command)
            self.set_running(True if running != "0" else False)
            return DaoResponse[bool](data=running != "0", error=DaoError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return DaoResponse[bool](data=None, error=DaoError(error=ServiceError.STAGE_ERROR,
                                                               description=str(err),
                                                               return_status=err.msg))
        """_summary_: function to stop the stage
        """
    def stop_stage(self) -> DaoResponse[bool]:
        try:
            command = CommandsFactory.stop_smoothly()
            stopped = self.__stage.execute(command)
            return DaoResponse[bool](data=stopped == 0, error=DaoError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return DaoResponse[bool](data=None, error=DaoError(error=ServiceError.STAGE_ERROR,
                                                               description=str(err),
                                                               return_status=err.msg))
        """_summary_: function to set the running status of the stage
        """
    def set_running(self, running: bool):
        self.__running_lock.acquire()
        self.running = running
        self.__running_lock.release()
        """_summary_: function to get the running status of the stage
        """
    def get_running(self) -> bool:
        self.__running_lock.acquire()
        running = self.running
        self.__running_lock.release()
        return running

from programFiles.errors.service_errors import ServiceError
from programFiles.DAOs.prior_connector import PriorConnector
from programFiles.DAOs.yaml.yaml_manager import YamlData
from programFiles.DAOs.stage_dao import StageDAO
from programFiles.errors.errors import StageExecuteError
from programFiles.factories.commands_factory import CommandsFactory
from programFiles.models.stage_models import DaoResponse, DaoError

class Stage:
    """Class that represents the stage object
    """
    def __init__(self):
        self.__prior_connector = PriorConnector(YamlData().get_stage_ddl_path(), 1000)
        self.__stage_dao = StageDAO(self.__prior_connector)
        self.__actual_speed = 1000
        self.__is_prior_connected = False

        """function to initialize the prior stage, it connects to the stage via COM port and opens a session
        :param com_port: str
        :return: ServiceError
        """
    def init_prior(self, com_port: str) -> ServiceError:
        try:
            com_port = int(com_port[3:])
            self.__prior_connector.initialize(com_port)
            response = self.__prior_connector.open_session()
            if response == "0":
                self.__is_prior_connected = True
                return ServiceError.OK
            return ServiceError.PRIOR_CONNECT_ERROR
        except Exception as e:
            return ServiceError.PRIOR_CONNECT_ERROR
    
    def goto_position(self, x: int, y: int, speed: int) -> DaoResponse:
        try:
            if self.__actual_speed != speed:
                set_speed_command = CommandsFactory.set_max_speed(speed)
                self.__prior_connector.execute(set_speed_command)
                self.__actual_speed = speed
            command = CommandsFactory.goto_position(x, y)
            response = self.__prior_connector.execute(command)
            return DaoResponse[str](data=response, error=DaoError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return DaoResponse[str](data="", error=DaoError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                            return_status=err.msg))

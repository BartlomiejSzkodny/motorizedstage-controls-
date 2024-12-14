from programFiles.errors.service_errors import ServiceError
from programFiles.DAOs.prior_connector import PriorConnector

class Stage:
    """Class that represents the stage object
    """
    def __init__(self):
        self.__prior_connector = PriorConnector()
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

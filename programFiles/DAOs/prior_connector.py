import logging #logging module for storing logs
from ctypes import create_string_buffer #ctypes module for creating buffer
import ctypes
from threading import Lock
#--------------------------------------------
from programFiles.errors.errors import StageConnectionError, StageOpenSessionError, StageCloseSessionError, \
    StageExecuteError
from programFiles.factories.commands_factory import CommandsFactory


class PriorConnector:
    def __init__(self, path: str, reading_buffer_size: int):
        self.__logger = logging.getLogger(__name__)
        self.__stage_dll_path = path #path to the dll file with the stage commands
        self.__read_buffer = create_string_buffer(reading_buffer_size) #buffer for reading the response
        self.__SDKPrior = None 
        self.__session_id = None
        self.__com_port = None
        self.__lock = Lock()#lock for thread safety

        """_summary_: function to initialize the prior stage, it connects to the stage via COM port
        :param com_port: int
        :return: None
        """
    def initialize(self, com_port: int):
        self.__com_port = com_port #com port for the stage
        self.__SDKPrior = ctypes.WinDLL(self.__stage_dll_path)#loading the dll file
        return_status = self.__SDKPrior.PriorScientificSDK_Initialise()#initializing the stage connection
        if return_status:#if the return status is not 0, raise an error
            self.__logger.critical(f"Prior initialization error: {return_status}")
            raise StageConnectionError(int(return_status))
        else:
            self.__logger.info(f"Prior initialized: {return_status}")

        """_summary_: function to open a session with the stage
        :return: str
        """
    def open_session(self):
        self.__session_id = self.__SDKPrior.PriorScientificSDK_OpenNewSession()
        if self.__session_id < 0:
            self.__logger.critical(f"Open session error: {self.__session_id}")
            raise StageOpenSessionError(str(self.__session_id))
        else:
            self.__logger.info(f"Session opened: {self.__session_id}")
            return self.execute(CommandsFactory.connect_stage(self.__com_port))
        

        """_summary_: function to close the session with the stage
        """
    def close_session(self):
        return_status = self.__SDKPrior.PriorScientificSDK_CloseSession(self.__session_id)
        if return_status:
            self.__logger.critical(f"Session close error: {return_status}")
            raise StageCloseSessionError(int(return_status))
        else:
            self.__logger.info(f"Session closed: {return_status}")
        data = self.__read_buffer.value.decode()
        return data
    
        """_summary_: function to disconnect the stage
        """
    def disconnect_stage(self) -> str:
        return self.execute(CommandsFactory.disconnect_stage(self.__com_port))

        """_summary_: function to execute a command on the stage
        """
    def execute(self, message: str) -> str:
        self.__lock.acquire()
        self.__logger.info(f"Executed message: {message}")
        return_status = self.__SDKPrior.PriorScientificSDK_cmd(self.__session_id,
                                                               create_string_buffer(message.encode()),
                                                               self.__read_buffer)
        if return_status:
            self.__logger.critical(f"Api error {return_status}")
            self.__lock.release()
            raise StageExecuteError(int(return_status))
        else:
            data = self.__read_buffer.value.decode()
            self.__logger.info(f"Success {data}")
        self.__lock.release()
        return data

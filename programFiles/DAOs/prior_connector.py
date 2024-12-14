import logging
from ctypes import create_string_buffer
import ctypes
from threading import Lock
from programFiles.errors.errors import StageConnectionError, StageOpenSessionError, StageCloseSessionError, \
    StageExecuteError
from programFiles.factories.commands_factory import CommandsFactory


class PriorConnector:
    def __init__(self, path: str, reading_buffer_size: int):
        self.__logger = logging.getLogger(__name__)
        self.__stage_dll_path = path
        self.__read_buffer = create_string_buffer(reading_buffer_size)
        self.__SDKPrior = None
        self.__session_id = None
        self.__com_port = None
        self.__lock = Lock()

    def initialize(self, com_port: int):
        self.__com_port = com_port
        self.__SDKPrior = ctypes.WinDLL(self.__stage_dll_path)
        return_status = self.__SDKPrior.PriorScientificSDK_Initialise()
        if return_status:
            self.__logger.critical(f"Prior initialization error: {return_status}")
            raise StageConnectionError(int(return_status))
        else:
            self.__logger.info(f"Prior initialized: {return_status}")

    def open_session(self):
        self.__session_id = self.__SDKPrior.PriorScientificSDK_OpenNewSession()
        if self.__session_id < 0:
            self.__logger.critical(f"Open session error: {self.__session_id}")
            raise StageOpenSessionError(str(self.__session_id))
        else:
            self.__logger.info(f"Session opened: {self.__session_id}")
            return self.execute(CommandsFactory.connect_stage(self.__com_port))

    def close_session(self):
        return_status = self.__SDKPrior.PriorScientificSDK_CloseSession(self.__session_id)
        if return_status:
            self.__logger.critical(f"Session close error: {return_status}")
            raise StageCloseSessionError(int(return_status))
        else:
            self.__logger.info(f"Session closed: {return_status}")
        data = self.__read_buffer.value.decode()
        return data

    def disconnect_stage(self) -> str:
        return self.execute(CommandsFactory.disconnect_stage(self.__com_port))

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

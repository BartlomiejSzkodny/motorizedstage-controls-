from enum import Enum


class ServiceError(Enum):
    OK = (0, "OK")
    STAGE_ERROR = (1, "STAGE_ERROR")
    STAGE_OPEN_SESSION_ERROR = (2, "STAGE_OPEN_SESSION_ERROR")
    PRIOR_CONNECT_ERROR = (3, "PRIOR_CONNECT_ERROR")
    PRIOR_DISCONNECT_ERROR = (4, "PRIOR_DISCONNECT_ERROR")
    STAGE_CALIBRATION_ERROR = (4, "STAGE_CALIBRATION_ERROR")
    STAGE_BUFFER_ERROR = (5, "STAGE_BUFFER_ERROR")
    LASER_ERROR = (6, "LASER_ERROR")
    DXF_ERROR = (7, "DXF_ERROR")


    def __init__(self, code: int, description: str):
        self.__code = code
        self.__description = description

    @property
    def code(self) -> int:
        return self.__code

    @property
    def description(self) -> str:
        return self.__description

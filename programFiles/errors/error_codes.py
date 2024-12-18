from enum import Enum


class StageErrorCodes(Enum):
    PRIOR_OK						= 0
    PRIOR_UNRECOGNISED_COMMAND		=-10001
    PRIOR_FAILEDTOOPENPORT			=-10002
    PRIOR_FAILEDTOFINDCONTROLLER	=-10003
    PRIOR_NOTCONNECTED				=-10004
    PRIOR_ALREADYCONNECTED			=-10005
    PRIOR_INVALID_PARAMETERS		=-10007
    PRIOR_UNRECOGNISED_DEVICE		=-10008
    PRIOR_APPDATAPATHERROR			=-10009
    PRIOR_LOADERERROR				=-10010
    PRIOR_CONTROLLERERROR			=-10011
    PRIOR_NOTIMPLEMENTEDYET			=-10012
    PRIOR_COMMS_ERROR				=-10013
    PRIOR_UNEXPECTED_ERROR			=-10100
    PRIOR_SDK_NOT_INITIALISED		=-10200
    PRIOR_SDK_INVALID_SESSION		=-10300
    PRIOR_SDK_NOMORE_SESSIONS		=-10301

    PRIOR_NO_STAGE				=1
    PRIOR_NOT_IDLE				=2
    PRIOR_NO_DRIVE				=3
    PRIOR_STRING_PARSE			=4
    PRIOR_COMMAND_NOT_FOUND		=5
    PRIOR_INVALID_SHUTTER		=6
    PRIOR_NO_FOCUS	      		=7
    PRIOR_VALUE_OUT_OF_RANGE	=8
    PRIOR_INVALID_WHEEL			=9
    PRIOR_ARG1_OUT_OF_RANGE		=10
    PRIOR_ARG2_OUT_OF_RANGE		=11
    PRIOR_ARG3_OUT_OF_RANGE		=12
    PRIOR_ARG4_OUT_OF_RANGE		=13
    PRIOR_ARG5_OUT_OF_RANGE		=14
    PRIOR_ARG6_OUT_OF_RANGE		=15
    PRIOR_INCORRECT_STATE		=16
    PRIOR_NO_FILTER_WHEEL		=17
    PRIOR_QUEUE_FULL			=18
    PRIOR_COMP_MODE_SET			=19
    PRIOR_SHUTTER_NOT_FITTED   	=20
    PRIOR_INVALID_CHECKSUM     	=21
    PRIOR_NOT_ROTARY			=22
    PRIOR_NO_FOURTH_AXIS		=40
    PRIOR_AUTOFOCUS_IN_PROG 	=41
    PRIOR_NO_VIDEO          	=42
    PRIOR_NO_ENCODER          	=43
    PRIOR_SIS_NOT_DONE			=44
    PRIOR_NO_VACUUM_DETECTOR	=45
    PRIOR_NO_SHUTTLE			=46
    PRIOR_VACUUM_QUEUED			=47
    PRIOR_SIZ_NOT_DONE			=48
    PRIOR_NOT_SLIDE_LOADER		=49
    PRIOR_ALREADY_PRELOADED		=50
    PRIOR_STAGE_NOT_MAPPED     	=51
    PRIOR_TRIGGER_NOT_FITTED    =52
    PRIOR_INTERPOLATOR_NOT_FITTED  =53
    PRIOR_THETA_NOT_FITTED		=54
    PRIOR_PIEZO_NOT_FITTED		=55
    PRIOR_WRITE_FAIL			=80
    PRIOR_ERASE_FAIL			=81
    PRIOR_NO_DEVICE				=128
    PRIOR_NO_PMD_AXIS			=129

    @classmethod
    def get_stage_error(cls, code: int) -> str:
        for error in list(cls):
            if error.value == code:
                return str(error)
        return "No such error code"

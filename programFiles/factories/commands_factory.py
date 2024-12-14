from app.stage.enums.stage_commands import BasicCommands, ControlCommands


class CommandsFactory:

    @staticmethod
    def connect_stage(port: int) -> str:
        return BasicCommands.CONNECT.command.format(port)

    @staticmethod
    def disconnect_stage(port: int) -> str:
        return BasicCommands.DISCONNECT.command.format(port)

    @staticmethod
    def get_last_error_code() -> str:
        return BasicCommands.LAST_ERROR_CODE.command

    @staticmethod
    def stop_smoothly() -> str:
        return BasicCommands.STOP_SMOOTHLY.command

    @staticmethod
    def stop_immediately() -> str:
        return BasicCommands.STOP_IMMEDIATELY.command

    @staticmethod
    def get_serial_number() -> str:
        return BasicCommands.GET_SERIAL_NUMBER.command

    @staticmethod
    def get_flag() -> str:
        return BasicCommands.GET_FLAG.command

    @staticmethod
    def set_flag() -> str:
        return BasicCommands.SET_FLAG.command

    @staticmethod
    def get_ilock() -> str:
        return BasicCommands.GET_ILOCK.command

    @staticmethod
    def get_stage_name() -> str:
        return BasicCommands.STAGE_GET_NAME.command

    @staticmethod
    def get_busy() -> str:
        return ControlCommands.STAGE_BUSY_GET.command

    @staticmethod
    def get_position() -> str:
        return ControlCommands.STAGE_POSITION_GET.command

    @staticmethod
    def set_position(x: int, y: int) -> str:
        return ControlCommands.STAGE_POSITION_SET.command.format(x, y)

    @staticmethod
    def goto_position(x: int, y: int) -> str:
        return ControlCommands.STAGE_GOTO_POSITION.command.format(x, y)

    @staticmethod
    def move_relative(x: int, y: int) -> str:
        return ControlCommands.STAGE_MOVE_RELATIVE.command.format(x, y)

    @staticmethod
    def move_at_velocity(x: int, y: int) -> str:
        return ControlCommands.STAGE_MOVE_AT_VELOCITY.command.format(x, y)

    @staticmethod
    def get_steps_per_microns() -> str:
        return ControlCommands.STAGE_GET_STEPS_PER_MICRONS.command

    @staticmethod
    def get_limits() -> str:
        return ControlCommands.STAGE_GET_LIMITS.command

    @staticmethod
    def get_speed() -> str:
        return ControlCommands.STAGE_GET_SPEED.command

    @staticmethod
    def set_max_speed(speed: int) -> str:
        return ControlCommands.STAGE_SET_SPEED.command.format(speed)

    @staticmethod
    def get_acc() -> str:
        return ControlCommands.STAGE_GET_ACC.command

    @staticmethod
    def set_max_acc(acc: int) -> str:
        return ControlCommands.STAGE_SET_ACC.command.format(acc)

    @staticmethod
    def stage_get_jerk() -> str:
        return ControlCommands.STAGE_GET_JERK.command

    @staticmethod
    def stage_set_jerk(time: int) -> str:
        return ControlCommands.STAGE_SET_JERK.command.format(time)

    @staticmethod
    def enable_joystick(enable: bool) -> str:
        if enable:
            return ControlCommands.ENABLE_JOYSTICK.command
        else:
            return ControlCommands.DISABLE_JOYSTICK.command

    @staticmethod
    def stage_get_step_size() -> str:
        return ControlCommands.STAGE_GET_STEP_SIZE.command

    @staticmethod
    def set_step_size(step_size: int) -> str:
        return ControlCommands.STAGE_SET_STEP_SIZE.command.format(step_size)

    @staticmethod
    def get_encoder_x_fitted() -> str:
        return ControlCommands.GET_ENCODER_X_FITTED.command

    @staticmethod
    def get_encoder_y_fitted() -> str:
        return ControlCommands.GET_ENCODER_Y_FITTED.command

    @staticmethod
    def get_ttl_input_state() -> str:
        return ControlCommands.GET_TTL_INPUT_STATE.command

    @staticmethod
    def get_ttl_output_state() -> str:
        return ControlCommands.GET_TTL_OUTPUT_STATE.command

    @staticmethod
    def set_ttl_output_state(state: int) -> str:
        return ControlCommands.SET_TTL_OUTPUT_STATE.command.format(state)

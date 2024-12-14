from enum import Enum


class BasicCommands(Enum):
    # Description:
    # Establish a communications connection between the DLL and the controller on the specified port.
    # Result: "0"
    # Params: {port}
    CONNECT = "controller.connect {}"

    # Description:
    # Closes the currently open communications channel to the controller.
    # Result: "0"
    DISCONNECT = "controller.disconnect"

    # Description:
    # Returns the last error code
    # Result: Last error code
    LAST_ERROR_CODE = "controller.lasterror.get"

    # Description:
    # Stops all axes moving in a controlled fashion, following the acceleration and jerk settings for each axis.
    # Positional accuracy is maintained.
    # Result: "0"
    STOP_SMOOTHLY = "controller.stop.smoothly"

    # Description:
    # Stops all axes moving immediately, ignoring any acceleration and jerk settings for each axis.
    # Positional accuracy may be lost and re-initialisation of individual axes is recommended.
    # Result: "0"
    STOP_IMMEDIATELY = "controller.stop.abruptly"

    # Description:
    # Returns controller serial number.
    # Result: E.g. “577892”
    GET_SERIAL_NUMBER = "controller.serialnumber.get"

    # Description:
    # Returns a generic flag as an unsigned 32-bit value as hex string. The flag value is “0” following a power on.
    # The user is free to use as required. A common use is to have it as a warm start flag,
    # whereby after Connect() you can determine whether the controller has been powered off since last disconnect
    # Result: 32-bit Flag value in HEX format ie ABCD1234
    GET_FLAG = "controller.flag.get"

    # Description:
    # Sets a generic flag as an unsigned 32-bit integer.
    # Result: "0"
    # Params: {flag}
    SET_FLAG = "controller.flag.set {}"

    # Description:
    # Return the status of the Ilock
    # Result: Eg "0", "1"
    GET_ILOCK = "controller.ilock.get"

    # Description:
    # Return the name of the stage attached
    # Result: name or NONE
    STAGE_GET_NAME = "controller.stage.name.get"

    def __init__(self, command: str):
        self.__command = command

    @property
    def command(self) -> str:
        return self.__command


class ControlCommands(Enum):
    # Description:
    # Gets the busy (moving) status of the stage
    # Result: “0” idle, “1” X moving, “2” Y moving, “3” both X&Y moving
    STAGE_BUSY_GET = "controller.stage.busy.get"

    # Description:
    # Returns the current stage XY position in microns, separated ','
    # Result: “X,Y” ie “1234,5678”
    STAGE_POSITION_GET = "controller.stage.position.get"

    # Description:
    # sets position of stage when stage is not busy
    # Result: 0
    # Params: {X}, {Y}
    STAGE_POSITION_SET = "controller.stage.position.set {} {}"

    # Description:
    # Request the stage to move to the given position using the existing speed, acceleration and curve settings
    # Result: 0
    # Params: {X}, {Y}
    STAGE_GOTO_POSITION = "controller.stage.goto-position {} {}"

    # Description:
    # Request the stage to move relative to its current position
    # Result: 0
    # Params: {X} {Y}
    STAGE_MOVE_RELATIVE = "controller.stage.move-relative {} {}"

    # Description:
    # Request the stage to move at a constant velocity of X and Y microns/s.
    # This is a float value and the controller will round that down to the next whole microstep velocity.
    # Result: 0
    # Params: {X} {Y}
    STAGE_MOVE_AT_VELOCITY = "controller.stage.move-at-velocity {} {}"

    # Description:
    # Returns the number of whole microsteps per micron.
    # Result: f.i. 25
    STAGE_GET_STEPS_PER_MICRONS = "controller.stage.steps-per-micron.get"

    # Description:
    # Returns the limit switch state for the XY axes of the controller, ret: int as a 4 bit val:
    # BIT:      |3  |2  |1  |0  |   0101
    # SWITCH:   |Y- |Y+ |X- |X+ |
    STAGE_GET_LIMITS = "controller.stage.limits.get"

    # Description:
    # gets the max speed during the movement from point to point as an integer
    # Result: An integer representing the speed in microns/s
    STAGE_GET_SPEED = "controller.stage.speed.get"

    # Description:
    # sets the max speed during the movement from point to point as integer in microns/s
    # Result: 0
    # Params: {max_speed}
    STAGE_SET_SPEED = "controller.stage.speed.set {}"

    # Description:
    # gets the max acc during the movement from point to point
    # Result: An integer representing the acceleration in microns/s/s
    STAGE_GET_ACC = "controller.stage.acceleration.get"

    # Descritpion:
    # Sets the maximum acceleration during a point to point move or velocity move
    # Result: 0
    # Params: {maxacc}
    STAGE_SET_ACC = "controller.stage.acceleration.set {}"

    # Description:
    # Gets the jerk time during a point to point move
    # Result: An integer representing the time in milliseconds before constant acceleration phase.
    STAGE_GET_JERK = "controller.stage.jerk.get"

    # Description:
    # Sets the jerk time during a point to point move
    # Result: "0"
    # Params: {time}
    STAGE_SET_JERK = "controller.stage.jerk.set {}"  # time - jerk time in milliseconds

    # Description:
    # Disables the joystick
    # Result: "0"
    DISABLE_JOYSTICK = "controller.stage.joyxyz.off"

    # Description:
    # Enables the joystick.
    # Result: "0"
    ENABLE_JOYSTICK = "controller.stage.joyxyz.on"

    # Description: Gets the current user unit step size. By default, the DLL works in user units of whole microns.
    # This value represents the number of micro-steps per micron.
    # This value varies depending on motor type and stage construction.
    # For example, a H101A stage has a 200-step motor and 2mm pitch lead screw.
    # Prior controllers micro-step at 250 steps/full step therefore there are 50000 micro-steps/rev of the motor.
    # 2mm / 50000 = 0.04microns. So theoretically setting SS to 1 results in user unit of 0.04microns,
    # or multiples thereof. In practice, this may not be physically possible due to motor behaviour
    # and mechanical limitations. See also controller.stage.steps-per-micron.get
    # Result: Typical responses for a stepper stage are “25”, “50” and “100”.
    # For a linear stage fitted with typical 50nm encoders the response will be “20”
    STAGE_GET_STEP_SIZE = "controller.stage.ss.get"

    # Description: Sets the current user unit step size.
    # Note: changing this value will reset controller.stage.hostdirection.set to default value of 1
    # Result: "0"
    # Params: {step_size}
    STAGE_SET_STEP_SIZE = "controller.stage.ss.set {}"

    # Description:
    # Get stage X encoder fitted status
    # Result: "0" or "1"
    GET_ENCODER_X_FITTED = "controller.stage.encoder.x.fitted.get"

    # Description:
    # Get stage Y encoder fitted status
    # Result: "0" or "1"
    GET_ENCODER_Y_FITTED = "controller.stage.encoder.y.fitted.get"

    # Description:
    # Returns the current tll input state
    # Result: Integer representing the binary pin state of available TTL inputs TTLIN3..0
    GET_TTL_INPUT_STATE = "controller.ttl.in.get"

    # Description
    # Returns the current tll output state
    # Result: Integer representing the binary pin state of available TTL outputs TTLOUT3..0
    GET_TTL_OUTPUT_STATE = "controller.ttl.out.get"

    # Description:
    # Sets the output TTL
    # Params: dec representation of binary output state -> 0-15
    # Result: "0"
    SET_TTL_OUTPUT_STATE = "controller.ttl.out.set {}"


    def __init__(self, command: str):
        self.__command = command

    @property
    def command(self) -> str:
        return self.__command

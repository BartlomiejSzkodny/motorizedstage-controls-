# motorizedstage-controls-
This project was created to help our team with laser fabrication of microfluidic chips.

### Files structure and where to look for what:\
DAO(folder) - DATA ACCESS OBJECT\
|- x64(folder) - files needed for the stage to move\
|yaml(folder) - files that defy the x64 library\
| | config.yaml - some values for the gui\
| | yaml_manager.py - functions that return those values\
|prior_connector.py - file with functions to connect to the stage and execute commands\
| stage_commands.py - predefined simple commands\
| stage_dao.py - commands for use\
errors(folder)\
| error_codes.py - all codes for all errors\
| errors.py - no idea whats that\
| service_errors.py - errors for stage commands\
factories(folder)\
| commands_factory.py - this commands are used in stage_dao.py file\
models(folder)\
| stage_models.py -these are used for errors and signals\
laserStageControll.py - file that connects CLI and the instructions for the stage\
stage.py - commands for the stage\
stageCLI - CLI controling the commands of the user\







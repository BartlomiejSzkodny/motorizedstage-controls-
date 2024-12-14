import yaml




class YamlData:
    def __init__(self, filename='programFiles/DAOs/yaml/config.yaml'):
        print("YamlData initialized")
        self.filename = filename
        print("YamlData file opened")
        with open(filename) as f:  
            self.data = yaml.safe_load(f)
            f.close()

    def save_data(self, stage_port: str, laser_port: str):
        self.data["ports_params"]["stage"] = stage_port
        self.data["ports_params"]["laser"] = laser_port

        with open(self.filename, 'w') as f:
            yaml.dump(self.data, f)

    def get_stage_ddl_path(self) -> str:
        return self.data["stage_params"]['path']

    def get_stage_com_port(self) -> int:
        return self.data["stage_params"]['COM']

    def get_default_com_ports(self) -> dict:
        return {"stage": self.data["ports_params"]["stage"], "laser": self.data["ports_params"]["laser"]}

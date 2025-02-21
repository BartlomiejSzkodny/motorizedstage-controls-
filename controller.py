from ctypes import WinDLL
from ctypes import create_string_buffer
import os
import sys
class PriorController:
    def __init__(self,port):
        self.connected =False
        self.port = -1
        self.initialisation(port)



    def initialisation(self,port):
                path = "app/PriorSDK1.9.2/PriorSDK 1.9.2/PriorSDK 1.9.2/x64/PriorScientificSDK.dll"
                self.port = port
                if(not self.connected):

                    if os.path.exists(path):
                        self.SDKPrior = WinDLL(path)
                    else:
                        raise RuntimeError("DLL could not be loaded.")

                    self.rx = create_string_buffer(1000)

                    ret = self.SDKPrior.PriorScientificSDK_Initialise()
                    if ret:
                        print(f"Error initialising {ret}")
                        sys.exit()
                    else:
                        print(f"Ok initialising {ret}")
                        self.connected = True


                    ret = self.SDKPrior.PriorScientificSDK_Version(self.rx)
                    print(f"dll version api ret={ret}, version={self.rx.value.decode()}")


                    self.sessionID = self.SDKPrior.PriorScientificSDK_OpenNewSession()
                    if self.sessionID < 0:
                        print(f"Error getting sessionID {ret}")
                    else:
                        print(f"SessionID = {self.sessionID}")


                    ret = self.SDKPrior.PriorScientificSDK_cmd(
                        self.sessionID, create_string_buffer(b"dll.apitest 33 goodresponse"), self.rx
                    )
                    print(f"api response {ret}, rx = {self.rx.value.decode()}")



                    ret = self.SDKPrior.PriorScientificSDK_cmd(
                        self.sessionID, create_string_buffer(b"dll.apitest -300 stillgoodresponse"), self.rx
                    )
                    print(f"api response {ret}, rx = {self.rx.value.decode()}")
                    ret =self.cmd(f"controller.connect {port}")
                    print(f"api response {ret}, rx = {self.rx.value.decode()}")

    def cmd(self, msg):
        rx = create_string_buffer(1000)
        ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(msg.encode()), rx
        )
        # if ret:
        #     print(f"Api error {ret}")
        # else:
        #     print(f"OK {rx.value.decode()}")

        return ret, rx.value.decode()
    
    
    
    def start_laser(self, power):
        self.cmd(f"controller.ttl.out.set {power}")#TODO check ttl
    
    def stop_laser(self):
        self.cmd("controller.ttl.out.set 0")

    def velocitymove(self, x, y):
        msg = f"controller.stage.move-at-velocity {x} {y}"
        self.cmd(msg)
    
    def move_to_position(self, x, y):
        msg = f"controller.stage.goto-position {int(x)} {int(y)}"
        self.cmd(msg)
        pass
    
    def get_position(self):
        return self.cmd("controller.stage.position.get")
    
    def is_moving(self):
        return self.cmd("controller.stage.busy.get")

    def set_max_speed(self,speed):
        msg = f"controller.stage.speed.set {speed}"
        self.cmd(msg)

from ctypes import WinDLL
from ctypes import create_string_buffer
import os
import sys
class PriorController:
    def initialisation(self):
        path = "app/PriorSDK1.9.2/PriorSDK 1.9.2/PriorSDK 1.9.2/x64/PriorScientificSDK.dll"


        if os.path.exists(path):
            self.SDKPrior = WinDLL(path)
        else:
            raise RuntimeError("DLL could not be loaded.")

        rx = create_string_buffer(1000)

        ret = self.SDKPrior.PriorScientificSDK_Version(rx)
        print(f"dll version api ret={ret}, version={rx.value.decode()}")


        self.sessionID = self.SDKPrior.PriorScientificSDK_OpenNewSession()
        if self.sessionID < 0:
            print(f"Error getting sessionID {ret}")
        else:
            print(f"SessionID = {self.sessionID}")


        ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(b"dll.apitest 33 goodresponse"), rx
        )
        print(f"api response {ret}, rx = {rx.value.decode()}")
        input("Press ENTER to continue...")


        ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(b"dll.apitest -300 stillgoodresponse"), rx
        )
        print(f"api response {ret}, rx = {rx.value.decode()}")
        input("Press ENTER to continue...")

    def cmd(self, msg):
        rx = create_string_buffer(1000)
        print(msg)
        ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(msg.encode()), rx
        )
        if ret:
            print(f"Api error {ret}")
        else:
            print(f"OK {rx.value.decode()}")

        return ret, rx.value.decode()


    def connect(self, port):
        try:
            result = self.cmd(self,f"controller.connect 4")
            #if result == 0:
            print(f"result---->{result}")
            self.connected = True
            print("Connected successfully")
        except:
            raise ConnectionError("Failed to connect")  
    
    
    
    def start_laser(self):
        pass #todo
    
    def stop_laser(self):
        pass #todo

    def velocitymove(self, x, y):
        msg = f"controller.stage.move-at-velocity {x} {y}"
        self.cmd(self, msg)
    
    def move_to_position(self, x, y):
        msg = f"controller.stage.goto-position {x} {y}"
        self.cmd(self, msg)
        pass
    
    def get_position(self):
        self.cmd(self,"controller.stage.position.get")
        pass
    
    def is_moving(self):
        pass #todo

#from ctypes import WinDLL,
from ctypes import create_string_buffer
import os
import sys
class PriorController:
    def __init__(self):
        path = "PriorScientificSDK.dll"
        #path to the dll
        if os.path.exists(path):
            self.SDKPrior = WinDLL(path)
        else:
            raise RuntimeError("DLL could not be loaded.")
        #create a buffer to store the response
        rx = create_string_buffer(1000)
        realhw = False
        ret = self.SDKPrior.PriorScientificSDK_Initialise()
        #send the command to the dll to initialise, if it returns 0 then it was successful
        if ret:
            print(f"Error initialising {ret}")
            sys.exit()
        else:
            print(f"Ok initialising {ret}")

        #get the version of the dll
        ret = self.SDKPrior.PriorScientificSDK_Version(rx)
        print(f"dll version api ret={ret}, version={rx.value.decode()}")

        #get id of the device
        self.sessionID = self.SDKPrior.PriorScientificSDK_OpenNewSession()
        if self.sessionID < 0:
            print(f"Error getting sessionID {ret}")
        else:
            print(f"SessionID = {self.sessionID}")

        #send a command to the dll, the response will be stored in the rx buffer
        ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(b"dll.apitest 33 goodresponse"), rx
        )
        print(f"api response {ret}, rx = {rx.value.decode()}")

        #send a command to the dll, the response will be stored in the rx buffer
        ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(b"dll.apitest -300 stillgoodresponse"), rx
        )
        print(f"api response {ret}, rx = {rx.value.decode()}")

    def connect(self, port):
        result = self.dll.PriorScientificSDK_cmd(self.sessionID, create_string_buffer(f"COM{port}"), create_string_buffer(256))
        if result == 0:
            self.connected = True
            print("Connected successfully")
        else:
            raise ConnectionError("Failed to connect")
        
    def cmd(self,msg):
        rx = create_string_buffer(1000)
        print(msg)
        ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(msg.encode()), rx
        )
        if ret:
            print(f"Api error {ret}")
        else:
            print(f"OK {rx.value.decode()}")

        input("Press ENTER to continue...")
        return ret, rx.value.decode()
        
        

    
    
    
    
    def start_laser(self):
        pass #todo
    
    def stop_laser(self):
        pass #todo
    
    def move_to_position(self, x, y):
        msg = f"controller.stage.goto-position {x} {y}"
        self.cmd(msg)
        pass
    
    def get_position(self):
        #print(self.cmd("controller.stage.position.get"))
        pass
    
    def is_moving(self):
        pass #todo

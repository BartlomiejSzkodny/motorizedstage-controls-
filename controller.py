#from ctypes import WinDLL,
from ctypes import create_string_buffer
import os
import sys
class PriorController:
    def __init__(self, dll_path):
        path = "PriorScientificSDK.dll"

        if os.path.exists(path):
            SDKPrior = WinDLL(path)
        else:
            raise RuntimeError("DLL could not be loaded.")

        rx = create_string_buffer(1000)
        realhw = False
        ret = SDKPrior.PriorScientificSDK_Initialise()
        if ret:
            print(f"Error initialising {ret}")
            sys.exit()
        else:
            print(f"Ok initialising {ret}")


        ret = SDKPrior.PriorScientificSDK_Version(rx)
        print(f"dll version api ret={ret}, version={rx.value.decode()}")


        sessionID = SDKPrior.PriorScientificSDK_OpenNewSession()
        if sessionID < 0:
            print(f"Error getting sessionID {ret}")
        else:
            print(f"SessionID = {sessionID}")


        ret = SDKPrior.PriorScientificSDK_cmd(
            sessionID, create_string_buffer(b"dll.apitest 33 goodresponse"), rx
        )
        print(f"api response {ret}, rx = {rx.value.decode()}")
        input("Press ENTER to continue...")


        ret = SDKPrior.PriorScientificSDK_cmd(
            sessionID, create_string_buffer(b"dll.apitest -300 stillgoodresponse"), rx
        )
        print(f"api response {ret}, rx = {rx.value.decode()}")
        input("Press ENTER to continue...")

    def connect(self, port):
        result = self.dll.PriorScientificSDK_cmd(self.sessionID, create_string_buffer(f"COM{port}"), create_string_buffer(256))
        if result == 0:
            self.connected = True
            print("Connected successfully")
        else:
            raise ConnectionError("Failed to connect")
        
        

    def disconnect(self):
        if not self.connected:
            print("Not connected")
            return
        result = self.dll.Disconnect()
        if result == 0:
            self.connected = False
            print("Disconnected successfully")
        else:
            raise ConnectionError("Failed to disconnect")

    def send_command(self, command):
        if not self.connected:
            raise ConnectionError("Not connected")
        buffer = create_string_buffer(256)
        result = self.dll.SendCommand(command.encode('utf-8'), buffer)
        if result == 0:
            return buffer.value.decode('utf-8')
        else:
            raise RuntimeError("Failed to send command")
    
    def list_ports(self):
        buffer = create_string_buffer(256)
        result = self.dll.ListPorts(buffer)
        if result == 0:
            return buffer.value.decode('utf-8').split(',')
        else:
            raise RuntimeError("Failed to list ports")
    
    def start_laser(self):
        if not self.connected:
            raise ConnectionError("Not connected")
        result = self.dll.StartLaser()
        if result != 0:
            raise RuntimeError("Failed to start laser")
    
    def stop_laser(self):
        if not self.connected:
            raise ConnectionError("Not connected")
        result = self.dll.StopLaser()
        if result != 0:
            raise RuntimeError("Failed to stop laser")
    
    def move_to_position(self, x, y):
        if not self.connected:
            raise ConnectionError("Not connected")
        result = self.dll.MoveToPosition(x, y)
        if result != 0:
            raise RuntimeError("Failed to move to position")
    
    def get_position(self):
        if not self.connected:
            raise ConnectionError("Not connected")
        x = create_string_buffer(256)
        y = create_string_buffer(256)
        result = self.dll.GetPosition(x, y)
        if result == 0:
            return x.value.decode('utf-8'), y.value.decode('utf-8')
        else:
            raise RuntimeError("Failed to get position")
    
    def is_moving(self):
        if not self.connected:
            raise ConnectionError("Not connected")
        result = self.dll.IsMoving()
        return result == 1

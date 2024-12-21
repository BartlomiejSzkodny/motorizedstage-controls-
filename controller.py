from ctypes import WinDLL, create_string_buffer
import os
import sys
class PriorController:
    def __init__(self, dll_path):
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"Cannot find DLL at {dll_path}")
        self.dll = WinDLL(dll_path)
        self.connected = False

    def connect(self, port):
        if self.connected:
            print("Already connected")
            return
        result = self.dll.Connect(port.encode('utf-8'))
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

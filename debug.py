import os
import sys
from ctypes import WinDLL, create_string_buffer
import time

class debug:
            def run(self):
                while True:
                    command = input("Enter command (help/vmove/move/get/exit/connect): ").strip().lower()
                    if command == "help":
                        print("vmove - Move at a specified velocity")
                        print("move - Move to a specified position")
                        print("get - Get the current position")
                        print("connect - Connect to the stage")
                        print("exit - Exit the program")
                    elif command == "move":
                        coordinates = input("Enter coordinates (x,y): ").split(",")
                        self.move(coordinates)
                    elif command == "set":
                        coordinates = input("Enter coordinates (x,y): ").split(",")
                        self.set_position(coordinates[0],coordinates[1])
                    elif command == "get":
                        self.get_position()
                    elif command == "connect":
                        self.connect()
                    elif command == "vmove":
                        velocity = input("Enter velocity(x,y): ").split(",")
                        self.move_at_velocity(velocity[0],velocity[1])
                    elif command == "test":
                        self.cmd(f"controller.stage.move-at-velocity 100 100")
                        time.sleep(20)
                        self.cmd(f"controller.stage.move-at-velocity 0 0")
                        self.cmd(f"controller.stage.move-at-velocity -100 0")
                        time.sleep(20)
                        self.cmd(f"controller.stage.move-at-velocity 0 0")
                        self.cmd(f"controller.stage.move-at-velocity 100 -100")
                        time.sleep(20)
                        self.cmd(f"controller.stage.move-at-velocity 0 0")
                        self.cmd(f"controller.stage.move-at-velocity 400 -100")
                        time.sleep(20)
                        self.cmd(f"controller.stage.move-at-velocity 0 0")
                        self.cmd(f"controller.stage.move-at-velocity 100 100")
                        time.sleep(20)
                        self.cmd(f"controller.stage.move-at-velocity 0 0")
                        self.cmd(f"controller.stage.move-at-velocity 0 -100")
                        time.sleep(20)
                        self.cmd(f"controller.stage.move-at-velocity 0 0")
                        self.cmd(f"controller.stage.move-at-velocity 100 100")
                        time.sleep(20)
                        self.cmd(f"controller.stage.move-at-velocity 0 0")


                    elif command == "exit":
                        print("Exiting...")
                        break
                    else:
                        print("Invalid command")

            def move(self, direction):
                # Implement the logic to move in the specified direction
                self.cmd(f"controller.stage.goto-position {direction[0]} {direction[1]} ")
                

                print(f"Moving {direction}")

            def get_position(self):
                # Implement the logic to get the current position
                ret =self.cmd("controller.stage.position.get")
                print(f"Getting current position{ret}")
            
            def move_at_velocity(self, velocityx,velocityy):
                self.cmd(f"controller.stage.move-at-velocity {velocityx} {velocityy}")
                time.sleep(20)
            
            def set_position(self, x,y):
                self.cmd(f"controller.stage.position.set {x} {y}")

            

            
            def connect(self):
                path = "app/PriorSDK1.9.2/PriorSDK 1.9.2/PriorSDK 1.9.2/x64/PriorScientificSDK.dll"

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
                port = input("Enter port: ")
                ret =self.cmd(f"controller.connect {port}")
                print(f"api response {ret}, rx = {self.rx.value.decode()}")
            
            def cmd(self,msg):
                print(msg)
                ret = self.SDKPrior.PriorScientificSDK_cmd(
                    self.sessionID, create_string_buffer(msg.encode()), self.rx
                )
                if ret:
                    print(f"Api error {ret}")
                else:
                    print(f"OK {self.rx.value.decode()}")
                return ret, self.rx.value.decode()
            
            
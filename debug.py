import os
import sys
from ctypes import WinDLL, create_string_buffer
from controller import PriorController as prior
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
                        print("test - Test the stage")
                        print("ttl - Set the ttl")
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
                    elif command == "getvel":
                        vel = self.cmd("controller.stage.speed.get")
                        print(vel)
                    elif command == "ttl":
                        num = input("Enter 15 to 0: ")
                        self.cmd(f"controller.ttl.out.set {num}")
                    elif command == "testplamka":
                        current = self.cmd("controller.stage.position.get")[1].split(',')
                        current = [int(current[0]),int(current[1])]
                        print(current)
                        self.cmd(f"controller.stage.speed.set 1000")
                        time.sleep(0.3)
                        #make rectangle where the test will be performed
                        self.cmd(f"controller.ttl.out.set 15")
                        time.sleep(1)
                        self.cmd(f"controller.stage.goto-position {current[0]-1000} {current[1]-1000}")
                        time.sleep(10)
                        self.cmd(f"controller.stage.goto-position {current[0]+5*1000+1000} {current[1]-1000}")
                        time.sleep(10)
                        self.cmd(f"controller.stage.goto-position {current[0]+5*1000+1000} {current[1]+10*1000+1000}")
                        time.sleep(10)
                        self.cmd(f"controller.stage.goto-position {current[0]-1000} {current[1]+10*1000+1000}")
                        time.sleep(10)
                        self.cmd(f"controller.stage.goto-position {current[0]-1000} {current[1]-1000}")
                        time.sleep(10)
                        self.cmd(f"controller.ttl.out.set 0")
                        time.sleep(10)
                        c = input("is it okey? (y/n): ")
                        if c == "y":
                            pass
                        else:
                            print("Exiting...")
                            break
                        

                        for x,czas in enumerate([0.1,0.2,0.3,0.4,0.5]):
                            for y,moc in enumerate( [6,7,8,9,10,11,12,13,14,15]):
                                self.set_position(current[0]+int(x*1000),current[1]+int(y*1000))
                                time.sleep(5)
                                self.cmd(f"controller.ttl.out.set {moc}")
                                time.sleep(czas)
                                self.cmd(f"controller.ttl.out.set 0")
                                time.sleep(1)
                                print(f"czas: {czas}, moc: {moc}")
                                print(f"x: {x}, y: {y}")
                    
                    elif command == "testlinia":
                        current = self.cmd("controller.stage.position.get")[1].split(',')
                        current = [int(current[0]), int(current[1])]
                        print(current)
                        time.sleep(0.3)
                        self.cmd(f"controller.ttl.out.set 1")
                        self.cmd(f"controller.stage.goto-position {current[0] - 1000} {current[1] - 1000}")
                        time.sleep(3)
                        self.cmd(f"controller.stage.goto-position {current[0] - 1000} {current[1] + 4000 + 1000}")
                        time.sleep(10)
                        self.cmd(f"controller.stage.goto-position {current[0] + 30000 + 1000} {current[1] + 4000 + 1000}")
                        time.sleep(46)
                        self.cmd(f"controller.stage.goto-position {current[0] + 30000 + 1000} {current[1] - 1000}")
                        time.sleep(10)
                        self.cmd(f"controller.stage.goto-position {current[0] - 1000} {current[1] - 1000}")
                        time.sleep(46)
                        self.cmd(f"controller.ttl.out.set 0")
                        c = input("is it okey? (y/n): ")
                        if c == "y":
                            pass
                        else:
                            print("Exiting...")
                            break
                        i = 0
                        for moc in [1,2,3,4,5,6,7,8]:
                            for velocity in [1500,2000,2500,3000,3500,4000,4500,5000]:
                                self.set_position(current[0] + i * 300, current[1])
                                time.sleep(5)
                                self.cmd(f"controller.stage.speed.set {velocity}")
                                time.sleep(5)
                                self.cmd(f"controller.ttl.out.set {moc}")
                                self.cmd(f"controller.stage.goto-position {current[0] + i * 300} {current[1] + 4000}")
                                time.sleep(4000/velocity)
                                self.cmd(f"controller.ttl.out.set 0")
                                time.sleep(1)
                                print(f"100+{i * 250}, 100")
                                i += 1
                            i+=3
                    elif command == "testpolilinia":
                        current = self.cmd("controller.stage.position.get")[1].split(',')
                        current = [int(current[0]), int(current[1])]

                        for i in range(20):
                            input("Press enter to continue")
                            self.set_position(current[0] + i * 1000, current[1])
                            time.sleep(5)
                            self.cmd(f"controller.ttl.out.set 1")
                            time.sleep(1)
                            self.cmd(f"controller.stage.goto-position {current[0] + i * 1000} {current[1] + 5000}")
                            time.sleep(5)
                            self.set_position(current[0] + i * 1000, current[1])
                            time.sleep(5)
                            self.cmd(f"controller.stage.goto-position {current[0] + i * 1000} {current[1] + 5000}")
                            time.sleep(5)
                            self.set_position(current[0] + i * 1000, current[1])
                            time.sleep(5)

                            self.cmd(f"controller.ttl.out.set 0")
                            time.sleep(1)



                        
                                


                                








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
                self.cmd(f"controller.stage.goto-position {x} {y}")

            

            
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
            
            
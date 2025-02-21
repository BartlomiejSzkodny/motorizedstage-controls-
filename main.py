import tkinter as tk
from stlapp import STLApp
from debug import debug

if __name__ == "__main__":
# Run the app
        # root = tk.Tk()
        # app = STLApp(root)
        # root.mainloop()
        # d = debug()
        # d.run()
        c = input("Enter command (app/debug): ").strip().lower()
        if c == "app":
            root = tk.Tk()
            app = STLApp(root)
            root.mainloop()
        elif c == "debug":
            d = debug()
            d.run()
        else:
            print("Invalid command")

        
#todo test seting the starting point
#test ttl
#if it will be posible run weronikas stl file
#add inversion
#skalowanie nie działa


import tkinter as tk
from stlapp import STLApp
from debug import debug

if __name__ == "__main__":
# Run the app
    c = input("Do you want to run the app(a) or the terminal(t)? ").strip().lower()
    if c.lower() == "a":
        root = tk.Tk()
        app = STLApp(root)
        root.mainloop()
    elif c.lower() == "t":
        d = debug()
        d.run()
    else:
        print("Invalid input")
        exit(1)
        
#todo test seting the starting point
#test ttl
#if it will be posible run weronikas stl file


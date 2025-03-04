import tkinter as tk
from tkinter import filedialog, messagebox
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial.tools.list_ports
from controller import PriorController as prior
import time

"""_summary_ = This class is used to create a GUI for slicing 3D STL files and simulating a laser engraving process.
The user can load an STL file, slice it into layers, select layers for processing, and simulate a laser engraving process
on the selected layers. The user can also select the line spacing for the laser engraving process and connect to a Prior
controller to control the laser engraving process. The user can also select the ports for the Prior controller and start
the laser engraving process. The user can also set the x and y starting position for the laser engraving process.

"""
class STLApp:
    def __init__(self, root):
        # positions = [
        #     (100, 100, True),
        #     (200, 200, True),
        #     (300, 300, False),  # No line drawn here
        #     (250, 150, True),
        #     (50, 50, True)
        # ]
        
        # # Start the Java process
        # process = subprocess.Popen(["java", "-jar", "LaserVisualizer.jar"], stdin=subprocess.PIPE, text=True)

        # for x, y, draw in positions:
        #     process.stdin.write(f"{x},{y},{draw}\n")  # Send position and draw flag
        #     process.stdin.flush()  # Ensure immediate update
        #     time.sleep(1)  # Simulate movement delay
       


        self.prior = None
        self.root = root
        self.root.title("3D STL Slicer")
        self.mesh_oryginal = None
        self.mesh_copy = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.sections = []
        self.prior_connected = False

        self.move_on_outline = False
        self.plot_interiors_only = True  # Add a boolean variable to control plotting
        self.lines_normal = False
        
        self.padding = 0.5  # Padding for the laser 
    
        # Start x,y position
        self.x = 0
        self.y = 0

        # File Selection
        self.file_label = tk.Label(root, text="No file selected", width=50)
        self.file_label.grid(row=0, column=0, padx=10, pady=10)
        self.file_button = tk.Button(root, text="Load STL File", command=self.load_file)
        self.file_button.grid(row=0, column=1, padx=10, pady=10)

        # Slicing Parameters
        tk.Label(root, text="Layer Thickness (mm):").grid(row=1, column=0, padx=10, pady=10)
        self.layer_thickness_var = tk.DoubleVar(value=1.0)
        self.layer_entry = tk.Entry(root, textvariable=self.layer_thickness_var, width=10)
        self.layer_entry.grid(row=1, column=1, padx=10, pady=10)

        # Line Spacing
        tk.Label(root, text="Line Spacing (mm):").grid(row=1, column=2, padx=10, pady=10)
        self.line_spacing_var = tk.DoubleVar(value=0.5)
        self.line_spacing_entry = tk.Entry(root, textvariable=self.line_spacing_var, width=10)
        self.line_spacing_entry.grid(row=1, column=3, padx=10, pady=10)

        # Scale of the layer
        tk.Label(root, text="Scale of the layer:").grid(row=2, column=0, padx=10, pady=10)
        self.scale_var = tk.DoubleVar(value=1.0)
        self.scale_entry = tk.Entry(root, textvariable=self.scale_var, width=10)
        self.scale_entry.grid(row=2, column=1, padx=10, pady=10)

        # Velocity selection
        tk.Label(root, text="Velocity (um/s):").grid(row=2, column=2, padx=10, pady=10)
        self.velocity_var = tk.DoubleVar(value=10)
        self.velocity_entry = tk.Entry(root, textvariable=self.velocity_var, width=10)
        self.velocity_entry.grid(row=2, column=3, padx=10, pady=10)

        # Slice Button
        self.slice_button = tk.Button(root, text="Slice STL", command=self.slice_stl)
        self.slice_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Simulation Options
        tk.Label(root, text="Simulation Options:").grid(row=3, column=2, padx=10, pady=10)
        self.simulation_listbox = tk.Listbox(root, height=4)
        self.simulation_listbox.grid(row=3, column=3, padx=10, pady=10)
        self.simulation_listbox.bind('<<ListboxSelect>>', self.on_simulation_select)
        self.simulation_listbox.insert(tk.END, "Normal")
        self.simulation_listbox.insert(tk.END, "Inverse")
        self.simulation_listbox.insert(tk.END, "lines inverse")
        self.simulation_listbox.insert(tk.END, "lines normal")

        # Output
        self.output_frame = tk.Frame(root)
        self.output_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.output_frame)
        self.canvas.get_tk_widget().pack()

        # Layer Selection
        tk.Label(root, text="Select Layer:").grid(row=5, column=0, padx=10, pady=10)
        self.layer_listbox = tk.Listbox(root, height=10)
        self.layer_listbox.grid(row=6, column=0, padx=10, pady=10)
        self.layer_listbox.bind('<<ListboxSelect>>', self.display_layer)

        # Layer Selection for Processing
        tk.Label(root, text="Select Layers for Processing:").grid(row=5, column=1, padx=10, pady=10)
        self.layer_selection_listbox = tk.Listbox(root, selectmode=tk.EXTENDED, height=10)
        self.layer_selection_listbox.grid(row=6, column=1, padx=10, pady=10)

        # Select Ports
        tk.Label(root, text="Select Ports:").grid(row=5, column=2, padx=10, pady=10)
        self.select_ports_button = tk.Listbox(root, height=10)
        self.select_ports_button.grid(row=6, column=2, padx=10, pady=10)
        self.select_ports_button.bind('<<ListboxSelect>>', self.connectPrior)

        # Refresh ports button
        self.refresh_ports_button = tk.Button(root, text="Refresh Ports", command=self.refresh_ports)
        self.refresh_ports_button.grid(row=7, column=2, padx=10, pady=10)

        # Laser start button
        self.laser_start_button = tk.Button(root, text="Start Laser", command=self.start_laser)
        self.laser_start_button.grid(row=7, column=0, padx=10, pady=10)

        # Show Max and Min button
        self.show_max_min_button = tk.Button(root, text="Show Max and Min", command=self.show_max_min)
        self.show_max_min_button.grid(row=7, column=1, padx=10, pady=10)

        # Set the x and y start position
        self.xy_entry = tk.Button(root, text="Set X,Y Starting", command=self.set_xy)
        self.xy_entry.grid(row=8, column=0, columnspan=2, pady=10)

        
        
    

        

        

        









        
        """_summary_ = This function is used to load an STL file and display a message box if the file is loaded successfully
        or if there is an error loading the file.
        """
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("STL Files", "*.stl")])
        if file_path:
            self.file_label.config(text=file_path)
            try:
                self.mesh_oryginal = trimesh.load(file_path)
                if self.mesh_oryginal.is_watertight:
                    messagebox.showinfo("Success", "STL file loaded successfully!")
                else:
                    messagebox.showwarning("Warning", "STL file is not watertight!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load STL file: {e}")

        """_summary_ = This function is used to slice the loaded STL file into layers based on the user-specified layer thickness.
        """
    def slice_stl(self):
        if not self.mesh_oryginal:
            messagebox.showerror("Error", "No STL file loaded!")
            return
        self.mesh_copy = self.mesh_oryginal
        layer_thickness = self.layer_thickness_var.get()
        z_min, z_max = self.mesh_copy.bounds[0][2], self.mesh_copy.bounds[1][2]
        z_levels = np.arange(z_min, z_max, layer_thickness)

        

        try:
            self.sections = self.mesh_copy.section_multiplane(
                plane_origin=[0, 0, 0],
                plane_normal=[0, 0, 1],
                heights=z_levels
            )

            # Update layer listbox
            self.layer_listbox.delete(0, tk.END)
            self.layer_selection_listbox.delete(0, tk.END)
            for i in range(len(self.sections)):
                self.layer_listbox.insert(tk.END, f"Layer {i}")
                self.layer_selection_listbox.insert(tk.END, f"Layer {i}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to slice STL file: {e}")

    def on_simulation_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            if index == 0:
                self.move_on_outline = False
                self.plot_interiors_only = False
                self.lines_normal = False
            elif index == 1:
                self.move_on_outline = True
                self.plot_interiors_only = False
                self.lines_normal = False
            elif index == 2:
                self.move_on_outline = False
                self.plot_interiors_only = True
                self.lines_normal = False
            elif index == 3:
                self.move_on_outline = False
                self.plot_interiors_only = False
                self.lines_normal = True
            self.display_layer(event)

        """_summary_ = This function is used to display the selected layer in the output frame.
        """
    def display_layer(self, event):
        print("Displaying layer")
        self.ax.clear()
        all_x, all_y = [], []
        scale = self.scale_var.get()
        self.ax.set_aspect('equal', adjustable='box')
        for section in self.sections:
            if section is not None:
                for polygon in section.polygons_full:
                    x, y = polygon.exterior.xy
                    x = [coord*scale for coord in x]
                    y = [coord*scale for coord in y]
                    all_x.extend(x)
                    all_y.extend(y)
        self.ax.set_xlim(min(all_x)-self.padding, max(all_x)+self.padding)
        self.ax.set_ylim(min(all_y)-self.padding, max(all_y)+self.padding)
        
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            if index < len(self.sections):
                section = self.sections[index]

            if section is not None:
                polygons = section.polygons_full
                scale = self.scale_var.get()
                if self.move_on_outline:
                    self.ax.clear()
                    for polygon in polygons:
                        for interior in polygon.interiors:
                            ix, iy = interior.xy
                            ix = [coord*scale for coord in ix]
                            iy = [coord*scale for coord in iy]
                            self.ax.plot(ix, iy, 'r--')  # Plot inner boundaries with dashed lines
                elif self.plot_interiors_only:
                    self.ax.clear()
                    line_spacing = self.line_spacing_var.get()
                    for polygon in polygons:
                        for interior in polygon.interiors:
                            ix, iy = interior.xy
                            ix = [coord*scale for coord in ix]
                            iy = [coord*scale for coord in iy]
                            min_y, max_y = min(all_y), max(all_y)
                            y_lines = np.arange(min_y, max_y, line_spacing)  # Use user-specified line spacing
                            for y_line in y_lines:
                                intersections = []
                                for i in range(len(ix) - 1):
                                    dy = iy[i+1] - iy[i]
                                    if abs(dy) < 1e-9:
                                        continue
                                    if (iy[i] <= y_line <= iy[i+1]) or (iy[i+1] <= y_line <= iy[i]):
                                        x_intersect = ix[i] + (y_line - iy[i]) * (ix[i+1] - ix[i]) / dy
                                        intersections.append(x_intersect)
                                intersections.sort()
                                for i in range(0, len(intersections), 2):
                                    if i+1 < len(intersections):
                                        start_point = (intersections[i], y_line)
                                        end_point = (intersections[i+1], y_line)
                                        self.ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='red')
                elif self.lines_normal:
                    self.ax.clear()
                    min_x, max_x = min(all_x), max(all_x)
                    min_y, max_y = min(all_y), max(all_y)
                    line_spacing = self.line_spacing_var.get()
                    for polygon in polygons:
                        x, y = polygon.exterior.xy
                        x = [coord*scale for coord in x]
                        y = [coord*scale for coord in y]
                        y_lines = np.arange(min_y, max_y, line_spacing)
                        for y_line in y_lines:
                            intersections = []
                            for i in range(len(x) - 1):
                                dy = y[i+1] - y[i]
                                if abs(dy) < 1e-9:
                                    continue
                                if (y[i] <= y_line <= y[i+1]) or (y[i+1] <= y_line <= y[i]):
                                    x_intersect = x[i] + (y_line - y[i]) * (x[i+1] - x[i]) / dy
                                    intersections.append(x_intersect)
                            for interior in polygon.interiors:
                                ix, iy = interior.xy
                                ix = [coord*scale for coord in ix]
                                iy = [coord*scale for coord in iy]
                                for i in range(len(ix) - 1):
                                    dy = iy[i+1] - iy[i]
                                    if abs(dy) < 1e-9:
                                        continue
                                    if (iy[i] <= y_line <= iy[i+1]) or (iy[i+1] <= y_line <= iy[i]):
                                        x_intersect = ix[i] + (y_line - iy[i]) * (ix[i+1] - ix[i]) / dy
                                        intersections.append(x_intersect)
                            intersections.sort()
                            for i in range(0, len(intersections), 2):
                                if i+1 < len(intersections):
                                    start_point = (intersections[i], y_line)
                                    end_point = (intersections[i+1], y_line)
                                    self.ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='red')
                else:
                    
                    self.ax.clear()
                    for polygon in polygons:
                        x, y = polygon.exterior.xy
                        x = [coord*scale for coord in x]
                        y = [coord*scale for coord in y]
                        self.ax.plot(x, y)
                        for interior in polygon.interiors:
                            ix, iy = interior.xy
                            ix = [coord*scale for coord in ix]
                            iy = [coord*scale for coord in iy]
                            self.ax.plot(ix, iy, color='red')  # Plot inner boundaries with dashed lines
                    self.ax.set_title(f"Layer {index}: {len(polygons)} polygons")
            else:
                self.ax.set_title(f"Layer {index}: No intersection") 

            if index == 0 and section is not None:
                x, y = section.polygons_full[0].exterior.xy
                self.ax.plot(x[0]*scale, y[0]*scale, 'ro')
            
                self.canvas.draw()
            else:
                self.ax.set_title(f"Layer {index}: No intersection")
                
                self.canvas.draw()
    
    """_summary_ = This function is used to close the main window of the application.
    """
    def on_closing(self):
        self.root.quit()

    """_summary_ = This function is used to close the laser simulation window.
    """ 
    def on_closing_laser(self):
        self.laser_running = False
        self.laser_window.destroy()

    """_summary_ = This function is used to start the laser engraving process on the selected layers.
    """
    def start_laser(self):
        if not self.sections:
            messagebox.showerror("Error", "No layers to process!")
            return
        # if not self.prior_connected:
        #     messagebox.showerror("Error", "Prior controller not connected!")
        #     return

        selected_layers = [int(self.layer_selection_listbox.get(i).split()[1]) for i in self.layer_selection_listbox.curselection()]
        if not selected_layers:
            messagebox.showerror("Error", "No layers selected for processing!")
            return

        self.laser_window = tk.Toplevel(self.root)
        self.laser_window.title("Laser Simulation")
        self.laser_figure, self.laser_ax = plt.subplots()
        self.laser_canvas = FigureCanvasTkAgg(self.laser_figure, master=self.laser_window)
        self.laser_canvas.get_tk_widget().pack()
        self.laser_window.protocol("WM_DELETE_WINDOW", self.on_closing_laser)

        self.process_layers(selected_layers)

    """_summary_ = This function is used to process the selected layers for the laser engraving process.
    The laser engraving process is simulated by moving the laser from the start point to the end point of each line
    intersection with the selected layers.

    Args:
        selected_layers (list): A list of selected layers for the laser engraving process.
    """
    def process_layers(self, selected_layers):
        line_spacing = self.line_spacing_var.get()
        speed = self.velocity_var.get()
        
        # Calculate the bounds for all layers
        all_x, all_y = [], []
        scale = self.scale_var.get()
        for section in self.sections:
            if section is not None:
                for polygon in section.polygons_full:
                    x, y = polygon.exterior.xy
                    x = [coord*scale for coord in x]
                    y = [coord*scale for coord in y]
                    all_x.extend(x)
                    all_y.extend(y)
        
        if not all_x or not all_y:
            messagebox.showerror("Error", "No valid layers to process!")
            return
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        self.laser_running = True
        time.sleep(1)
        
        for layer_index in selected_layers:
            section = self.sections[layer_index]
            self.laser_ax.clear()
            if section is not None:
                polygons = section.polygons_full
            if self.move_on_outline:
                self.process_outline(polygons, scale, min_x, max_x, min_y, max_y, layer_index)
            elif self.plot_interiors_only:
                self.process_interiors(polygons, scale, min_x, max_x, min_y, max_y, layer_index, line_spacing, speed)
            elif self.lines_normal:
                self.process_lines(polygons, scale, min_x, max_x, min_y, max_y, layer_index, line_spacing, speed)
            else:
                self.process_default(polygons, scale, min_x, max_x, min_y, max_y, layer_index)
            self.laser_window.after(500)  # wait time before moving to the next layer
        self.laser_canvas.draw()
        self.laser_window.update()
        self.laser_window.after(500)  # wait time before moving to the next layer

    def process_outline(self, polygons, scale, min_x, max_x, min_y, max_y, layer_index):
            for polygon in polygons:
                for interior in polygon.interiors:
                    ix, iy = interior.xy
                    self.ax.plot(ix, iy, color='red')  # Plot inner boundaries with dashed lines
                    x1 = ix[0]
                    y1 = iy[0]
                    current = self.prior.get_position()[1].split(',')
                    distance = ((int(current[0]) - (x1 * scale + self.x)) ** 2 + (int(current[1]) - (y1 * scale + self.y)) ** 2) ** 0.5
                    self.prior.cmd("controller.stage.speed.set 1000")
                    self.prior.move_to_position(self.x + x1 * scale, self.y + y1 * scale)
                    time.sleep((distance / 1000 + 0.2))
                    for i in range(len(ix) - 1):
                        self.laser_ax.plot([ix[i] * scale, ix[i + 1] * scale], [iy[i] * scale, iy[i + 1] * scale], color='red')
                        self.laser_ax.set_title(f"Layer {layer_index}")
                        self.laser_ax.set_xlim(min_x - self.padding, max_x + self.padding)
                        self.laser_ax.set_ylim(min_y - self.padding, max_y + self.padding)
                        self.laser_ax.set_aspect('equal', adjustable='box')
                        xf, yf = self.prior.get_position()[1].split(',')
                        self.prior.start_laser()
                        time.sleep(0.3)
                        self.prior.move_to_position(self.x + ix[i] * scale, self.y + iy[i] * scale)
                        distance = ((int(xf) - (ix[i] * scale + self.x)) ** 2 + (int(yf) - (iy[i] * scale + self.y)) ** 2) ** 0.5
                        time.sleep((distance / 100))
                        self.prior.stop_laser()
                        time.sleep(0.3)
                        try:
                            self.laser_canvas.draw()
                            self.laser_window.update()
                        except tk.TclError:
                            return

    def process_interiors(self, polygons, scale, min_x, max_x, min_y, max_y, layer_index, line_spacing, speed):
            line_spacing = self.line_spacing_var.get()
            self.x, self.y = self.prior.get_position()[1].split(',')
            self.x = float(self.x)
            self.y = float(self.y)
            for polygon in polygons:
                        for interior in polygon.interiors:
                            ix, iy = interior.xy
                            ix = [coord * scale  for coord in ix]
                            iy = [coord * scale  for coord in iy]
                            y_lines = np.arange(min_y, max_y, line_spacing)  # Use user-specified line spacing
                            for y_line in y_lines:
                                intersections = []
                                for i in range(len(ix) - 1):
                                    dy = iy[i + 1] - iy[i]
                                    if abs(dy) < 1e-9:
                                        continue
                                    if (iy[i] <= y_line <= iy[i + 1]) or (iy[i + 1] <= y_line <= iy[i]):
                                        x_intersect = ix[i] + (y_line - iy[i]) * (ix[i + 1] - ix[i]) / dy
                                        intersections.append(x_intersect)
                                intersections.sort()
                                for i in range(0, len(intersections), 2):
                                    if i + 1 < len(intersections):
                                        start_point = (intersections[i], y_line)
                                        end_point = (intersections[i + 1], y_line)
                                        self.laser_ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='red')
                                        self.laser_ax.set_title(f"Layer {layer_index}")
                                        self.laser_ax.set_xlim(min_x - self.padding, max_x + self.padding)
                                        self.laser_ax.set_ylim(min_y - self.padding, max_y + self.padding)
                                        self.laser_ax.set_aspect('equal', adjustable='box')
                                        startx = float(self.prior.get_position()[1].split(',')[0])
                                        time.sleep(0.3)
                                        starty = float(self.prior.get_position()[1].split(',')[1])
                                        time.sleep(0.3)
                                        distance = ((float(startx) - (start_point[0] + float(self.x))) ** 2 + (float(starty) - (start_point[1] + float(self.y))) ** 2) ** 0.5
                                        self.prior.move_to_position(float(self.x) + start_point[0], float(self.y) + start_point[1])
                                        time.sleep(distance / speed)
                                        time.sleep(0.3)
                                        self.prior.start_laser(1)
                                        time.sleep(0.1)
                                        self.prior.move_to_position(float(self.x) + end_point[0], float(self.y) + end_point[1])
                                        distance = ((abs(end_point[0]) - abs(start_point[0])) ** 2 + (abs(end_point[1]) - abs(start_point[1])) ** 2) ** 0.5
                                        time.sleep(distance / speed)
                                        self.prior.stop_laser()
                                        time.sleep(0.3)
                                        try:
                                            self.laser_canvas.draw()
                                            self.laser_window.update()
                                        except tk.TclError:
                                            return

                                        

    def process_lines(self, polygons, scale, min_x, max_x, min_y, max_y, layer_index, line_spacing, speed):
            for polygon in polygons:
                x, y = polygon.exterior.xy
                y_lines = np.arange(min_y, max_y, line_spacing)
                for y_line in y_lines:
                    intersections = []
                    for i in range(len(x) - 1):
                        dy = y[i + 1] - y[i]
                        if abs(dy) < 1e-9:
                            continue
                        if (y[i] <= y_line <= y[i + 1]) or (y[i + 1] <= y_line <= y[i]):
                            x_intersect = x[i] + (y_line - y[i]) * (x[i + 1] - x[i]) / dy
                            intersections.append(x_intersect)
                        for interior in polygon.interiors:
                            ix, iy = interior.xy
                        ix = [coord * scale for coord in ix]
                        iy = [coord * scale for coord in iy]
                        for i in range(len(ix) - 1):
                            dy = iy[i + 1] - iy[i]
                            if abs(dy) < 1e-9:
                                continue
                            if (iy[i] <= y_line <= iy[i + 1]) or (iy[i + 1] <= y_line <= iy[i]):
                                x_intersect = ix[i] + (y_line - iy[i]) * (ix[i + 1] - ix[i]) / dy
                                intersections.append(x_intersect)
                            intersections.sort()
                            for i in range(0, len(intersections), 2):
                                if i + 1 < len(intersections):
                                    start_point = (intersections[i], y_line)
                                    end_point = (intersections[i + 1], y_line)
                                    self.laser_ax.plot([start_point[0] * scale, end_point[0] * scale], [start_point[1] * scale, end_point[1] * scale], color='red')
                                    self.laser_ax.set_title(f"Layer {layer_index}")
                                    self.laser_ax.set_xlim(min_x - self.padding, max_x + self.padding)
                                    self.laser_ax.set_ylim(min_y - self.padding, max_y + self.padding)
                                    self.laser_ax.set_aspect('equal', adjustable='box')
                                    time.sleep(0.3)
                                    current = self.prior.get_position()[1].split(',')
                                    distance = ((int(current[0]) - (start_point[0] * scale + self.x)) ** 2 + (int(current[1]) - (start_point[1] * scale + self.y)) ** 2) ** 0.5
                                    self.prior.move_to_position(self.x + start_point[0] * scale, self.y + start_point[1] * scale)
                                    time.sleep(distance / speed * 0.01)
                                    distance = ((abs(end_point[0]) * scale - abs(start_point[0]) * scale) ** 2 + (abs(end_point[1]) * scale - abs(start_point[1]) * scale) ** 2) ** 0.5
                                    self.prior.start_laser()
                                    self.prior.move_to_position(self.x + end_point[0] * scale, self.y + end_point[1] * scale)
                                    time.sleep(distance / speed * 0.01)
                                    self.prior.stop_laser()
                                    time.sleep(0.3)
                                    try:
                                        self.laser_canvas.draw()
                                        self.laser_window.update()
                                    except tk.TclError:
                                        return
                                    self.laser_window.after(10)  # wait time in milliseconds when the laser is moving

    def process_default(self, polygons, scale, min_x, max_x, min_y, max_y, layer_index):
        for polygon in polygons:
            x, y = polygon.exterior.xy
            x = [coord * scale for coord in x]
            y = [coord * scale for coord in y]
            self.laser_ax.plot(x, y)
            for interior in polygon.interiors:
                ix, iy = interior.xy
                ix = [coord * scale for coord in ix]
                iy = [coord * scale for coord in iy]
                self.laser_ax.plot(ix, iy, color='red')  # Plot inner boundaries with dashed lines
        self.laser_ax.set_title(f"Layer {layer_index}: {len(polygons)} polygons")
        self.laser_ax.set_xlim(min_x - self.padding, max_x + self.padding)
        self.laser_ax.set_ylim(min_y - self.padding, max_y + self.padding)
        self.laser_ax.set_aspect('equal', adjustable='box')
        self.laser_canvas.draw()
        self.laser_window.update()

        """_summary_ = This function is used to refresh the ports for the Prior controller.
        """
    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.select_ports_button.delete(0, tk.END)
        for port in ports:
            self.select_ports_button.insert(tk.END, port)
                
        if not ports:
            self.select_ports_button.insert(tk.END, "No ports available")
        else:
            self.select_ports_button.insert(tk.END, "Select a port")

    """_summary_ = This function is used to connect to the Prior controller using the selected port.

    Args:
        event (tk.Event): The event object that triggered the function call.
    """
    def connectPrior(self, event):
        if not self.prior_connected:
            print("---")
            
            port = event.widget.get(event.widget.curselection())[-1]
            self.prior = prior(port)

            try:
                
                self.prior_connected = True
                messagebox.showinfo("Success", "Connected to Prior Controller successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to connect to Prior Controller: {e}")

    """_summary_ = This function is used to show the max and min x and y values of the layers.
    """
    def show_max_min(self):
        if not self.sections:
            messagebox.showerror("Error", "No layers to process!")
            return

        # Calculate the bounds for all layers
        all_x, all_y = [], []
        for section in self.sections:
            if section is not None:
                for polygon in section.polygons_full:
                    x, y = polygon.exterior.xy
                    all_x.extend(x)
                    all_y.extend(y)
        
        if not all_x or not all_y:
            messagebox.showerror("Error", "No valid layers to process!")
            return
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        print(f"Max X: {max_x}, Min X: {min_x}")
        print(f"Max Y: {max_y}, Min Y: {min_y}")
        print(type(self.x+min_x))
        prior.move_to_position(self.prior, self.x + min_x, self.y + min_y)
        time.sleep(5)
        self.prior.start_laser()

        prior.move_to_position(self.prior, self.x + max_x, self.y + min_y)
        time.sleep(5)
        prior.move_to_position(self.prior, self.x + max_x, self.y + max_y)
        time.sleep(5)
        prior.move_to_position(self.prior, self.x + min_x, self.y + max_y)
        time.sleep(5)
        prior.move_to_position(self.prior, self.x + min_x, self.y + min_y)
        self.prior.stop_laser()
    
    """_summary_= This function is used to set the x and y starting position for the laser engraving process.
    """
    #TODO: Implement this function, it is to move the laser to the position, see how guys did it
    def set_xy(self):
        position = self.prior.get_position()[1].split(',')
        print(position)
        self.x = int(position[0])
        self.y = int(position[1])
        pass

        

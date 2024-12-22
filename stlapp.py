import tkinter as tk
from tkinter import filedialog, messagebox
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial.tools.list_ports
from controller import PriorController as prior
import time

class STLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3D STL Slicer")
        self.mesh = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.sections = []
        self.prior = prior

        #start x,y position
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
        tk.Label(root, text="Line Spacing (mm):").grid(row=2, column=0, padx=10, pady=10)
        self.line_spacing_var = tk.DoubleVar(value=0.5)
        self.line_spacing_entry = tk.Entry(root, textvariable=self.line_spacing_var, width=10)
        self.line_spacing_entry.grid(row=2, column=1, padx=10, pady=10)

        # Slice Button
        self.slice_button = tk.Button(root, text="Slice STL", command=self.slice_stl)
        self.slice_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Output
        self.output_frame = tk.Frame(root)
        self.output_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.output_frame)
        self.canvas.get_tk_widget().pack()

        # Layer Selection
        tk.Label(root, text="Select Layer:").grid(row=0, column=2, padx=10, pady=10)
        self.layer_listbox = tk.Listbox(root, height=10)
        self.layer_listbox.grid(row=1, column=2, rowspan=6, padx=10, pady=10)
        self.layer_listbox.bind('<<ListboxSelect>>', self.display_layer)

        

        # Select Ports
        tk.Label(root, text="Select Ports:").grid(row=0, column=3, padx=10, pady=10)
        self.select_ports_button = tk.Listbox(root, height=10)
        self.select_ports_button.grid(row=1, column=3, rowspan=6, padx=10, pady=10)
        self.select_ports_button.bind('<<ListboxSelect>>', self.connectPrior)

        # Laser start button
        self.laser_start_button = tk.Button(root, text="Start Laser", command=self.start_laser)
        self.laser_start_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Refresh ports button
        self.refresh_ports_button = tk.Button(root, text="Refresh Ports", command=self.refresh_ports)
        self.refresh_ports_button.grid(row=7, column=2, columnspan=2, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("STL Files", "*.stl")])
        if file_path:
            self.file_label.config(text=file_path)
            try:
                self.mesh = trimesh.load(file_path)
                if self.mesh.is_watertight:
                    messagebox.showinfo("Success", "STL file loaded successfully!")
                else:
                    messagebox.showwarning("Warning", "STL file is not watertight!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load STL file: {e}")

    def slice_stl(self):
        if not self.mesh:
            messagebox.showerror("Error", "No STL file loaded!")
            return

        layer_thickness = self.layer_thickness_var.get()
        z_min, z_max = self.mesh.bounds[0][2], self.mesh.bounds[1][2]
        z_levels = np.arange(z_min, z_max, layer_thickness)

        try:
            self.sections = self.mesh.section_multiplane(
                plane_origin=[0, 0, 0],
                plane_normal=[0, 0, 1],
                heights=z_levels
            )

            # Update layer listbox
            self.layer_listbox.delete(0, tk.END)
            for i in range(len(self.sections)):
                self.layer_listbox.insert(tk.END, f"Layer {i}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to slice STL file: {e}")

    def display_layer(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            if index < len(self.sections):
                section = self.sections[index]
                self.ax.clear()
                if section is not None:
                    polygons = section.polygons_full
                    for polygon in polygons:
                        x, y = polygon.exterior.xy
                        self.ax.plot(x, y)
                    self.ax.set_title(f"Layer {index}: {len(polygons)} polygons")
                else:
                    self.ax.set_title(f"Layer {index}: No intersection")

                if index == 0 and section is not None:
                    x, y = section.polygons_full[0].exterior.xy
                    self.ax.plot(x[0], y[0], 'ro') 
                
                self.canvas.draw()
        
    def on_closing(self):
        self.root.quit()
        self.root.destroy()
    
    def on_closing_laser(self):
        self.laser_window.destroy()

    def start_laser(self):
        if not self.sections:
            messagebox.showerror("Error", "No layers to process!")
            return

        self.laser_window = tk.Toplevel(self.root)
        self.laser_window.title("Laser Simulation")
        self.laser_figure, self.laser_ax = plt.subplots()
        self.laser_canvas = FigureCanvasTkAgg(self.laser_figure, master=self.laser_window)
        self.laser_canvas.get_tk_widget().pack()
        self.laser_window.protocol("WM_DELETE_WINDOW", self.on_closing_laser)

        self.process_layers()

        
    def process_layers(self):
        
        line_spacing = self.line_spacing_var.get()
        for layer_index, section in enumerate(self.sections):
            self.laser_ax.clear()
            if section is not None:
                polygons = section.polygons_full
                for polygon in polygons:
                    print(polygon.interiors)
                    x, y = polygon.exterior.xy
                    min_y, max_y = min(y), max(y)
                    y_lines = np.arange(min_y, max_y, line_spacing)  # Use user-specified line spacing
                    for y_line in y_lines:
                        intersections = []
                        for i in range(len(x) - 1):
                            if (y[i] <= y_line <= y[i+1]) or (y[i+1] <= y_line <= y[i]).any():
                                x_intersect = x[i] + (y_line - y[i]) * (x[i+1] - x[i]) / (y[i+1] - y[i])
                                intersections.append(x_intersect)
                        intersections.sort()
                        for i in range(0, len(intersections), 2):
                            if i+1 < len(intersections):
                                start_point = (intersections[i], y_line)
                                end_point = (intersections[i+1], y_line)
                                self.prior.move_to_position(self.x+start_point[0], self.y+start_point[1])
                                self.prior.start_laser()
                                self.prior.move_to_position(self.x+end_point[0], self.y+end_point[1])
                                while self.prior.is_moving():
                                    time.sleep(0.1)
                                self.prior.stop_laser()
                                self.laser_ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='blue')
                                self.laser_canvas.draw()
                                self.laser_window.update()
                                self.laser_window.after(10)  # wait time in milliseconds when the laser is on

            self.laser_ax.set_title(f"Layer {layer_index}")
            self.laser_canvas.draw()
            self.laser_window.update()
            self.laser_window.after(500)  # wait time before moving to the next layer

    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.select_ports_button.delete(0, tk.END)
        for port in ports:
            self.select_ports_button.insert(tk.END, port)
                
        if not ports:
            self.select_ports_button.insert(tk.END, "No ports available")
        else:
            self.select_ports_button.insert(tk.END, "Select a port")
        


    def connectPrior(self,event):
        port = event.widget.get(event.widget.curselection())[-1]
        try:
            self.prior.connect(self.prior, port=port)
            messagebox.showinfo("Success", "Connected to Prior Controller successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to Prior Controller: {e}")

import tkinter as tk
from tkinter import filedialog, messagebox
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial.tools.list_ports

class STLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3D STL Slicer")
        self.mesh = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.sections = []

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

        # Slice Button
        self.slice_button = tk.Button(root, text="Slice STL", command=self.slice_stl)
        self.slice_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Output
        self.output_frame = tk.Frame(root)
        self.output_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.output_frame)
        self.canvas.get_tk_widget().pack()

        # Layer Selection
        tk.Label(root, text="Select Layer:").grid(row=4, column=0, padx=10, pady=10)
        self.layer_listbox = tk.Listbox(root, height=10)
        self.layer_listbox.grid(row=5, column=0, padx=10, pady=10)
        self.layer_listbox.bind('<<ListboxSelect>>', self.display_layer)

        # Select Ports
        tk.Label(root, text="Select Ports:").grid(row=4, column=1, padx=10, pady=10)
        self.select_ports_button = tk.Listbox(root, height=10)
        self.select_ports_button.grid(row=5, column=1, padx=10, pady=10)

        # Laser start button
        self.laser_start_button = tk.Button(root, text="Start Laser", command=self.start_laser)
        self.laser_start_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Refresh ports button
        self.refresh_ports_button = tk.Button(root, text="Refresh Ports", command=self.refresh_ports)
        self.refresh_ports_button.grid(row=7, column=0, columnspan=2, pady=10)

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
        self.canvas.draw()
        self.root.quit()
        self.root.destroy()
    
    def start_laser(self):
        if not self.sections:
            messagebox.showerror("Error", "No layers to process!")
            return

        self.laser_window = tk.Toplevel(self.root)
        self.laser_window.title("Laser Simulation")
        self.laser_figure, self.laser_ax = plt.subplots()
        self.laser_canvas = FigureCanvasTkAgg(self.laser_figure, master=self.laser_window)
        self.laser_canvas.get_tk_widget().pack()
        self.laser_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.process_layers()

        drawingPolygon = False
        for layer_index, section in enumerate(self.sections):
            self.laser_ax.clear()
            if section is not None:
                polygons = section.polygons_full
                for polygon in polygons:
                    x, y = polygon.exterior.xy
                    self.laser_ax.plot(x, y, color='blue')
                    for point_index in range(len(x)):
                        self.laser_ax.plot(x[point_index], y[point_index], 'ro', markersize=2)
                        self.laser_canvas.draw()
                        self.laser_window.update()
                        self.laser_window.after(10)  # wait time in milliseconds when the laser is on
                    drawingPolygon = False

            self.laser_ax.set_title(f"Layer {layer_index}")
            self.laser_canvas.draw()
            self.laser_window.update()
            self.laser_window.after(500)  # wait time before moving to the next layer

    def process_layers(self):
            drawingPolygon = False
            for layer_index, section in enumerate(self.sections):
                self.laser_ax.clear()
                if section is not None:
                    polygons = section.polygons_full
                    for polygon in polygons:
                        x, y = polygon.exterior.xy
                        self.laser_ax.plot(x, y, color='blue')
                        drawingPolygon = True
                        for point_index in range(len(x)):
                                self.laser_ax.plot(x[point_index], y[point_index], 'ro', markersize=2)
                                self.laser_canvas.draw()
                                self.laser_window.update()
                                self.laser_window.after(1)  # wait time in milliseconds when the laser is on
                                
                        drawingPolygon = False


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

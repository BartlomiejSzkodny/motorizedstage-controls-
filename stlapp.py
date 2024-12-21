import tkinter as tk
from tkinter import filedialog, messagebox
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
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

        # Canvas for displaying slices
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("STL files", "*.stl")])
        if file_path:
            self.mesh = trimesh.load(file_path)
            self.file_label.config(text=file_path)

    def slice_stl(self):
        if self.mesh is None:
            messagebox.showerror("Error", "No STL file loaded")
            return

        layer_thickness = self.layer_thickness_var.get()
        self.sections = self.mesh.section_multiplane(plane_origin=self.mesh.bounds[0],
                                                     plane_normal=[0, 0, 1],
                                                     heights=np.arange(self.mesh.bounds[0][2], self.mesh.bounds[1][2], layer_thickness))

        self.plot_slices()

    def plot_slices(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        for section in self.sections:
            if section is not None:
                for path in section.polygons_full:
                    patch = Polygon(path, closed=True, fill=True, edgecolor='r', facecolor='b', alpha=0.5)
                    ax.add_patch(patch)

        ax.autoscale_view()
        self.canvas.draw()

    def on_closing(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = STLApp(root)
    root.mainloop()

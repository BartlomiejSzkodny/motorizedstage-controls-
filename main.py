import tkinter as tk
from tkinter import filedialog, messagebox
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class STLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3D STL Slicer")
        self.mesh = None

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
        self.layer_listbox.grid(row=4, column=1, padx=10, pady=10)
        self.layer_listbox.bind('<<ListboxSelect>>', self.display_layer)

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
            self.canvas.draw()

# Run the app
root = tk.Tk()
app = STLApp(root)
root.mainloop()

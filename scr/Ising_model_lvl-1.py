import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numba import jit

# --- PHYSICS ENGINE (Optimized) ---
@jit(nopython=True)
def metropolis_step(lattice, beta, steps):
    n_rows, n_cols = lattice.shape
    for _ in range(n_rows * n_cols * steps):
        x = np.random.randint(0, n_rows)
        y = np.random.randint(0, n_cols)
        
        spin = lattice[x, y]
        neighbor_sum = (
            lattice[(x + 1) % n_rows, y] +
            lattice[(x - 1) % n_rows, y] +
            lattice[x, (y + 1) % n_cols] +
            lattice[x, (y - 1) % n_cols]
        )
        
        dE = 2 * spin * neighbor_sum
        
        if dE <= 0:
            lattice[x, y] *= -1
        elif np.random.random() < np.exp(-dE * beta):
            lattice[x, y] *= -1
            
    return lattice

# --- GUI APPLICATION ---
class IsingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Ising Model Simulator")
        self.root.geometry("900x700")
        
        # Default Parameters
        self.N = 150
        self.temp = 2.27
        self.speed = 1
        self.running = True
        
        # Initialize Lattice
        self.lattice = np.random.choice([1, -1], size=(self.N, self.N))
        
        # --- LAYOUT ---
        # 1. Controls Frame (Bottom)
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Temperature Slider
        lbl_temp = ttk.Label(control_frame, text="Temperature (T):")
        lbl_temp.pack(side=tk.LEFT, padx=5)
        
        self.slider_temp = ttk.Scale(control_frame, from_=0.1, to=10.0, 
                                     orient=tk.HORIZONTAL, length=200, 
                                     command=self.update_temp)
        self.slider_temp.set(self.temp)
        self.slider_temp.pack(side=tk.LEFT, padx=5)
        
        self.lbl_temp_val = ttk.Label(control_frame, text=f"{self.temp:.2f}")
        self.lbl_temp_val.pack(side=tk.LEFT, padx=5)

        # Spacer
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=20)

        # Speed Slider
        lbl_speed = ttk.Label(control_frame, text="Simulation Speed:")
        lbl_speed.pack(side=tk.LEFT, padx=5)
        
        self.slider_speed = ttk.Scale(control_frame, from_=1, to=20, 
                                      orient=tk.HORIZONTAL, length=150,
                                      command=self.update_speed)
        self.slider_speed.set(self.speed)
        self.slider_speed.pack(side=tk.LEFT, padx=5)

        # Reset Button
        btn_reset = ttk.Button(control_frame, text="Randomize / Reset", command=self.reset_lattice)
        btn_reset.pack(side=tk.RIGHT, padx=10)

        # 2. Visualization Frame (Top)
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        self.fig.patch.set_facecolor('#202020') # Dark background for the figure
        
        self.img = self.ax.imshow(self.lattice, cmap='magma', animated=True)
        self.ax.set_axis_off()
        self.ax.set_title("System Evolution", color='white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Start Loop
        self.root.after(10, self.animate)

    def update_temp(self, val):
        self.temp = float(val)
        self.lbl_temp_val.config(text=f"{self.temp:.2f}")

    def update_speed(self, val):
        self.speed = int(float(val))

    def reset_lattice(self):
        self.lattice = np.random.choice([1, -1], size=(self.N, self.N))

    def animate(self):
        # Physics Step
        beta = 1.0 / self.temp
        self.lattice = metropolis_step(self.lattice, beta, self.speed)
        
        # Update Image
        self.img.set_data(self.lattice)
        self.canvas.draw_idle()
        
        # Schedule next frame
        self.root.after(1, self.animate)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    root = tk.Tk()
    # Optional: Try to set a modern theme
    style = ttk.Style()
    try:
        style.theme_use('clam') 
    except:
        pass
        
    app = IsingSimulator(root)
    root.mainloop()
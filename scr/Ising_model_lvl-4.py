import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numba import jit

# --- PHYSICS ENGINE (HEISENBERG MODEL) ---
@jit(nopython=True)
def heisenberg_step(grid, beta, steps):
    n = grid.shape[0]
    for _ in range(n * n * steps):
        x = np.random.randint(0, n)
        y = np.random.randint(0, n)
        
        old_vec = grid[x, y]
        
        # --- 1. Generate Random 3D Unit Vector ---
        # Using Marsaglia's method (uniform sphere sampling)
        while True:
            v1 = np.random.random() * 2 - 1
            v2 = np.random.random() * 2 - 1
            s = v1*v1 + v2*v2
            if s < 1:
                scale = 2 * np.sqrt(1 - s)
                vx = v1 * scale
                vy = v2 * scale
                vz = 1 - 2*s
                new_vec = np.array([vx, vy, vz], dtype=np.float64)
                break
        
        # --- 2. Calculate Energy Change ---
        # Neighbors (Periodic Boundary)
        neighbor_sum = (grid[(x+1)%n, y] + grid[(x-1)%n, y] + 
                        grid[x, (y+1)%n] + grid[x, (y-1)%n])
        
        # Energy = - Dot_Product(Spin, Neighbor_Sum)
        # We calculate the difference directly to save steps
        # dE = -(new_vec . N) - (-(old_vec . N)) = (old_vec - new_vec) . N
        
        dot_old = np.sum(old_vec * neighbor_sum)
        dot_new = np.sum(new_vec * neighbor_sum)
        
        dE = -(dot_new - dot_old)

        # --- 3. Metropolis Check ---
        if dE <= 0 or np.random.random() < np.exp(-dE * beta):
            grid[x, y] = new_vec
            
    return grid

# --- GUI APPLICATION ---
class HeisenbergSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Heisenberg Model: Real-Time 3D Vector Lab")
        self.root.geometry("800x750")
        
        # Parameters
        self.N = 80 # Smaller grid recommended for 3D calculations
        self.temp = 1.0
        self.speed = 1
        
        # Initialize Random Unit Vectors on Sphere
        self.grid = np.random.randn(self.N, self.N, 3)
        # Normalize initial grid
        for i in range(self.N):
            for j in range(self.N):
                self.grid[i,j] /= np.linalg.norm(self.grid[i,j])

        # --- CONTROLS ---
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Temp Slider
        ttk.Label(control_frame, text="Temperature:").pack(side=tk.LEFT)
        self.s_temp = ttk.Scale(control_frame, from_=0.1, to=4.0, command=self.upd_params)
        self.s_temp.set(self.temp)
        self.s_temp.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.lbl_temp = ttk.Label(control_frame, text=f"{self.temp:.2f}")
        self.lbl_temp.pack(side=tk.LEFT)

        # Speed Slider
        ttk.Label(control_frame, text="Speed:").pack(side=tk.LEFT, padx=(10,0))
        self.s_speed = ttk.Scale(control_frame, from_=1, to=10, command=self.upd_params)
        self.s_speed.set(self.speed)
        self.s_speed.pack(side=tk.LEFT, padx=5)

        # Reset
        ttk.Button(control_frame, text="Reset", command=self.reset).pack(side=tk.RIGHT)

        # --- PLOT ---
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.fig.patch.set_facecolor('#202020')
        self.ax.set_axis_off()
        self.ax.set_title("3D Spins (XYZ mapped to RGB)", color='white')
        
        # Initial draw
        self.img = self.ax.imshow(self.vec_to_rgb(self.grid))
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.root.after(10, self.animate)

    def vec_to_rgb(self, grid):
        # Map vectors (-1 to 1) to RGB colors (0 to 1)
        return (grid + 1) / 2

    def upd_params(self, val):
        self.temp = float(self.s_temp.get())
        self.speed = int(float(self.s_speed.get()))
        self.lbl_temp.config(text=f"{self.temp:.2f}")

    def reset(self):
        # Re-initialize random unit vectors
        self.grid = np.random.randn(self.N, self.N, 3)
        for i in range(self.N):
            for j in range(self.N):
                self.grid[i,j] /= np.linalg.norm(self.grid[i,j])

    def animate(self):
        beta = 1.0 / self.temp
        self.grid = heisenberg_step(self.grid, beta, self.speed)
        
        self.img.set_data(self.vec_to_rgb(self.grid))
        self.canvas.draw_idle()
        self.root.after(1, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = HeisenbergSimulator(root)
    root.mainloop()
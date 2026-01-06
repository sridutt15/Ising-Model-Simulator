import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import hsv_to_rgb
from numba import jit

# --- PHYSICS ENGINE (XY MODEL) ---
@jit(nopython=True)
def xy_step(thetas, beta, steps):
    n = thetas.shape[0]
    for _ in range(n * n * steps):
        x = np.random.randint(0, n)
        y = np.random.randint(0, n)
        
        old_theta = thetas[x, y]
        # Propose small rotation (Metropolis)
        new_theta = old_theta + (np.random.random() - 0.5) * 2.0 
        
        # Periodic Boundary Neighbors
        neighbors = [thetas[(x+1)%n, y], thetas[(x-1)%n, y], 
                     thetas[x, (y+1)%n], thetas[x, (y-1)%n]]
        
        E_old = 0.0
        E_new = 0.0
        for nb in neighbors:
            E_old -= np.cos(old_theta - nb)
            E_new -= np.cos(new_theta - nb)
            
        dE = E_new - E_old

        if dE <= 0 or np.random.random() < np.exp(-dE * beta):
            thetas[x, y] = new_theta
            
    return thetas

# --- GUI APPLICATION ---
class XYSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("XY Model: Real-Time Vortex Lab")
        self.root.geometry("800x700")
        
        # Parameters
        self.N = 100
        self.temp = 0.85
        self.speed = 1
        self.thetas = np.random.random((self.N, self.N)) * 2 * np.pi
        self.image_buffer = np.zeros((self.N, self.N, 3))

        # --- CONTROLS ---
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Temp Slider
        ttk.Label(control_frame, text="Temperature:").pack(side=tk.LEFT)
        self.s_temp = ttk.Scale(control_frame, from_=0.1, to=3.0, command=self.upd_params)
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
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        self.fig.patch.set_facecolor('#202020')
        self.ax.set_axis_off()
        self.img = self.ax.imshow(self.get_rgb(), interpolation='bilinear')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.root.after(10, self.animate)

    def get_rgb(self):
        # Map Angle to Hue (HSV -> RGB)
        hue = (self.thetas % (2*np.pi)) / (2*np.pi)
        self.image_buffer[..., 0] = hue
        self.image_buffer[..., 1] = 1.0 # Saturation
        self.image_buffer[..., 2] = 1.0 # Value
        return hsv_to_rgb(self.image_buffer)

    def upd_params(self, val):
        self.temp = float(self.s_temp.get())
        self.speed = int(float(self.s_speed.get()))
        self.lbl_temp.config(text=f"{self.temp:.2f}")

    def reset(self):
        self.thetas = np.random.random((self.N, self.N)) * 2 * np.pi

    def animate(self):
        beta = 1.0 / self.temp
        self.thetas = xy_step(self.thetas, beta, self.speed)
        self.img.set_data(self.get_rgb())
        self.canvas.draw_idle()
        self.root.after(1, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = XYSimulator(root)
    root.mainloop()
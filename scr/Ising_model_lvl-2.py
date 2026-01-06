import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numba import jit

# --- PHYSICS ENGINE (POTTS MODEL) ---
@jit(nopython=True)
def potts_step(grid, beta, q, steps):
    n = grid.shape[0]
    for _ in range(n * n * steps):
        x, y = np.random.randint(0, n), np.random.randint(0, n)
        current_s = grid[x, y]
        new_s = np.random.randint(0, q) # Random new color
        
        if current_s == new_s: continue

        neighbors = [grid[(x+1)%n, y], grid[(x-1)%n, y], 
                     grid[x, (y+1)%n], grid[x, (y-1)%n]]
        
        # Energy: -1 if matching, 0 if different
        E_current = 0
        for nb in neighbors:
            if nb == current_s: E_current -= 1
            
        E_new = 0
        for nb in neighbors:
            if nb == new_s: E_new -= 1
            
        dE = E_new - E_current

        if dE <= 0 or np.random.random() < np.exp(-dE * beta):
            grid[x, y] = new_s
    return grid

# --- GUI APPLICATION ---
class PottsSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Potts Model: Real-Time Crystal Lab")
        self.root.geometry("800x700")
        
        self.N = 150
        self.temp = 0.8
        self.q = 4
        self.speed = 1
        self.grid = np.random.randint(0, self.q, size=(self.N, self.N))

        # --- CONTROLS ---
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Q-State Slider
        ttk.Label(control_frame, text="States (Q):").pack(side=tk.LEFT)
        self.s_q = ttk.Scale(control_frame, from_=2, to=10, command=self.reset_needed)
        self.s_q.set(self.q)
        self.s_q.pack(side=tk.LEFT, padx=5)
        self.lbl_q = ttk.Label(control_frame, text=f"{self.q}")
        self.lbl_q.pack(side=tk.LEFT)

        # Temp Slider
        ttk.Label(control_frame, text="Temp:").pack(side=tk.LEFT, padx=(10,0))
        self.s_temp = ttk.Scale(control_frame, from_=0.1, to=2.0, command=self.upd_params)
        self.s_temp.set(self.temp)
        self.s_temp.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Reset
        ttk.Button(control_frame, text="Reset", command=self.reset).pack(side=tk.RIGHT)

        # --- PLOT ---
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.fig.patch.set_facecolor('#202020')
        self.ax.set_axis_off()
        # 'tab10' is good for categorical data (distinct colors)
        self.img = self.ax.imshow(self.grid, cmap='tab10', vmin=0, vmax=9)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.root.after(10, self.animate)

    def upd_params(self, val):
        self.temp = float(self.s_temp.get())

    def reset_needed(self, val):
        # Update Q label but don't reset immediately to avoid lag, 
        # usually user wants to reset after picking Q
        self.q = int(float(self.s_q.get()))
        self.lbl_q.config(text=f"{self.q}")

    def reset(self):
        self.q = int(float(self.s_q.get()))
        self.grid = np.random.randint(0, self.q, size=(self.N, self.N))

    def animate(self):
        beta = 1.0 / self.temp
        self.grid = potts_step(self.grid, beta, self.q, self.speed)
        self.img.set_data(self.grid)
        self.canvas.draw_idle()
        self.root.after(1, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = PottsSimulator(root)
    root.mainloop()

# Level 2: The Potts Model"The Integration of Diversity"The Complication: In the Ising model, you are either "with us" or "against us." In the Potts model, there are multiple options (states $0, 1, 2... q$).The Outcome: You won't see just two massive continents fighting. You will see a Mosaic. This simulates how crystals form (grains), where different patches grow and meet at "grain boundaries."The Physics Change: The energy rule changes. If neighbors are the same $\rightarrow$ Energy is Low. If neighbors are different $\rightarrow$ Energy is High (it doesn't matter how different, just that they are not the same).
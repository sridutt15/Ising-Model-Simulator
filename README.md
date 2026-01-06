# The Physics of Reality: From Ising to Heisenberg 🧲

A real-time, interactive laboratory simulating the statistical physics of magnetic spins. This project visualizes how complex behavior (phase transitions, vortices, and crystal formation) emerges from simple rules.

The simulators are built in **Python** and accelerated using **Numba** for high-performance real-time visualization.

## 🚀 The Ladder of Reality

This repository is structured as a progression of complexity, moving from simple binary systems to realistic 3D quantum models.

### Level 1: The Ising Model (Binary) ⬛⬜
* **The World:** Black and White.
* **The Physics:** Spins can only be Up (+1) or Down (-1).
* **What to look for:** At **T ≈ 2.27**, watch for "Critical Opalescence"—large fractal domains fighting for dominance.
* **Run it:** `python src/Ising_model_lvl-1.py`

### Level 2: The Potts Model (Diversity) 🎨
* **The World:** A Mosaic.
* **The Physics:** Spins have $Q$ different states (colors). This models crystal grain boundaries and foam structures.
* **What to look for:** "Grain Growth." Watch how distinct colored regions form borders that slowly shift as the crystal "anneals."
* **Run it:** `python src/Ising_model_lvl-2.py`

### Level 3: The XY Model (Freedom) 🌀
* **The World:** Swirling Fluids.
* **The Physics:** Spins are 2D vectors that can rotate 360°.
* **What to look for:** **Vortices!** Look for pinwheels of color. At low temperatures, they pair up (bound states). As you heat it up, they break apart. This visualizes the Nobel Prize-winning **Kosterlitz-Thouless transition**.
* **Run it:** `python src/Ising_model_lvl-3.py`

### Level 4: The Heisenberg Model (Reality) 🌐
* **The World:** 3D Texture.
* **The Physics:** Spins are 3D vectors $(x, y, z)$ on a sphere. This represents real magnetic materials like Iron.
* **What to look for:** Smooth, continuous gradients resembling brushed metal or silk.
* **Run it:** `python src/Ising_model_lvl-4.py`

---

## 🛠️ Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/physics-of-reality.git](https://github.com/sridutt15/Ising-Model-Simulator.git)
    cd Ising-Model-Simulator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run a simulation:**
    Navigate to the source folder and run any model:
    ```bash
    python src/Ising_model_lvl-3.py
    ```

## 🎮 Controls

All simulations come with a Real-Time GUI:
* **Temperature Slider:** Control the chaos. Low T = Order, High T = Noise.
* **Speed Slider:** Fast forward the evolution.
* **Reset:** Re-randomize the grid to start over.

## 📚 Tech Stack
* **Python:** Core Logic.
* **NumPy:** Matrix operations.
* **Matplotlib:** Real-time rendering.
* **Numba:** JIT compilation (accelerates the physics loops by ~100x).
* **Tkinter:** GUI Controls.

---
*Created for the love of Physics and Code.*
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CartesianPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Cartesian Plane Plotter")

        # Input fields for X and Y coordinates
        tk.Label(root, text="X Coordinate:").grid(row=0, column=0, padx=5, pady=5)
        self.x_entry = tk.Entry(root)
        self.x_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Y Coordinate:").grid(row=1, column=0, padx=5, pady=5)
        self.y_entry = tk.Entry(root)
        self.y_entry.grid(row=1, column=1, padx=5, pady=5)

        # Color Selection Dropdown
        tk.Label(root, text="Point Color:").grid(row=2, column=0, padx=5, pady=5)
        self.color_var = tk.StringVar(value="red")  # Default color
        colors = ["red", "blue", "green", "black", "purple", "orange"]
        self.color_menu = tk.OptionMenu(root, self.color_var, *colors)
        self.color_menu.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        self.plot_button = tk.Button(root, text="Plot Point", command=self.plot_point)
        self.plot_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.clear_button = tk.Button(root, text="Clear Plot", command=self.clear_plot)
        self.clear_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Matplotlib Figure
        self.fig = Figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111)

        # Embedding Matplotlib into Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

        # Now call setup_axes AFTER self.canvas is initialized
        self.setup_axes()

        # Plot predefined points
        self.plot_initial_points()

    def setup_axes(self):
        """Setup Cartesian plane with grid and axes"""
        self.ax.clear()
        self.ax.set_xlim(-1, 1)  # X-axis range from -1 to 1
        self.ax.set_ylim(-1, 1)  # Y-axis range from -1 to 1
        self.ax.axhline(0, color='black', linewidth=1)  # X-axis line
        self.ax.axvline(0, color='black', linewidth=1)  # Y-axis line
        self.ax.grid(True, linestyle="--", linewidth=0.5)
        self.canvas.draw()

    def plot_initial_points(self):
        """Plot predefined points at startup."""
        initial_points = {"Tx1": (0, 1), "Tx2": (-1, 0), "Tx3": (0, -1), "Tx4": (1, 0)}
        for label, (x, y) in initial_points.items():
            self.ax.plot(x, y, 'o', color='blue', markersize=8)  # Plot points
            self.ax.text(x, y, f" {label}", fontsize=12, verticalalignment='bottom', horizontalalignment='right')

        self.canvas.draw()  # Update canvas

    def plot_point(self):
        """Plot the point entered in the input fields with selected color."""
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            color = self.color_var.get()

            self.ax.plot(x, y, 'o', color=color, markersize=8)  # Plot point
            self.canvas.draw()  # Update canvas
        except ValueError:
            print("Please enter valid numbers for X and Y.")

    def clear_plot(self):
        """Clear all plotted points and reset the axes."""
        self.setup_axes()  # Reset the axes
        self.plot_initial_points()  # Re-add predefined points

# Run the application
root = tk.Tk()
app = CartesianPlotter(root)
root.mainloop()

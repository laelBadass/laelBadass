import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import joblib
import numpy as np

class CartesianPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Rx Location Predictor By ELLA")

        # Load the trained ML model
        self.model = joblib.load("rx_location_predictor.pkl")

        # Create input fields for the 4 values
        self.entries = []
        for i in range(4):
            tk.Label(root, text=f"It {i+1}:").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(root)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(entry)

        # Predict Button
        self.predict_button = tk.Button(root, text="Predict & Plot", command=self.predict_and_plot)
        self.predict_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Matplotlib Figure for Cartesian Plane
        self.fig = Figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

        # Setup the Cartesian Plane
        self.setup_axes()
        
        # Plot predefined points
        self.plot_initial_points()

    def setup_axes(self):
        """Setup Cartesian plane"""
        self.ax.clear()
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.grid(True, linestyle="--", linewidth=0.5)
        self.canvas.draw()
        
    
    def plot_initial_points(self):
        """Plot predefined points at startup."""
        initial_points = {"Tx1": (0, 1), "Tx2": (-1, 0), "Tx3": (0, -1), "Tx4": (1, 0)}
        for label, (x, y) in initial_points.items():
            self.ax.plot(x, y, 'o', color='black', markersize=50)  # Plot points
            self.ax.text(x, y, f" {label}", fontsize=20, verticalalignment='bottom', horizontalalignment='right',color='blue')

        self.canvas.draw()  # Update canvas    
        

    def predict_and_plot(self):
        """Use the ML model to predict (x, y) from 4 inputs and plot the point"""
        try:
            # Get values from input fields
            input_values = [float(entry.get()) for entry in self.entries]
            sorted_input_values = sorted(input_values)  # Sort the values
            a = sorted_input_values[0]/sorted_input_values[3]  
            b = sorted_input_values[0]/sorted_input_values[2]
            c = sorted_input_values[0]/sorted_input_values[1]
            d = sorted_input_values[1]/sorted_input_values[3]
            e = sorted_input_values[1]/sorted_input_values[2]
            f = sorted_input_values[2]/sorted_input_values[3]
            g = sorted_input_values[3]-sorted_input_values[0]
            h = sorted_input_values[2]-sorted_input_values[0]
            j = sorted_input_values[1]-sorted_input_values[0]
            k = sorted_input_values[3]-sorted_input_values[1]
            l = sorted_input_values[2]-sorted_input_values[1]
            m = sorted_input_values[3]-sorted_input_values[2]
            input_array = input_values + [a,b,c,d,e,f,g,h,j,k,l,m]  # Reshape for model
            print(input_array)
            #input_array = np.array([input_values]).reshape(1, -1)  # Reshape for model

            # Predict (x, y) using the trained model
            x_pred, y_pred = self.model.predict([input_array])[0]
            print(input_array)
            # Plot the predicted point
            self.ax.plot(x_pred, y_pred, 'o', color='red', markersize=8)
            self.canvas.draw()

        except ValueError:
            print("Please enter valid numeric values.")

# Run the application
root = tk.Tk()
app = CartesianPlotter(root)
root.mainloop()

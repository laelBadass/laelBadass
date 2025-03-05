import customtkinter as ctk
import numpy as np

class ComplexNumberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Complex Number Calculator")

        # Title Label
        ctk.CTkLabel(root, text="Enter 4 Complex Numbers:", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Entry Fields for Complex Numbers
        self.entries = []
        for i in range(4):
            ctk.CTkLabel(root, text=f"Value {i+1}:").grid(row=i+1, column=0, padx=5, pady=5)
            entry = ctk.CTkEntry(root, width=150)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            self.entries.append(entry)

        # Buttons for Calculating Average & Median
        self.avg_button = ctk.CTkButton(root, text="Calculate Average", command=self.calculate_average)
        self.avg_button.grid(row=5, column=0, pady=10)

        self.median_button = ctk.CTkButton(root, text="Calculate Median", command=self.calculate_median)
        self.median_button.grid(row=5, column=1, pady=10)

        # Labels to Display Results
        self.avg_label = ctk.CTkLabel(root, text="Average: --", font=("Arial", 12))
        self.avg_label.grid(row=6, column=0, columnspan=2, pady=5)

        self.median_label = ctk.CTkLabel(root, text="Median: --", font=("Arial", 12))
        self.median_label.grid(row=7, column=0, columnspan=2, pady=5)

    def get_complex_numbers(self):
        """Fetch and convert user input to complex numbers."""
        try:
            complex_numbers = [complex(entry.get()) for entry in self.entries]
            return complex_numbers
        except ValueError:
            self.avg_label.configure(text="Error: Invalid Input", text_color="red")
            self.median_label.configure(text="Error: Invalid Input", text_color="red")
            return None

    def calculate_average(self):
        """Calculate the average of the input complex numbers."""
        numbers = self.get_complex_numbers()
        if numbers:
            avg = sum(numbers) / len(numbers)
            self.avg_label.configure(text=f"Average: {avg}")

    def calculate_median(self):
        """Calculate the median of the input complex numbers."""
        numbers = self.get_complex_numbers()
        if numbers:
            median = np.median(numbers)
            self.median_label.configure(text=f"Median: {median}")

# Run the application
root = ctk.CTk()
app = ComplexNumberApp(root)
root.mainloop()

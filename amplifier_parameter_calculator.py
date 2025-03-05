import customtkinter as ctk
import numpy as np

class ComplexNumberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Amplifier Parameters Calculator By ELLA")

        # Title Label
        ctk.CTkLabel(root, text="Enter 4 Complex Numbers:", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Entry Fields for Complex Numbers
        self.entries = []
        for i in range(4):
            ctk.CTkLabel(root, text=f"S{i+1}:").grid(row=i+1, column=0, padx=5, pady=5)
            entry = ctk.CTkEntry(root, width=150, placeholder_text="0.0+0.0j")
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            self.entries.append(entry)

        # Buttons for Calculating Average & Median
        self.avg_button = ctk.CTkButton(root, text="Calculate reflexion coefficient and gain", command=self.gammaS_gammaL)
        self.avg_button.grid(row=5, column=0, pady=10)

        self.median_button = ctk.CTkButton(root, text="Calculate stability factors", command=self.calculate_stability_factors)
        self.median_button.grid(row=5, column=2, pady=10)

        # Labels to Display Results
        self.avg_label = ctk.CTkLabel(root, text="GammaS: --", font=("Arial", 12))
        self.avg_label.grid(row=6, column=0, columnspan=2, pady=5)
        self.gammaL_label = ctk.CTkLabel(root, text="GammaL: --", font=("Arial", 12))
        self.gammaL_label.grid(row=7, column=0, columnspan=2, pady=5)
        self.gain_label = ctk.CTkLabel(root, text="Transducer gain max: --", font=("Arial", 12))
        self.gain_label.grid(row=8, column=0, columnspan=2, pady=5)
        

        self.muS_label = ctk.CTkLabel(root, text="Mu input: --", font=("Arial", 12))
        self.muS_label.grid(row=6, column=2, columnspan=2, pady=5)
        self.muL_label = ctk.CTkLabel(root, text="Mu output: --", font=("Arial", 12))
        self.muL_label.grid(row=6, column=3, columnspan=2, pady=5)
        self.k_label = ctk.CTkLabel(root, text="K factor: --", font=("Arial", 12))
        self.k_label.grid(row=7, column=2, columnspan=2, pady=5)
        self.stability_label = ctk.CTkLabel(root, text="", font=("Arial", 12))
        self.stability_label.grid(row=8, column=2, columnspan=2, pady=5)

    def get_complex_numbers(self):
        """Fetch and convert user input to complex numbers."""
        try:
            complex_numbers = [complex(entry.get()) for entry in self.entries]
            return complex_numbers
        except ValueError:
            self.avg_label.configure(text="Error: Invalid Input", text_color="red")
            self.median_label.configure(text="Error: Invalid Input", text_color="red")
            return None

    def calculate_stability_factors(self):
        """Calculate the stability factors of the input complex numbers."""
        numbers = self.get_complex_numbers()
        S11 = numbers[0]
        S12 = numbers[1]
        S21 = numbers[2]
        S22 = numbers[3]
        delta = S11 * S22 - S12 * S21
        k_factor = (1-abs(S11)**2-abs(S22)**2+abs(delta)**2)/(2*abs(S12*S21))
        mu_factorS = ((1-abs(S11)**2)/((abs(S22-S11.conjugate()*delta))+(abs(S12*S21))))
        mu_factorL = ((1-abs(S22)**2)/((abs(S11-S22.conjugate()*delta))+(abs(S12*S21))))
        if mu_factorS > 1 and mu_factorL:
            self.stability_label.configure(text="Unconditionnaly Stable", text_color="green")
        elif mu_factorS > 1 and mu_factorL < 1:
            self.stability_label.configure(text="Input Stable  Output Unstable", text_color="blue")
        elif mu_factorS < 1 and mu_factorL > 1:
            self.stability_label.configure(text="Input Unstable  Output Stable", text_color="blue")
        else:
            self.stability_label.configure(text="Unstable", text_color="red")
        
       
        self.muS_label.configure(text=f"Mu input: {mu_factorS:.4f}")
        self.muL_label.configure(text=f"Mu output: {mu_factorL:.4f}")
        self.k_label.configure(text=f"K factor: {k_factor:.4f}")
        
        

    def calculate_median(self):
        """Calculate the median of the input complex numbers."""
        numbers = self.get_complex_numbers()
        if numbers:
            median = np.median(numbers)
            self.median_label.configure(text=f"Median: {median}")
            
            
    # def calculate_transducer_gain(self):
    #     """Calculate the transducer gain."""
    #     numbers = self.get_complex_numbers()
    #     gammaS, gammaL = self.gammaS_gammaL()
    #     S11, S12, S21, S22 = numbers
    #     gammaIN = S11 + ((S12*S21*gammaL)/(1-S22*gammaL))
    #     gammaOUT = S22 + ((S12*S21*gammaS)/(1-S11*gammaS))
    #     gainS = ((1-abs(gammaS)**2)/(abs(1-gammaIN*gammaS)**2))
    #     gain0 = abs(S21)**2
    #     gainL = ((1-abs(gammaL)**2)/(abs(1-S22*gammaL)**2))
    #     gainT = gainS * gain0 * gainL 
    #     gainSdB = 10*np.log10(gainS)
    #     gain0dB = 10*np.log10(gain0)
    #     gainLdB = 10*np.log10(gainL)
    #     gainTdB = 10*np.log10(gainT)  
    #     self.gain_label.configure(text=f"Transducer gain: {gainTdB:.4f}")    
            
            
    def gammaS_gammaL(self):
        """Calculate the source and load reflection coefficients."""
        numbers = self.get_complex_numbers()
        S11 = numbers[0]
        S12 = numbers[1]
        S21 = numbers[2]
        S22 = numbers[3]
        delta = S11 * S22 - S12 * S21
        B1 = 1 + abs(S11)**2 - abs(S22)**2 - abs(delta)**2
        B2 = 1 + abs(S22)**2 - abs(S11)**2 - abs(delta)**2
        C1 = S11 - delta * S22.conjugate()
        C2 = S22 - delta* S11.conjugate()
        gammaSplus = ((B1+(B1**2-4*abs(C1)**2)**0.5)/(2*C1))
        gammaSminus = ((B1-(B1**2-4*abs(C1)**2)**0.5)/(2*C1))
        gammaLplus = ((B2+(B2**2-4*abs(C2)**2)**0.5)/(2*C2))
        gammaLminus = ((B2-(B2**2-4*abs(C2)**2)**0.5)/(2*C2))
        if abs(gammaSplus) < 1:
            gammaS = gammaSplus
        else:
            gammaS = gammaSminus
        if abs(gammaLplus) < 1:
            gammaL = gammaLplus
        else:
            gammaL = gammaLminus
        
        gammaIN = S11 + ((S12*S21*gammaL)/(1-S22*gammaL))
        gammaOUT = S22 + ((S12*S21*gammaS)/(1-S11*gammaS))
        gainS = ((1-abs(gammaS)**2)/(abs(1-gammaIN*gammaS)**2))
        gain0 = abs(S21)**2
        gainL = ((1-abs(gammaL)**2)/(abs(1-S22*gammaL)**2))
        gainT = gainS * gain0 * gainL 
        
        gainSdB = 10*np.log10(gainS)
        gain0dB = 10*np.log10(gain0)
        gainLdB = 10*np.log10(gainL)
        gainTdB = gainSdB + gain0dB + gainLdB  
        print(gainSdB, gain0dB, gainLdB, gainTdB)
        self.gain_label.configure(text=f"Transducer gain: {gainTdB:.4f}dB")   
        self.avg_label.configure(text=f"GammaS+: {gammaSplus:.4f}")
        self.gammaL_label.configure(text=f"GammaL+: {gammaLplus:.4f}")
        

# Run the application
root = ctk.CTk()
app = ComplexNumberApp(root)
root.geometry("720x480")
root.mainloop()

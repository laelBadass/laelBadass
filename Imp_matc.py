import customtkinter 
import tkinter 
import cmath 
from PIL import Image


def inductance_from_impedance(Z, f):
    """Calculate inductance (L) from impedance (Z) at frequency f."""
    omega = 2 * cmath.pi * f  # Angular frequency
    Z = Z * 50
    L = abs(Z) / omega
    return L

def inductance_from_admittance(Y, f):
    """Calculate inductance (L) from admittance (Y) at frequency f."""
    omega = 2 * cmath.pi * f
    Y = Y * 0.02
    if Y.imag == 0:
        raise ValueError("Admittance must have an imaginary part for inductance calculation.")
    L = -1 / (omega * Y.imag)
    return L

def capacitance_from_impedance(Z, f):
    """Calculate capacitance (C) from impedance (Z) at frequency f."""
    omega = 2 * cmath.pi * f
    Z = Z * 50
    if Z.imag == 0:
        raise ValueError("Impedance must have an imaginary part for capacitance calculation.")
    C = -1 / (omega * Z.imag)
    return C

def capacitance_from_admittance(Y, f):
    """Calculate capacitance (C) from admittance (Y) at frequency f."""
    omega = 2 * cmath.pi * f
    Y = Y * 0.02
    C = abs(Y) / omega
    return C


def find_first_element_type(Zi):
    """Determine the type of the first element in the matching network."""
    if Zi.imag > 0:
        return "C"
    elif Zi.imag < 0:
        return "L"
    else:
        return "R"
    
    
    
def find_second_element_type(Lx1,Cx1,Lx2,Cx2,Lx3,Cx3,Lx4,Cx4):
    """Determine the type of the second element in the matching network."""
    y1 = ""
    y2 = ""
    y3 = ""
    y4 = ""
    if ((Lx1 != 0) or (Cx1 != 0)):
        y1 = "SC"
    if ((Lx2 != 0) or (Cx2 != 0)):
        y2 = "SL"
    if ((Lx3 != 0) or (Cx3 != 0)):
        y3 = "PC"
    if ((Lx4 != 0) or (Cx4 != 0)):
        y4 = "PL"
    return y1,y2,y3,y4
    
    
    
def find_x1_x2(Zi,Zta,Za):
    try:
        i = 0.01
        x = 0
        y = 0
        #print(f"Normalized Impedance from Admittance: {Za:.4f}")
        while(y<1.02):
            Zta = complex(Zta.real,(Zta.imag + i))
            Zi = 1 / Zta
            x = x + i
            #y = y+1
            y = Zi.real
            # print(f"Normalized Admittance from Impedance: {Zta:.4f}")
            # print(f"Normalized Impedance from Admittance: {Zi:.4f}")
        x = x    
        Zx = complex(Zi.real, (-Zi.imag))
        Yx = 1 / Zx
        x2 = abs(Za.imag)+abs(Yx.imag)
        x1 = complex(0,x)
        x2 = complex(0,x2)
        y1 = complex(0,Zi.imag)
        y2 = complex(0,Zx.imag)
                     
    except ValueError:
        print("Please enter a valid number")  # Error message
        
    return x1, x2, y1, y2


def find_x3_x4(Zi,Zti,Za):
    try:
        i = -0.01
        x = 0
        y = 0
        #print(f"Normalized Impedance from Admittance: {Za:.4f}")
        Zti = complex(Zti.real,Zti.imag )/50
        Zi = complex(Zi.real,Zi.imag )/50
        while(y<1.02):
            Zti = complex(Zti.real,(Zti.imag + i))
            Za = 1 / Zti
            x = x + i
            #y = y+1
            y = Za.real
            # print(f"Normalized Admittance from Impedance: {Za:.4f}")
            # print(f"Normalized Impedance from Admittance: {Zti:.4f}") 
        Zx = complex(Zti.real, (-Zti.imag))
        Yx = 1 / Zx
        x2 = -Zi.imag + Zx.imag
        x3 = complex(0,x)
        x4 = complex(0,x2)
        y3 = complex(0,Za.imag)
        y4 = complex(0,Yx.imag)    
                     
    except ValueError:
        print("Please enter a valid number")  # Error message
        
    return x3, x4, y3, y4
    


def calculate_first_element(Zi, Zti, Za,Zta,f):
    """Calculate the first element in the matching network."""
    C1,C2,D1,D2 = find_x1_x2(Zi,Zta,Za)
    C3,C4,D3,D4 = find_x3_x4(Zi,Zti,Za)
    Lx1 = 0
    Cx1 = 0     
    Lx2 = 0
    Cx2 = 0
    Lx3 = 0
    Cx3 = 0
    Lx4 = 0
    Cx4 = 0
    Cy1 = 0
    Cy3 = 0
    Ly2 = 0
    Ly4 = 0
    # Determine the type of the first element
    first_element_type = find_first_element_type(Zi)
    # Calculate the first element
    if ((first_element_type == "L") and (C1.imag != 0)):
        Lx1 = inductance_from_admittance(C1, f)
    if ((first_element_type == "C") and (C1.imag != 0)):
        Cx1 = capacitance_from_admittance(C1, f)
    if ((first_element_type == "L") and (C2.imag != 0)):
        Lx2 = inductance_from_admittance(C2, f)
    if ((first_element_type == "C") and (C2.imag != 0)):
        Cx2 = capacitance_from_admittance(C2, f)
    if ((first_element_type == "L") and (C3.imag != 0)):
        Lx3 = inductance_from_impedance(C3, f)
    if ((first_element_type == "C") and (C3.imag != 0)):
        Cx3 = capacitance_from_impedance(C3, f)
    if ((first_element_type == "L") and (C4.imag != 0)):
        Lx4 = inductance_from_impedance(C4, f)
    if ((first_element_type == "C") and (C4.imag != 0)):
        Cx4 = capacitance_from_impedance(C4, f)
        
    y1,y2,y3,y4 = find_second_element_type(Lx1,Cx1,Lx2,Cx2,Lx3,Cx3,Lx4,Cx4)
    if y1 == "SC":
        Cy1 = capacitance_from_impedance(D1, f)
    if y2 == "SL":
        Ly2 = inductance_from_impedance(D2, f)
    if y3 == "PC":
        Cy3 = capacitance_from_admittance(D3, f)
    if y4 == "PL":
        Ly4 = inductance_from_admittance(D4, f)
    return abs(Lx1), abs(Cx1), abs(Lx2), abs(Cx2), abs(Lx3), abs(Cx3), abs(Lx4), abs(Cx4), abs(Cy1), abs(Ly2), abs(Cy3), abs(Ly4)


def circuit_assembling(Cx1, Lx1, Cx2, Lx2, Cx3, Lx3, Cx4, Lx4):
    """Assemble the impedance matching circuit."""
    circuit = []
    if Cx1 != 0:
        circuit.append("SC_PC")
    if Lx1 != 0:
        circuit.append("SC_PL")
    if Cx2 != 0:
        circuit.append("SL_PC")
    if Lx2 != 0:
        circuit.append("SL_PL")
    if Cx3 != 0:
        circuit.append("PC_SC")
    if Lx3 != 0:
        circuit.append("PL_SC")
    if Cx4 != 0:
        circuit.append("PC_SL")
    if Lx4 != 0:
        circuit.append("PL_SL")
    return circuit


class MatchingCircuit:
    def __init__(self, type, element1, element2, elementText1, elementText2):
        self.type = type
        self.element1 = element1
        self.element2 = element2 
        self.elementText1 = elementText1
        self.elementText2 = elementText2      




def result_assembling(circuit, Cy1, Cx1, Ly2, Lx1, Cx2, Lx2, Cy3, Cx3, Ly4, Lx3, Cx4, Lx4):
    """Assemble the impedance matching circuit results."""
    result = []
    for i, element in enumerate(circuit):
        if element == "SC_PC":
            p1 = MatchingCircuit("SC_PC", Cy1, Cx1, f"Cs = {Cy1*1e12:.3f} pF", f"Cp = {Cx1*1e12:.3f} pF")
            result.append(p1)
        if element == "SC_PL":
            p2 = MatchingCircuit("SC_PL", Cy1, Lx1, f"Cs = {Cy1*1e12:.3f} pF", f"Lp = {Lx1*1e9:.3f} nH")
            result.append(p2)
        if element == "SL_PC":
            p3 = MatchingCircuit("SL_PC", Ly2, Cx2, f"Ls = {Ly2*1e9:.3f} nH", f"Cp = {Cx2*1e12:.3f} pF")
            result.append(p3)
        if element == "SL_PL":
            p4 = MatchingCircuit("SL_PL", Ly2, Lx2, f"Ls = {Ly2*1e9:.3f} nH", f"Lp = {Lx2*1e9:.3f} nH")
            result.append(p4)
        if element == "PC_SC":
            p5 = MatchingCircuit("PC_SC", Cy3, Cx3, f"Cp = {Cy3*1e12:.3f} pF", f"Cs = {Cx3*1e12:.3f} pF")
            result.append(p5)
        if element == "PL_SC":
            p6 = MatchingCircuit("PL_SC", Ly4, Cx4, f"Lp = {Ly4*1e9:.3f} nH", f"Cs = {Cx4*1e12:.3f} pF")
            result.append(p6)
        if element == "PC_SL":
            p7 = MatchingCircuit("PC_SL", Cx4, Ly4, f"Cp = {Cx4*1e12:.3f} pF", f"Ls = {Ly4*1e9:.3f} nH")
            result.append(p7)
        if element == "PL_SL":
            p8 = MatchingCircuit("PL_SL", Ly4, Lx4, f"Lp = {Ly4*1e9:.3f} nH", f"Ls = {Lx4*1e9:.3f} nH")
            result.append(p8)
    return result



def radiobutton_event(selected_index):
    # Disable all entries
    Real1.configure(state="disabled")
    Img1.configure(state="disabled")
    Real2.configure(state="disabled")
    Img2.configure(state="disabled")
    Real3.configure(state="disabled")
    Img3.configure(state="disabled")
    
    if selected_index == 1:
        Real1.configure(state="normal")
        Img1.configure(state="normal")
    elif selected_index == 2:
        Real2.configure(state="normal")
        Img2.configure(state="normal")
    elif selected_index == 3:
        Real3.configure(state="normal")
        Img3.configure(state="normal")
        
        
def impedance_admittance(Z, Z0):
    """
    Calculate normalized admittance (Yn) from impedance (Z)
    Yn = 1 / Zn, where Zn = Z / Z0
    """
    Zn = Z / Z0  # Normalize the impedance
    Yn = 1 / Zn  # Compute the normalized admittance
    return Yn

def gamma_impedance(Gamma):
    """
    Calculate normalized impedance (Zn) from reflection coefficient (Gamma).
    Zn = (1 + Gamma) / (1 - Gamma)
    """
    if Gamma == 1:
        raise ValueError("Gamma = 1 results in infinite impedance!")
    Zn = (1 + Gamma) / (1 - Gamma)
    return Zn

def admittance_impedance(Y, Z0):
    """
    Calculate normalized impedance (Zn) from admittance (Y) .
    Yn = Y * Z0
    Zn = 1 / Yn
    """
    Yn = Y * Z0  # Compute normalized admittance
    Zn = 1 / Yn  # Compute normalized impedance
    return Zn



def image_declaration():
    SC_PC = "E:/JOB HUNT/2025/Impedance_matching_App/Images/SC_PC1.jpg"
    SC_PL = "E:/JOB HUNT/2025/Impedance_matching_App/Images/SC_PL1.jpg"
    SL_PC = "E:/JOB HUNT/2025/Impedance_matching_App/Images/SL_PC1.jpg"
    SL_PL = "E:/JOB HUNT/2025/Impedance_matching_App/Images/SL_PL1.jpg"
    PC_SC = "E:/JOB HUNT/2025/Impedance_matching_App/Images/PC_SC1.jpg"
    PL_SC = "E:/JOB HUNT/2025/Impedance_matching_App/Images/PL_SC1.jpg"
    PC_SL = "E:/JOB HUNT/2025/Impedance_matching_App/Images/PC_SL1.jpg"
    PL_SL = "E:/JOB HUNT/2025/Impedance_matching_App/Images/PL_SL1.jpg"

    SC_PC = "E:/JOB HUNT/2025/Impedance_matching_App/Images/SC_PC1.jpg"
    scpc_image = customtkinter.CTkImage(light_image=Image.open(SC_PC), dark_image=Image.open(SC_PC), size=(100, 100))
    image_label1 = customtkinter.CTkLabel(app, image=scpc_image, text="")  # display image with a CTkLabel
    

    scpl_image = customtkinter.CTkImage(light_image=Image.open(SC_PL), dark_image=Image.open(SC_PL), size=(100, 100))
    image_label2 = customtkinter.CTkLabel(app, image=scpl_image, text="")  # display image with a CTkLabel
    

    slpc_image = customtkinter.CTkImage(light_image=Image.open(SL_PC), dark_image=Image.open(SL_PC), size=(100, 100))
    image_label3 = customtkinter.CTkLabel(app, image=slpc_image, text="")  # display image with a CTkLabel


    slpl_image = customtkinter.CTkImage(light_image=Image.open(SL_PL), dark_image=Image.open(SL_PL), size=(100, 100))
    image_label4 = customtkinter.CTkLabel(app, image=slpl_image, text="")  # display image with a CTkLabel
    

    pcsc_image = customtkinter.CTkImage(light_image=Image.open(PC_SC), dark_image=Image.open(PC_SC), size=(100, 100))
    

    plsc_image = customtkinter.CTkImage(light_image=Image.open(PL_SC), dark_image=Image.open(PL_SC), size=(100, 100))
    image_label6 = customtkinter.CTkLabel(app, image=plsc_image, text="")  # display image with a CTkLabel
    image_label5 = customtkinter.CTkLabel(app, image=pcsc_image, text="")  # display image with a CTkLabel
   

    pcsl_image = customtkinter.CTkImage(light_image=Image.open(PC_SL), dark_image=Image.open(PC_SL), size=(100, 100))
    image_label7 = customtkinter.CTkLabel(app, image=pcsl_image, text="")  # display image with a CTkLabel
    
    plsl_image = customtkinter.CTkImage(light_image=Image.open(PL_SL), dark_image=Image.open(PL_SL), size=(100, 100))
    image_label8 = customtkinter.CTkLabel(app, image=plsl_image, text="")  # display image with a CTkLabel
   





def button_event():
    print(f"button pressed: {ZZ.get()}")
    Zi = complex(float(Real1.get()), float(Img1.get()))
    Zz = float(ZZ.get())
    Za = impedance_admittance(Zi, Zz)
    Zta = Za
    Zti = Zi
    Lx1, Cx1, Lx2, Cx2, Lx3, Cx3, Lx4, Cx4, Cy1, Ly2, Cy3, Ly4  = calculate_first_element(Zi, Zti, Za,Zta, float(Freq.get()))
    circuit = circuit_assembling(Cx1, Lx1, Cx2, Lx2, Cx3, Lx3, Cx4, Lx4)
    results = result_assembling(circuit, Cy1, Cx1, Ly2, Lx1, Cx2, Lx2, Cy3, Cx3, Ly4, Lx3, Cx4, Lx4)
    textBox1 = customtkinter.CTkLabel(app, width=70, height=30, text="")
    textBox1.grid(row=12, column=2, padx=5, pady=10)
    textBox2 = customtkinter.CTkLabel(app, width=70, height=30, text="")
    textBox2.grid(row=12, column=3, padx=5, pady=10)
    textBox3 = customtkinter.CTkLabel(app, width=70, height=30, text="")
    textBox3.grid(row=12, column=4, padx=5, pady=10)
    textBox4 = customtkinter.CTkLabel(app, width=70, height=30, text="")
    textBox4.grid(row=12, column=5, padx=5, pady=10)
    #image_declaration()
    for i, result in enumerate(results):
        if result.type == "SC_PC":
            textBox1.configure(text= result.elementText1 + "\n" +  result.elementText2)
            SC_PC = "E:/JOB HUNT/2025/Impedance_matching_App/Images/SC_PC1.jpg"
            scpc_image = customtkinter.CTkImage(light_image=Image.open(SC_PC), dark_image=Image.open(SC_PC), size=(200, 200))
            image_label1 = customtkinter.CTkLabel(app, image=scpc_image, text="")  # display image with a CTkLabel
            image_label1.grid(row=13, column=2, padx=5, pady=10)
            
        elif result.type == "SC_PL":
            textBox2.configure(text= result.elementText1 + "\n" +  result.elementText2)
            SC_PL = "E:/JOB HUNT/2025/Impedance_matching_App/Images/SC_PL1.jpg"
            scpl_image = customtkinter.CTkImage(light_image=Image.open(SC_PL), dark_image=Image.open(SC_PL), size=(200, 200))
            image_label2 = customtkinter.CTkLabel(app, image=scpl_image, text="")  # display image with a CTkLabel
            image_label2.grid(row=13, column=3, padx=5, pady=10)
            
        elif result.type == "SL_PC":
            textBox3.configure(text= result.elementText1 + "\n" + result.elementText2)
            SL_PC = "E:/JOB HUNT/2025/Impedance_matching_App/Images/SL_PC1.jpg"
            slpc_image = customtkinter.CTkImage(light_image=Image.open(SL_PC), dark_image=Image.open(SL_PC), size=(200, 200))
            image_label3 = customtkinter.CTkLabel(app, image=slpc_image, text="")  # display image with a CTkLabel
            image_label3.grid(row=13, column=4, padx=5, pady=10)
            
        elif result.type == "SL_PL":
            textBox4.configure(text= result.elementText1 + "\n" + result.elementText2)
            SL_PL = "E:/JOB HUNT/2025/Impedance_matching_App/Images/SL_PL1.jpg"
            slpl_image = customtkinter.CTkImage(light_image=Image.open(SL_PL), dark_image=Image.open(SL_PL), size=(200, 200))
            image_label4 = customtkinter.CTkLabel(app, image=slpl_image, text="")  # display image with a CTkLabel
            image_label4.grid(row=13, column=5, padx=5, pady=10)
            
        elif result.type == "PC_SC":
            textBox4.configure(text= result.elementText1 + "\n" + result.elementText2)
            #image_label5.grid(row=12, column=10, padx=5, pady=10)
            PC_SC = "E:/JOB HUNT/2025/Impedance_matching_App/Images/PC_SC1.jpg"
            pcsc_image = customtkinter.CTkImage(light_image=Image.open(PC_SC), dark_image=Image.open(PC_SC), size=(200, 200))
            image_label5 = customtkinter.CTkLabel(app, image=pcsc_image, text="")  # display image with a CTkLabel
            image_label5.grid(row=13, column=5, padx=5, pady=10)
            
        elif result.type == "PL_SC":
            textBox3.configure(text= result.elementText1 + "\n" + result.elementText2)
            PL_SC = "E:/JOB HUNT/2025/Impedance_matching_App/Images/PL_SC1.jpg"
            plsc_image = customtkinter.CTkImage(light_image=Image.open(PL_SC), dark_image=Image.open(PL_SC), size=(200, 200))
            image_label6 = customtkinter.CTkLabel(app, image=plsc_image, text="")  # display image with a CTkLabel
            image_label6.grid(row=13, column=4, padx=5, pady=10)
            
        elif result.type == "PC_SL":
            textBox2.configure(text= result.elementText1 + "\n" + result.elementText2)
            PC_SL = "E:/JOB HUNT/2025/Impedance_matching_App/Images/PC_SL1.jpg"
            pcsl_image = customtkinter.CTkImage(light_image=Image.open(PC_SL), dark_image=Image.open(PC_SL), size=(200, 200))
            image_label7 = customtkinter.CTkLabel(app, image=pcsl_image, text="")  # display image with a CTkLabel
            image_label7.grid(row=13, column=3, padx=5, pady=10)
            
        elif result.type == "PL_SL":
            textBox1.configure(text= result.elementText1 + "\n" + result.elementText2)
            PL_SL = "E:/JOB HUNT/2025/Impedance_matching_App/Images/PL_SL1.jpg"
            plsl_image = customtkinter.CTkImage(light_image=Image.open(PL_SL), dark_image=Image.open(PL_SL), size=(200, 200))
            image_label8 = customtkinter.CTkLabel(app, image=plsl_image, text="")  # display image with a CTkLabel
            image_label8.grid(row=13, column=2, padx=5, pady=10)
           
            
        
            
        
    
        
        
    # print(f"Inductance from Impedance Lx1 : {Lx1*1e9:.3f}nH")
    # print(f"Capacitance from Impedance Cx1 : {Cx1*1e12:.3f}pF")
    # print(f"Inductance from Admittance Lx2: {Lx2*1e9:.3f}nH")
    # print(f"Capacitance from Admittance Cx2: {Cx2*1e12:.3f}pF")
    # print(f"Inductance from Impedance Lx3 : {Lx3*1e9:.3f}nH")
    # print(f"Capacitance from Impedance Cx3: {Cx3*1e12:.3f}pF")
    # print(f"Inductance from Admittance Lx4: {Lx4*1e9:.3f}nH")
    # print(f"Capacitance from Admittance Cx4: {Cx4*1e12:.3f}pF")
    # print(f"Capacitance from Impedance Cy1: {Cy1*1e12:.3f}pF")
    # print(f"Inductance from Impedance Ly2: {Ly2*1e9:.3f}nH")
    # print(f"Capacitance from Admittance Cy3: {Cy3*1e12:.3f}pF")
    # print(f"Inductance from Admittance Ly4: {Ly4*1e9:.3f}nH")
    
    
    
    



# System Settings 
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("1440x1440")
app.title("Impedance Matching Calculator By ELLA")

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Impedance Matching Elements Calculator", font=("Arial", 40), justify="center")
title.grid(row=1, column=8,padx=10, pady=10)

radio_buttons = []
all_entries = []

# Radio Buttons, Entry Boxes

radioImp = tkinter.IntVar(value=1)

txtImpReal = customtkinter.CTkLabel(app, text="Real", font=("Arial", 15))
txtImpReal.grid(row=3, column=4, padx=5, pady=10)
Real1 = customtkinter.CTkEntry(app, width=70, height=30)
Real1.grid(row=3, column= 5, padx=5, pady=10)

txtImpImg = customtkinter.CTkLabel(app, text="Imaginary", font=("Arial", 15))
txtImpImg.grid(row=3, column=6, padx=5, pady=10)
Img1 = customtkinter.CTkEntry(app, width=70, height=30)
Img1.grid(row=3, column=7, padx=5, pady=10)

txtAdmReal = customtkinter.CTkLabel(app, text="Real", font=("Arial", 15))
txtAdmReal.grid(row=4, column=4, padx=5, pady=10)
Real2 = customtkinter.CTkEntry(app, width=70, height=30, state="disabled")
Real2.grid(row=4, column= 5, padx=5, pady=10)

txtAdmImg = customtkinter.CTkLabel(app, text="Imaginary", font=("Arial", 15))
txtAdmImg.grid(row=4, column=6, padx=5, pady=10)
Img2 = customtkinter.CTkEntry(app, width=70, height=30, state="disabled")
Img2.grid(row=4, column=7, padx=5, pady=10)

txtRCoefReal = customtkinter.CTkLabel(app, text="Real", font=("Arial", 15))
txtRCoefReal.grid(row=5, column=4, padx=5, pady=10)
Real3 = customtkinter.CTkEntry(app, width=70, height=30, state="disabled")
Real3.grid(row=5, column= 5, padx=5, pady=10)

txtRCoefImg = customtkinter.CTkLabel(app, text="Imaginary", font=("Arial", 15))
txtRCoefImg.grid(row=5, column=6, padx=5, pady=10)
Img3 = customtkinter.CTkEntry(app, width=70, height=30, state="disabled")
Img3.grid(row=5, column=7, padx=5, pady=10)


# Impedance 

ImpRB = customtkinter.CTkRadioButton(app, value=1,text="Impedance", command=lambda: radiobutton_event(1), variable= radioImp,  font=("Arial", 15))
ImpRB.grid(row=3, column=2, pady=10)
radio_buttons.append(ImpRB)



# Admittance
AdmRB = customtkinter.CTkRadioButton(app, value=2,text="Admittance", command=lambda: radiobutton_event(2), variable= radioImp,  font=("Arial", 15))
AdmRB.grid(row=4, column=2,pady=10)
radio_buttons.append(AdmRB)


# Reflexion coefficient
rCoefRB = customtkinter.CTkRadioButton(app, text="Reflexion Coefficient", command=lambda: radiobutton_event(3), variable= radioImp, value=3, font=("Arial", 15))
rCoefRB.grid(row=5, column=2,pady=10)
radio_buttons.append(rCoefRB)


# Frequency
txtFreq = customtkinter.CTkLabel(app, text="Frequency", font=("Arial", 15))
txtFreq.grid(row=6, column=2, padx=5, pady=10)
Freq = customtkinter.CTkEntry(app, width=70, height=30)
Freq.grid(row=6, column= 4, padx=5, pady=10)

# Z0
txtZZ = customtkinter.CTkLabel(app, text="Z0", font=("Arial", 15))
txtZZ.grid(row=7, column=2, padx=5, pady=10)
ZZ = customtkinter.CTkEntry(app, width=70, height=30)
ZZ.grid(row=7, column= 4, padx=5, pady=10)

# Calculation button
btnCalculate = customtkinter.CTkButton(app, text="Calculate", command=button_event, font=("Arial", 15))
btnCalculate.grid(row=9, column=4, padx=5, pady=10)





# Run app
app.mainloop()
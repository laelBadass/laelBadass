import cmath  # For complex number operations

def calculate_normalized_admittance(Z, Z0):
    """
    Calculate normalized admittance (Yn) from impedance (Z) for a given characteristic impedance (Z0).
    
    Yn = 1 / Zn, where Zn = Z / Z0
    """
    Zn = Z / Z0  # Normalize the impedance
    Yn = 1 / Zn  # Compute the normalized admittance
    return Yn

def calculate_normalized_impedance_from_Gamma(Gamma):
    """
    Calculate normalized impedance (Zn) from reflection coefficient (Gamma).
    
    Zn = (1 + Gamma) / (1 - Gamma)
    """
    if Gamma == 1:
        raise ValueError("Gamma = 1 results in infinite impedance!")
    Zn = (1 + Gamma) / (1 - Gamma)
    return Zn

def calculate_normalized_impedance_from_admittance(Y, Z0):
    """
    Calculate normalized impedance (Zn) from admittance (Y) for a given characteristic impedance (Z0).
    
    Yn = Y * Z0
    Zn = 1 / Yn
    """
    Yn = Y * Z0  # Compute normalized admittance
    Zn = 1 / Yn  # Compute normalized impedance
    return Zn

# Example usage:
Z = complex(25, -25)  # Example impedance (30 + j40 Ohm)
Z0 = 50  # Characteristic impedance (Ohm)
Gamma = complex(0.3, 0.4)  # Example reflection coefficient
Y = complex(1, 1)  # Example admittance (Siemens)

# Calculating normalized admittance from impedance
Yn = calculate_normalized_admittance(Z, Z0)
print(f"Normalized Admittance: {Yn:.4f}")

# Calculating normalized impedance from reflection coefficient
Zn_from_Gamma = calculate_normalized_impedance_from_Gamma(Gamma)
print(f"Normalized Impedance from Reflection Coefficient: {Zn_from_Gamma:.4f}")

# Calculating normalized impedance from admittance
Zn_from_Y = calculate_normalized_impedance_from_admittance(Y, Z0)
print(f"Normalized Impedance from Admittance: {Zn_from_Y:.4f}")

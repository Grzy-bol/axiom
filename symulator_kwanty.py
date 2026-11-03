import random
import sys
import subprocess
import site

def ensure_installed(package_name):
    try:

        __import__(package_name)
    except ImportError:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            package_name, 
            "--break-system-packages"
        ])

ensure_installed("numpy")

import numpy as np

print(np.__version__)

stan_0 = np.array([1, 0], dtype=complex)
stan_1 = np.array([0, 1], dtype=complex)


# Bramka X 
X = np.array([[0, 1], 
              [1, 0]], dtype=complex)

# Bramka Z
Z = np.array([[1,  0], 
              [0, -1]], dtype=complex)

# Bramka H
H = (1 / np.sqrt(2)) * np.array([[1,  1], 
                                 [1, -1]], dtype=complex)

# Bramka Ry
def Ry(theta):
    return np.array([
        [np.cos(theta/2), -np.sin(theta/2)],
        [np.sin(theta/2),  np.cos(theta/2)]
    ], dtype=complex)

# CNOT
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

def pomiar(stan):
   
    prawdopodobienstwa = np.abs(stan) ** 2
    
    
    wynik = random.choices(range(len(stan)), weights=prawdopodobienstwa)[0]
    
    return wynik


stan = np.array([1, 0], dtype=complex)


stan = np.dot(H, stan)


stan = np.dot(H, stan)

print("Stan po H*H:", stan)  

I = np.eye(2, dtype=complex) # Macierz jednostkowa

# 1. Stan początkowy |00> (wektor 4-elementowy)
stan_2q = np.kron(np.array([1, 0], dtype=complex), np.array([1, 0], dtype=complex))

# 2. Bramka H na pierwszy kubit: (H (x) I)
H_krokowo = np.kron(H, I)
stan_2q = np.dot(H_krokowo, stan_2q)

# 3. Bramka CNOT
stan_2q = np.dot(CNOT, stan_2q)

print("Stan Bella (|Φ+>):", stan_2q) 

# 4. Test pomiarów (powinno wychodzić w ~50% przypadków '0' (czyli 00) i w ~50% '3' (czyli 11))
wyniki = [pomiar(stan_2q) for _ in range(1000)]
print("Liczba wyników 00 :", wyniki.count(0))
print("Liczba wyników 11 :", wyniki.count(3))
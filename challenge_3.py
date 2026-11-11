import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
# 4 kubity i 4 warstwy
num_qubits = 4
L = 4

#parametry modelu
x = ParameterVector("x", num_qubits)  
th = ParameterVector("th", num_qubits * L)     

qc = QuantumCircuit(num_qubits)

#encoding
for i in range(num_qubits):
    qc.ry(x[i], i)

#ansatz
param_idx = 0
for l in range(L):
    #rotacje
    for i in range(num_qubits):
        qc.ry(th[param_idx], i)
        param_idx += 1
    # Entanglement
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)

#pomiar Z na pierwszym kubicie
observable = SparsePauliOp.from_sparse_list([("Z", [0], 1.0)], num_qubits=num_qubits)
estimator = StatevectorEstimator()

#forward pass
def f(x_val, th_val):
    bound_qc = qc.assign_parameters({**dict(zip(x, x_val)), **dict(zip(th, th_val))})
    job = estimator.run([(bound_qc, observable)])
    return float(job.result()[0].data.evs)

#backward pass (wyliczanie gradientu)
def get_gradients(x_val, th_val):
    grads = np.zeros(len(th_val))
    for j in range(len(th_val)):
        plus = th_val.copy()
        minus = th_val.copy()
        plus[j] += np.pi / 2
        minus[j] -= np.pi / 2
        grads[j] = (f(x_val, plus) - f(x_val, minus)) / 2.0
    return grads

#EKSPERYMENT!!!
np.random.seed(42)
num_samples = 50
layer1_grads = []
layer4_grads = []

for _ in range(num_samples):
    x_sample = np.random.uniform(0, np.pi, num_qubits)
    th_sample = np.random.uniform(-np.pi, np.pi, num_qubits * L)
    
    g = get_gradients(x_sample, th_sample)

#warstwa 1, tuż przy początku obwodu
layer1_grads.append(np.mean(np.abs(g[0:4])))
#warstwa 4, na samym końcu obwodu
layer4_grads.append(np.mean(np.abs(g[12:16])))

#średnia z wyników
avg_layer1 = np.mean(layer1_grads)
avg_layer4 = np.mean(layer4_grads)
drop_percentage = (1 - avg_layer1 / avg_layer4) * 100

print(f"średni gradient w warstwie 1 (początek): {avg_layer1:.5f}")
print(f"średni gradient w warstwie 4 (koniec)  : {avg_layer4:.5f}")
print(f"tłumienie gradientu w warstwie 1 względem warstwy 4: {drop_percentage:.2f}%")

#wykres w matplotlibie
plt.figure(figsize=(7, 5))
plt.bar(["Warstwa 1 (Początek)", "Warstwa 4 (Koniec)"], [avg_layer1, avg_layer4], color=["#E6D92B", "#2e65cc"])
plt.ylabel("Średni moduł gradientu |∂f/∂θ|")
plt.title("Zjawisko spadku gradientu w głębi obwodu")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("gradient_shielding.png")
plt.show()

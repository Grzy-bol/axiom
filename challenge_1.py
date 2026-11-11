#Duży i rozbudowany model osiągnie zjawisko overfittingu na tak małym datasetcie jakim jest heart_disease. Accuracy na danych treningowych będzie bliskie 100%, 
#jednak na zbiorze testowym model poradzi sobie dużo gorzej. Mniejszy i łatwiejszy,ale za to bardziej sprecyzowany model powinien poradzić sobie lepiej na tak małym datasetcie.

import sys
import subprocess
import seaborn as sb
import pandas as pd
import matplotlib
import matplotlib.pyplot as mpl
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split, GridSearchCV
#Pobieranie i wczytywanie datasetu
df = pd.read_csv('heart.csv')
df = df.drop_duplicates()
x = df.drop('target', axis=1) #x to wszystkie dane w tabeli
y = df['target'] #y to ich odpowiedzi

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
# skalowanie danych
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

#podstawienie datasetu do dużego, głębokiego modelu 
nn_model = MLPClassifier(
    hidden_layer_sizes=(256, 128, 64), 
    max_iter=1000, 
    random_state=42,
    learning_rate_init=0.01
)
nn_model.fit(x_train_scaled, y_train)

#oraz do małego ale sprecyzowanego modelu, gdzie dopasowujemy hiperparametr
param_grid = {'C': [0.1, 0.5, 1.0, 5.0, 10.0, 50.0]}

grid_search = GridSearchCV(
    LogisticRegression(random_state=42), 
    param_grid, 
    cv=5, 
    scoring='accuracy'
)
grid_search.fit(x_train_scaled, y_train)
logreg_mod = grid_search.best_estimator_

#odpowiedzi jak działają modele na tym datasetcie
nn_train_acc = accuracy_score(y_train, nn_model.predict(x_train_scaled))
nn_test_acc = accuracy_score(y_test, nn_model.predict(x_test_scaled))

lr_train_acc = accuracy_score(y_train, logreg_mod.predict(x_train_scaled))
lr_test_acc = accuracy_score(y_test, logreg_mod.predict(x_test_scaled))

print(f"Sieć Neuronowa      -> Train Acc: {nn_train_acc:.4f} | Test Acc: {nn_test_acc:.4f}")
print(f"Regresja Logistyczna -> Train Acc: {lr_train_acc:.4f} | Test Acc: {lr_test_acc:.4f}")

#Porównanie graficzne c:


results = pd.DataFrame({
    'Model': ['Sieć Neuronowa (MLP)', 'Sieć Neuronowa (MLP)', 'Regresja Logistyczna', 'Regresja Logistyczna'],
    'Zbiór': ['Treningowy', 'Testowy', 'Treningowy', 'Testowy'],
    'Accuracy': [nn_train_acc, nn_test_acc, lr_train_acc, lr_test_acc]
})

mpl.figure(figsize=(9, 5))
sb.barplot(data=results, x='Model', y='Accuracy', hue='Zbiór', palette='Set1')
mpl.title('Porównanie przeuczenia (Overfitting): Sieć Neuronowa vs Regresja Logistyczna')
mpl.ylim(0.5, 1.05)
mpl.axhline(0.5, color='gray', linestyle='--')


for p in mpl.gca().patches:
    height = p.get_height()
    if height > 0:
        mpl.gca().annotate(f'{height:.2%}', 
                            (p.get_x() + p.get_width() / 2., height), 
                            ha='center', va='bottom', fontsize=10, xytext=(0, 3), 
                            textcoords='offset points')

mpl.show()
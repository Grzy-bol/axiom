# ===Hipoteza===
W głębokim obwodzie (L=4) średnia wartość gradientu (Parameter-Shift) dla parametrów z pierwszej warstwy będzie dużo mniejsza niż dla parametrów z czwartej warstwy.

# ===Uzasadnienie=== 
Bramki CNOT w warstwach pośrednich zaplątują kubity i rozpraszają informację o zmianie kąta z 1. warstwy po całej przestrzeni stanów.
Ponieważ pomiar wykonywany jest tylko na jednym kubicie (Z0), wpływ pierwszych parametrów na wynik wyjściowy 
ulega drastycznemu tłumieniu (ślad częściowy), dając bardzo małe różnice wartości w regule Parameter-Shift.

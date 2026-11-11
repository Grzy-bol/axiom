# ===Hipoteza===
W głębokim obwodzie (L=4) średnia wartość gradientu (Parameter-Shift) dla parametrów z pierwszej warstwy będzie dużo mniejsza niż dla parametrów z czwartej warstwy.

# ===Uzasadnienie=== 
Bramki CNOT w warstwach pośrednich zaplątują kubity i rozpraszają informację o zmianie kąta z 1. warstwy po całej przestrzeni stanów.
Ponieważ pomiar wykonywany jest tylko na jednym kubicie (Z0), wpływ pierwszych parametrów na wynik wyjściowy 
ulega drastycznemu tłumieniu (ślad częściowy), dając bardzo małe różnice wartości w regule Parameter-Shift.



# ===Wyniki eksperymentu===
Eksperyment przeprowadzony na 50 próbkach wygenerował następujące metryki:
* Średni moduł gradientu w Warstwie 1 (Początek) : 0.21647
* Średni moduł gradientu w Warstwie 4 (Koniec)   : 0.03074
* Wskaźnik tłumienia: -604.26%

Plik z wykresem: `gradient_shielding.png`

# ===Weryfikacja hipotezy===
Hipoteza została obalona z dwóch głownych powodów:
-Przezroczystość bramki CNOT dla kubitu kontrolnego w bazie Z: 
W topologii Linear użyto bramek CX(0->1), CX(1->2), CX(2->3). Kubit 0 działa jako CONTROL. W bazie obserwacji Z zachodzi relacja algebraiczną CX * (Z ⊗ I) * CX = Z ⊗ I.
Oznacza to, że z punktu widzenia pomiaru Z0 bramki CNOT nie rozpraszają stanu kubitu 0, pozwalając sygnałowi z parametru th[0] (Warstwa 1) przejść przez obwód bez tłumienia.

-Rozcieńczenie średniej w Warstwie 4 ("martwe parametry"):
Mierząc wyłącznie pierwszy kubit (Z0), parametry na kubitach 1, 2 i 3 w ostatniej warstwie (th[13], th[14], th[15]) mają gradient analitycznie równy DOKŁADNIE 0.0
(nie mają fizycznego wpływu na Z0). Uśrednienie ich z jedynym aktywnym parametrem (th[12]) zaniżyło średnią warstwy 4 aż o 75%.

# ===Pytanie i odpowiedź===

Co by się zmieniło, gdybym zamiast pojedynczego Z0 zamienił je na observable parzystości Z0*Z1*Z2*Z3?
Wtedy wszystkie 4 warstwy brałyby aktywny udział w pomiarach a bramki CNOT realnie wymieszałyby fazy wszystkich kubitów.
No i w takim przypadku wyszłoby założenie z hipotezy, ponieważ gradient 4 warstwy mocno by wzrósł, a przez to wskaźnik tłumienia byłby dodatni

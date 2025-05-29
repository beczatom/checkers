# ♟️ Dáma

Projekt je implementáciou významnej tradičnej hry – dámy.
Poskytuje priestor pre hru medzi ľudmi, ale aj s počítačom. 👥💻
Štýl hry počítača je plne nastaviteľný 
a navyše je ho možné trénovať pomocou metód genetického programovania.  🧪

## ⚙️ Funkcie

- 0️⃣1️⃣ Šachovnica je implementovaná bitovým poľom. 
Takisto celé generovanie ťahov sú bitové operácie. 
Vďaka tomu vie byť hra rýchla a následne trénovanie tiež. 


- 🧬 Pre trénovanie je použitý algoritmus genetického trénovania.
Keďže som chcel nechať populáciu nech si sama nájde ideálne koeficienty,
nepoužívam žiadne externé enginy 
(v šachu napr. Stockfish 🚫🐟, v dáme sa však ajtak len ťažko nachádzajú).
Algoritmus je teda bez evaluačnej funkcie a na porovnávanie jednotlivých
hráčov sa používa výhradne výsledok ich vzájomnej hry.


- 💻 🖥️ Netradične, oproti bežným webovým stránkam, poskytuje implementácia
aj pohľad na hru počítača proti inému.
Navyše s možnosťou si zvoliť vlastné koeficienty, a teda štýl hry.


- ❌ Projekt **neslúži** ako revolúcia v AI herných agentoch. 🤖
Takisto autor si plne uvedomuje, že rekurentné neurónové siete 🧠
by vedeli robiť lepšie ťahy. 
Avšak projekt predstavuje netradičnejší pohľad na hľadanie najlepších ťahov.

## 🔍 Používanie

### 📝 Prerekvizity

- 🐍 Python 3.13


- 📦 Potrebné balíčky (viď. `requirements.txt`)

### 📥 Inštalácia

Inštalácia potrebných balíčkov:

```bash
  pip install -r requirements.txt
```

### 🚀 Spustenie

V pracovnom adresári `semestral` je treba pre:

- 🎨 GUI spustiť


```bash
  python -m app.utils.main
```


- 🔬 spustenie genetického algoritmu s nastavením v `app/genetic/constants.py`
na riadkoch 5 - 9 spustiť


```bash
  python -m app.genetic.genetic
```


- ⚠️ genetický algoritmus je takisto možné spustiť z GUI aplikácie, 
každopádne to bude trvať dlhšie (výpočet síce prebieha na viacerých procesoch
ale tie volá vlákno, ktoré sú v Pythone pomalé).


- ✅ Testy codestyle a testy funkcionality

```bash
  pytest
```
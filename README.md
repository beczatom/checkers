# ♟️ Checkers

This is a semestral project for **Programming in Python** (BI-PYT).

This project is an implementation of the traditional game of checkers (draughts).
It allows playing human vs. human as well as human vs. computer. 👥💻
The computer's play style is fully customizable 
and can be trained using **genetic algorithm**. 🧪

## ⚙️ Features

- 0️⃣1️⃣ The board is implemented using bitboards. 
Move generation is also entirely based on bitwise operations. 
This ensures high performance for both gameplay and training. 


- 🧬 Training utilizes a genetic algorithm.
To allow the population to discover optimal coefficients on its own,
no external engines are used 
(unlike chess with e.g. Stockfish 🚫🐟, which are hard to find for checkers anyway).
The algorithm operates without a hand-crafted evaluation function;
player evaluation and comparison rely solely on the outcome of their head-to-head matches.


- 💻 🖥️ Unlike typical web implementations, this project also provides 
a view for computer vs. computer matches,
with the option to choose custom coefficients and play styles.


- ❌ This project is **not** intended as a revolution in AI game agents. 🤖
The author is fully aware that other ML models 🧠 
could achieve much better moves. 
However, the project presents a non-traditional perspective on discovering the best moves.

## 🔍 Usage

### 📝 Prerequisites

- 🐍 Python 3.13


- 📦 Required packages (see `requirements.txt`)

### 📥 Installation

Install the required packages:

```bash
  pip install -r requirements.txt
```

### 🚀 Running the Project

From the `semestral` working directory:

- 🎨 Launch GUI


```bash
  python -m app.utils.main
```


- 🔬 Run genetic algorithm with configuration in `app/genetic/constants.py`
on lines 5–9:


```bash
  python -m app.genetic.genetic
```


- ⚠️ The genetic algorithm can also be launched from the GUI application; 
however, it will take longer (computation runs on multiple processes,
but they are managed by a thread, which has overhead in Python).


- ✅ Code style and functionality tests

```bash
  pytest
```
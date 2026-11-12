"""
Analyse expérimentale de la complexité de l'algorithme force brute.
"""

import big_o
from bruteforce import force_brute


def generer_actions(n):
    """Crée n actions fictives (nom, coût, profit)."""
    return [
        (f"Action-{i}", 10 + i, 1 + i * 0.1)
        for i in range(n)
    ]


def main():

    meilleur, _ = big_o.big_o(
        force_brute,
        generer_actions,
        min_n=5,
        max_n=18,
        n_measures=10,
        n_repeats=1,
    )

    print(f"Complexité temporelle estimée : {meilleur}")


if __name__ == "__main__":
    main()
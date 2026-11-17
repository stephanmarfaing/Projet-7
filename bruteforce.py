"""
Algorithme de force brute

Le programme lit le fichier CSV (nom, coût, bénéfice en %), teste toutes les
combinaisons possibles d'actions (chacune achetée au plus une fois, sans
fraction) dont le coût total ne dépasse pas le budget de 500€, puis affiche celle qui
maximise le profit après 2 ans.
"""

import csv
import sys
import time
from itertools import combinations

BUDGET_MAX = 500
FICHIER_PAR_DEFAUT = "Liste_d_actions_-_P7_Python_-_Feuille_1.csv"


def lire_actions(chemin):
    """Lit le CSV et retourne une liste de tuples (nom, coût, profit en euros).

    Le bénéfice du CSV est un pourcentage du coût : profit = coût * pourcentage / 100.
    """
    actions = []  # Création d'une liste d'actions

    try:
        with open(chemin, newline="", encoding="utf-8-sig") as fichier:  # Essaie l'UTF-8
            lignes = fichier.read().splitlines()
    except UnicodeDecodeError:
        with open(chemin, newline="", encoding="cp1252") as fichier:  # Sinon, format Windows (Excel)
            lignes = fichier.read().splitlines()

    lecteur = csv.reader(lignes)  # Crée un lecteur permettant de parcourir le CSV ligne par ligne
    next(lecteur)  # ignore l'en-tête

    for ligne in lecteur:
            if len(ligne) < 3:  # Si moins de 3 colonnes, on traite la suivante
                continue

            nom = ligne[0].strip()  # .strip enlève les espaces en début et fin de texte
            cout = float(ligne[1])  # Converti la 2 ème colonne en float
            pourcentage = float(
                ligne[2].strip().replace("%", "")
            )  # On prend le %, enlève les espaces et le %
            # puis transforme en float

            profit = cout * pourcentage / 100  # transforme le pourcentage en coût

            actions.append((nom, cout, profit))  # On crée un tuple nom, coût et profit

    return actions  # renvoie la liste une fois terminée


def force_brute(actions, budget=BUDGET_MAX):
    """Teste toutes les combinaisons possibles et retourne la meilleure.

    Retourne (meilleure_combinaison, cout_total, profit_total).
    """
    meilleure_combinaison = ()
    meilleur_profit = 0.0
    meilleur_cout = 0.0

    for taille in range(1, len(actions) + 1):
        for combinaison in combinations(actions, taille):

            cout_total = sum(action[1] for action in combinaison)

            if cout_total > budget:
                continue  # Si >500€, on ne prend pas

            profit_total = sum(action[2] for action in combinaison)

            if profit_total > meilleur_profit:
                meilleur_profit = profit_total
                meilleur_cout = cout_total

                meilleure_combinaison = combinaison
                # Si la nouvelle combinaison est plus rentable, elle prend
                # la place de l'ancienne plus rentable

    return meilleure_combinaison, meilleur_cout, meilleur_profit


def afficher_resultat(combinaison, cout_total, profit_total):
    print("Meilleur investissement :")

    for nom, cout, profit in combinaison:
        print(f"  - {nom} : coût {cout:.2f} € | profit {profit:.2f} €")

    print(f"\nNombre d'actions : {len(combinaison)}")
    print(f"Coût total : {cout_total:.2f} €")
    print(f"Profit total après 2 ans : {profit_total:.2f} €")


def main():
    chemin = sys.argv[1] if len(sys.argv) > 1 else FICHIER_PAR_DEFAUT

    actions = lire_actions(chemin)

    debut = time.perf_counter()

    combinaison, cout, profit = force_brute(actions)

    duree = time.perf_counter() - debut

    afficher_resultat(combinaison, cout, profit)

    print(f"Temps d'exécution : {duree:.2f} s")


if __name__ == "__main__":
    main()
import csv
import sys
import time

BUDGET_MAX = 500


def lire_actions(chemin):
    """
    Lit le fichier CSV et retourne une liste de dictionnaires :
    {
        "nom": str,
        "cout": int (centimes),
        "profit": int (centimes)
    }
    """

    actions = [] # Création d'une liste d'actions

    try:
        with open(chemin, newline="", encoding="utf-8-sig") as fichier:  # Essaie l'UTF-8
            lignes = fichier.read().splitlines()
    except UnicodeDecodeError:
        with open(chemin, newline="", encoding="cp1252") as fichier:  # Sinon, format Windows (Excel)
            lignes = fichier.read().splitlines()

    lecteur = csv.reader(lignes)  # Crée un lecteur permettant de parcourir le CSV ligne par ligne
    next(lecteur)  # ignore l'en-tête

    for ligne in lecteur:

            if len(ligne) < 3: # Si moins de 3 colonnes, on traite la suivante
                continue

            nom = ligne[0].strip() # Récupère le nom de l'action et supprime les espaces inutiles

            try:
                cout = float(ligne[1]) # Converti la 2 ème colonne en float
                benefice = float(ligne[2].replace("%", "").strip()) # Convertit le coût
                                                                    # et le pourcentage de bénéfice en nombres
            except ValueError:
                continue

            if cout <= 0 or benefice <= 0: # si profit = 0 ou négatif, on ignore
                continue

            profit = cout * benefice / 100 # Calcule le profit réel en euros à partir du pourcentage de bénéfice

            actions.append({ # On crée un dictionnaire contenant le nom, le coût et le profit
                "nom": nom,
                "cout": int(round(cout * 100)),
                "profit": int(round(profit * 100))
            })

    return actions # renvoie la liste une fois terminée


def portefeuille_optimal(actions, budget=BUDGET_MAX):
    """
    Résout le problème du sac à dos 0/1.
    """

    budget_max = budget * 100  # Conversion du budget en centimes
    nb_actions = len(actions) # Récupère le nombre total d'actions disponibles.

    # Matrice de programmation dynamique
    dp = [[0 for _ in range(budget_max + 1)] # Ligne = nombre d'actions considérées.
                                             # Colonne = budget disponible.
          for _ in range(nb_actions + 1)]

    # Remplissage de la matrice
    for i in range(1, nb_actions + 1): # Parcourt les actions une par une.

        cout = actions[i - 1]["cout"] # Récupère le coût de l'action courante.
        profit = actions[i - 1]["profit"] # Récupère son profit.

        for b in range(budget_max + 1): # Parcourt tous les budgets possibles
                                        # de 0 jusqu'à 50 000 centimes.

            # Si l'action peut être achetée avec le budget disponible
            if cout <= b:

                # On conserve le meilleur choix :
                # acheter ou ne pas acheter, on conserve le profit le plus élevé
                dp[i][b] = max(
                    dp[i - 1][b],
                    dp[i - 1][b - cout] + profit
                )

            else:
                # Action trop chère pour ce budget, on garde la solution précédente
                dp[i][b] = dp[i - 1][b]

    # Reconstruction du portefeuille optimal
    portefeuille = []
    b = budget_max

    for i in range(nb_actions, 0, -1):

        # Si la valeur change, l'action a été retenue
        if dp[i][b] != dp[i - 1][b]:

            portefeuille.append(actions[i - 1])

            # On retire son coût du budget restant
            b -= actions[i - 1]["cout"]

    portefeuille.reverse()

    return portefeuille

def afficher_resultats(portefeuille):
    # Calcule le coût total du portefeuille et convertit
    # les centimes en euros
    cout_total = sum(action["cout"] for action in portefeuille) / 100
    # Calcule le profit total et convertit les centimes en euros
    profit_total = sum(action["profit"] for action in portefeuille) / 100
    # Idem pour les profits
    print("\nMeilleure combinaison d'actions :\n")

    for action in portefeuille:
        print(
            f"- {action['nom']} | "
            f"Coût : {action['cout'] / 100:.2f} € | "
            f"Profit : {action['profit'] / 100:.2f} €"
        )

    print("\n------------------------------------")
    print(f"Nombre d'actions : {len(portefeuille)}")
    print(f"Coût total : {cout_total:.2f} €")
    print(f"Profit total après 2 ans : {profit_total:.2f} €")
    print("------------------------------------")


def main():

    fichier = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Liste_d_actions_-_P7_Python_-_Feuille_1.csv"
    )
    # Démarre le chronomètre avant l'exécution
    debut = time.perf_counter()

    actions = lire_actions(fichier)
    portefeuille = portefeuille_optimal(actions)
    # Calcule le temps d'exécution total de l'algorithme
    duree = time.perf_counter() - debut

    afficher_resultats(portefeuille)

    print(f"\nTemps d'exécution : {duree:.6f} seconde(s)")


if __name__ == "__main__":
    main()
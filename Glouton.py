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


def portefeuille_glouton(actions, budget=500):
    """
    Sélection gloutonne basée sur le ratio profit/coût.
    """

    budget_restant = budget * 100  # centimes

    # Trie les actions par rentabilité décroissante
    actions_triees = sorted(
        actions,
        key=lambda action: action["profit"] / action["cout"],
        reverse=True
    )

    portefeuille = []

    for action in actions_triees:

        # Si l'action entre dans le budget restant
        if action["cout"] <= budget_restant:

            portefeuille.append(action)

            budget_restant -= action["cout"]

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
    portefeuille = portefeuille_glouton(actions)
    # Calcule le temps d'exécution total de l'algorithme
    duree = time.perf_counter() - debut

    afficher_resultats(portefeuille)

    print(f"\nTemps d'exécution : {duree:.6f} seconde(s)")


if __name__ == "__main__":
    main()
import logging   # module standard pour écrire des journaux (logs)

from csv_reader import (
    charger_csv,
    CsvException,
    FichierIntrouvableException,
    LigneInvalideException,
    PrixNegatifException,
)

# ===== CONFIGURATION DU LOGGER (facultatif) =====
# Écrit les erreurs dans le fichier erreurs.log, avec la date et l'heure.
# level=ERROR : on n'enregistre que les erreurs (pas les messages d'information).
logging.basicConfig(
    filename="erreurs.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


def main():
    chemin = "articles.csv"

    # ===== GESTION DES ERREURS =====
    # Principe du TP : csv_reader.py SIGNALE les erreurs (exceptions),
    # main.py DÉCIDE quoi afficher à l'utilisateur.
    try:
        articles = charger_csv(chemin)

    # Un except par type d'erreur, avec un message adapté à chacun.
    # logging.error(e) enregistre le détail technique dans erreurs.log.
    except FichierIntrouvableException as e:
        logging.error(e)
        print("Le fichier demandé n'existe pas. Vérifiez le chemin.")
    except LigneInvalideException as e:
        logging.error(e)
        print(f"Le fichier contient une ligne invalide : {e}")
    except PrixNegatifException as e:
        logging.error(e)
        print(f"Prix incorrect : {e}")
    except CsvException as e:
        # Filet de sécurité : toute autre erreur CSV future sera attrapée ici.
        # Il vient APRÈS les exceptions filles, sinon il les attraperait toutes.
        logging.error(e)
        print(f"Erreur CSV : {e}")

    # "else" s'exécute SEULEMENT si le try s'est terminé sans exception.
    # C'est ici qu'on met le traitement normal des résultats.
    else:
        print(f"{len(articles)} article(s) chargé(s) :")
        for a in articles:
            # :.2f = nombre décimal avec 2 chiffres après la virgule
            print(f"  {a['id']} - {a['nom']} : {a['prix']:.2f}€")


# Cette condition est vraie seulement quand on lance directement "python main.py".
# Si un autre fichier fait "import main", main() ne se lance pas automatiquement.
if __name__ == "__main__":
    main()
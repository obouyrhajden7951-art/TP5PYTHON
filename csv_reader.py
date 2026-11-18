import os   # module pour interagir avec le système de fichiers


# ===== HIÉRARCHIE D'EXCEPTIONS =====
# CsvException est la mère : un seul "except CsvException" attrape toutes les erreurs CSV.
class CsvException(Exception):
    pass


class FichierIntrouvableException(CsvException):
    pass


class LigneInvalideException(CsvException):
    pass


class PrixNegatifException(CsvException):
    pass


def charger_csv(chemin):
    """Lit un fichier CSV (id;nom;prix) et renvoie une liste de dictionnaires.

    Chaque article est un dictionnaire : {"id": "1", "nom": "Stylo", "prix": 1.5}
    Lève : FichierIntrouvableException, LigneInvalideException, PrixNegatifException.
    """
    # ----- Étape 1 : le fichier existe-t-il ? -----
    # os.path.isfile() renvoie True si le chemin désigne un fichier existant.
    # On vérifie avant d'ouvrir : on lève NOTRE exception, plus claire que
    # l'erreur FileNotFoundError native de Python.
    if not os.path.isfile(chemin):
        raise FichierIntrouvableException(f"Fichier introuvable : {chemin}")

    articles = []   # liste qui contiendra les résultats

    # "with" ouvre le fichier et le FERME automatiquement à la sortie du bloc,
    # même si une exception est levée à l'intérieur.
    # encoding="utf-8" : lit correctement les accents.
    with open(chemin, encoding="utf-8") as fichier:

        # Parcourir un fichier donne ses lignes une par une.
        # enumerate(..., start=1) ajoute un compteur : numero vaut 1, 2, 3...
        # On s'en sert pour dire à l'utilisateur QUELLE ligne est fausse.
        for numero, ligne in enumerate(fichier, start=1):

            # La ligne se termine par "\n" ; strip() l'enlève (et les espaces autour)
            ligne = ligne.strip()

            # ----- Étape 2 : ignorer les lignes vides -----
            # "continue" passe directement à la ligne suivante de la boucle
            if not ligne:
                continue

            # ----- Étape 3 : contrôler le nombre de colonnes -----
            # split(";") découpe la ligne : "1;Stylo;1.50" -> ["1", "Stylo", "1.50"]
            colonnes = ligne.split(";")
            if len(colonnes) != 3:
                raise LigneInvalideException(
                    f"Ligne {numero} : 3 colonnes attendues, {len(colonnes)} trouvées."
                )

            # Déballage de liste : chaque élément va dans une variable.
            # L'expression (c.strip() for c in colonnes) enlève les espaces de chaque colonne.
            id_article, nom, prix_texte = (c.strip() for c in colonnes)

            # Un identifiant ou un nom vide est invalide
            if not id_article or not nom:
                raise LigneInvalideException(
                    f"Ligne {numero} : identifiant ou nom vide."
                )

            # ----- Étape 4 : le prix est-il un nombre ? -----
            # float("abc") lève une ValueError (exception native de Python).
            # On l'attrape et on la TRADUIT en notre exception métier.
            try:
                prix = float(prix_texte)
            except ValueError:
                raise LigneInvalideException(
                    f"Ligne {numero} : prix non numérique ('{prix_texte}')."
                )

            # ----- Étape 5 : le prix est-il strictement positif ? -----
            if prix <= 0:
                raise PrixNegatifException(
                    f"Ligne {numero} : le prix doit être supérieur à 0 (reçu : {prix})."
                )

            # Ligne valide : on ajoute un dictionnaire à la liste
            articles.append({"id": id_article, "nom": nom, "prix": prix})

    # Si aucune exception n'a été levée, on renvoie tous les articles
    return articles
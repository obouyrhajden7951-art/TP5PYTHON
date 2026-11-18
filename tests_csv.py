import os
import tempfile   # pour créer des fichiers temporaires
import unittest   # module de tests unitaires intégré à Python

from csv_reader import (
    charger_csv,
    FichierIntrouvableException,
    LigneInvalideException,
    PrixNegatifException,
)


# Une classe de test hérite de unittest.TestCase.
# Chaque méthode dont le nom commence par "test_" est exécutée comme un test.
class TestChargerCsv(unittest.TestCase):

    # Méthode utilitaire (pas un test : son nom ne commence pas par "test_")
    # Elle crée un petit fichier CSV temporaire avec le contenu voulu.
    def _creer_fichier(self, contenu):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        f.write(contenu)
        f.close()
        # addCleanup : supprime le fichier temporaire à la fin du test, même en cas d'échec
        self.addCleanup(os.remove, f.name)
        return f.name   # chemin du fichier créé

    def test_csv_valide(self):
        chemin = self._creer_fichier("1;Stylo;1.50\n2;Cahier;3.20\n3;Classeur;4.75\n")
        articles = charger_csv(chemin)
        # assertEqual(a, b) : le test réussit si a == b
        self.assertEqual(len(articles), 3)
        self.assertEqual(articles[0], {"id": "1", "nom": "Stylo", "prix": 1.5})

    def test_fichier_absent(self):
        # assertRaises : le test réussit SEULEMENT si l'exception indiquée est levée
        with self.assertRaises(FichierIntrouvableException):
            charger_csv("fichier_qui_nexiste_pas.csv")

    def test_prix_texte(self):
        # "abc" n'est pas un nombre
        chemin = self._creer_fichier("1;Stylo;abc\n")
        with self.assertRaises(LigneInvalideException):
            charger_csv(chemin)

    def test_prix_negatif(self):
        chemin = self._creer_fichier("1;Stylo;-2.0\n")
        with self.assertRaises(PrixNegatifException):
            charger_csv(chemin)

    def test_colonne_manquante(self):
        # 2 colonnes au lieu de 3
        chemin = self._creer_fichier("1;Stylo\n")
        with self.assertRaises(LigneInvalideException):
            charger_csv(chemin)

    def test_trop_de_colonnes(self):
        # 4 colonnes au lieu de 3
        chemin = self._creer_fichier("1;Stylo;1.5;extra\n")
        with self.assertRaises(LigneInvalideException):
            charger_csv(chemin)

    def test_lignes_vides_ignorees(self):
        # Des lignes vides au milieu et à la fin ne doivent pas gêner
        chemin = self._creer_fichier("\n1;Stylo;1.5\n\n2;Cahier;3\n\n")
        self.assertEqual(len(charger_csv(chemin)), 2)


# Lance tous les tests quand on exécute "python tests_csv.py"
if __name__ == "__main__":
    unittest.main()
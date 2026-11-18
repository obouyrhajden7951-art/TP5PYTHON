# ===== DÉFINIR SA PROPRE EXCEPTION =====
# En Python, toutes les exceptions héritent de la classe Exception.
# "class A(B)" signifie : A hérite de B (A est une sorte de B).
# On crée notre exception pour distinguer clairement cette erreur métier
# des erreurs générales de Python (ValueError, TypeError, etc.).
class SoldeInsuffisantException(Exception):
    # __init__ est le constructeur : il s'exécute à la création de l'objet
    # message : le texte qui décrira l'erreur
    def __init__(self, message):
        # super() désigne la classe parente (Exception).
        # On lui passe le message pour qu'elle le mémorise.
        # Sans cet appel, str(e) n'afficherait pas le message.
        super().__init__(message)


class CompteBancaire:
    # solde=0 : valeur par défaut. CompteBancaire("Bob") crée un compte à 0.
    def __init__(self, nom, solde=0):
        # self.xxx = attribut de l'objet (chaque compte a son nom et son solde)
        self.nom = nom
        self.solde = solde

    def deposer(self, montant):
        # On n'accepte que les montants positifs.
        # Un dépôt négatif est ici ignoré silencieusement
        # (extension du TP : lever une exception à la place).
        if montant > 0:
            self.solde += montant   # équivalent à : self.solde = self.solde + montant

    def retirer(self, montant):
        if montant > self.solde:
            # raise = LEVER une exception.
            # Le code de la méthode s'arrête immédiatement à cette ligne :
            # self.solde -= montant ne sera PAS exécuté.
            # L'erreur "remonte" vers le code qui a appelé retirer().
            raise SoldeInsuffisantException("Solde insuffisant pour ce retrait.")
        # On n'arrive ici que si le retrait est possible
        self.solde -= montant

    def afficher(self):
        # f-string : les {variables} sont remplacées par leur valeur
        print(f"Compte: {self.nom}, Solde: {self.solde}€")


# ===== PROGRAMME DE TEST =====
# try : "essaie d'exécuter ce bloc". Si une exception survient, Python
# saute directement au "except" correspondant.
try:
    compte = CompteBancaire("Alice", 100)
    compte.afficher()          # affiche le solde : 100€
    compte.retirer(150)        # 150 > 100 -> l'exception est levée ICI
    print("Retrait réussi")    # cette ligne n'est JAMAIS exécutée
# except Type as variable : attrape uniquement cette exception.
# "e" contient l'objet exception, donc son message.
except SoldeInsuffisantException as e:
    print("Erreur:", e)
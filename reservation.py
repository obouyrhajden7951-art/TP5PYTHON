# ===== HIÉRARCHIE D'EXCEPTIONS =====
#
#   Exception
#      └── ReservationException            (mère : toute erreur de réservation)
#             ├── CapaciteDepasseeException
#             ├── NombreInvalideException
#             └── NomClientInvalideException
#
# Avantage : "except ReservationException" attrape les trois cas d'un coup,
# mais on peut aussi attraper un cas précis si besoin.

class ReservationException(Exception):
    def __init__(self, message):
        super().__init__(message)


# "pass" = bloc vide. Ces classes héritent de tout (y compris du constructeur)
# et n'ajoutent rien : leur utilité est leur NOM, qui identifie le type d'erreur.
class CapaciteDepasseeException(ReservationException): pass
class NombreInvalideException(ReservationException): pass
class NomClientInvalideException(ReservationException): pass


class Evenement:
    def __init__(self, nom, capacite):
        self.nom = nom
        self.capacite = capacite       # nombre maximal de places
        self.places_reservees = 0      # personne n'a réservé au départ

    def reserver(self, nom_client, nb_places):
        # On valide les entrées une par une, de la plus simple à la plus complexe.
        # Ce style s'appelle "validation par garde" : on traite d'abord les erreurs,
        # puis le cas normal à la fin.

        # strip() supprime les espaces au début et à la fin.
        # "   ".strip() donne "" ; une chaîne vide est considérée comme fausse
        # en Python, donc "not ''" vaut True -> nom invalide.
        if not nom_client.strip():
            raise NomClientInvalideException("Nom du client requis.")

        if nb_places <= 0:
            raise NombreInvalideException("Nombre de places invalide.")

        # Places déjà prises + places demandées ne doivent pas dépasser la capacité.
        # Exemple : capacité 5, déjà 4 réservées, on en demande 2 : 4 + 2 = 6 > 5 -> erreur
        if self.places_reservees + nb_places > self.capacite:
            raise CapaciteDepasseeException("Capacité dépassée.")

        # Cas normal : toutes les validations sont passées
        self.places_reservees += nb_places
        print(f"Réservation confirmée pour {nom_client} ({nb_places} places).")

    def afficher(self):
        print(f"Événement: {self.nom} — {self.places_reservees}/{self.capacite} places réservées")


# ===== PROGRAMME DE TEST =====
try:
    event = Evenement("Concert", 5)
    event.reserver("", 2)     # nom vide -> NomClientInvalideException
# On attrape la classe MÈRE : cela fonctionne pour n'importe quelle exception fille
except ReservationException as e:
    print("Erreur:", e)
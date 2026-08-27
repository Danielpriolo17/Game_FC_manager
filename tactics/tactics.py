# tactics.py

class Player:
    """Clase para almacenar los datos de cada futbolista."""
    def __init__(self, id_player, name, position, rating, is_gk=False):
        self.id_player = id_player
        self.name = name
        self.position = position
        self.rating = rating
        self.is_gk = is_gk


# Coordenadas relativas en cancha (11 posiciones por formación)
FORMATIONS = {
    "4-2-3-1": [
        (55, 290),   # Portero
        (160, 110), (160, 230), (160, 350), (160, 470),  # Defensas (LB, CB, CB, RB)
        (260, 210), (260, 370),                           # Pivotes (LDM, RDM)
        (350, 120), (350, 290), (350, 460),               # Mediapuntas (LAM, CAM, RAM)
        (410, 290)                                        # Delantero (ST)
    ],
    "4-4-2": [
        (55, 290),   # Portero
        (160, 110), (160, 230), (160, 350), (160, 470),  # Defensas
        (280, 110), (280, 230), (280, 350), (280, 470),  # Mediocampistas
        (400, 220), (400, 360)                            # Delanteros
    ],
    "4-3-3": [
        (55, 290),   # Portero
        (160, 110), (160, 230), (160, 350), (160, 470),  # Defensas
        (270, 170), (270, 290), (270, 410),               # Medios
        (380, 120), (410, 290), (380, 460)                # Extremos y Delantero
    ]
}
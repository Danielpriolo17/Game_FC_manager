import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, 
    QGraphicsScene, QGraphicsEllipseItem, QWidget, 
    QVBoxLayout, QHBoxLayout, QComboBox, QLabel
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QBrush, QColor, QPen


class PlayerItem(QGraphicsEllipseItem):
    """Representa a un jugador con posición dinámica."""
    def __init__(self, x, y, color_hex, is_gk=False):
        radius = 8
        super().__init__(-radius, -radius, radius * 2, radius * 2)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(color_hex)))
        pen_color = Qt.GlobalColor.yellow if is_gk else Qt.GlobalColor.white
        self.setPen(QPen(pen_color, 1.5))


class PitchScene(QGraphicsScene):
    """Dibuja el campo de fútbol."""
    def __init__(self):
        super().__init__(0, 0, 800, 500)
        self.setBackgroundBrush(QBrush(QColor("#2e7d32")))
        self._draw_lines()

    def _draw_lines(self):
        pen = QPen(Qt.GlobalColor.white, 2)
        self.addRect(QRectF(30, 30, 740, 440), pen)
        self.addLine(400, 30, 400, 470, pen)
        self.addEllipse(340, 190, 120, 120, pen)
        self.addEllipse(397, 247, 6, 6, QPen(Qt.GlobalColor.white), QBrush(Qt.GlobalColor.white))
        self.addRect(30, 140, 100, 220, pen)
        self.addRect(670, 140, 100, 220, pen)


class TacticalManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión Táctica - Selección de Formación")
        self.resize(850, 600)

        # Diccionario con las coordenadas tácticas del equipo local
        self.FORMATIONS = {
            "4-2-3-1": [
                (55, 250), (140, 80), (140, 190), (140, 310), (140, 420),
                (230, 170), (230, 330), (310, 100), (310, 250), (310, 400), (375, 250)
            ],
            "4-4-2": [
                (55, 250), (140, 80), (140, 190), (140, 310), (140, 420),
                (250, 80), (250, 190), (250, 310), (250, 420), (360, 180), (360, 320)
            ],
            "4-3-3": [
                (55, 250), (140, 80), (140, 190), (140, 310), (140, 420),
                (240, 130), (240, 250), (240, 370), (340, 100), (370, 250), (340, 400)
            ],
            "5-3-2": [
                (55, 250), (130, 70), (130, 160), (130, 250), (130, 340), (130, 430),
                (240, 140), (240, 250), (240, 360), (360, 180), (360, 320)
            ],
            
        }

        self.home_players = []
        self._setup_ui()

    def _setup_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        # --- Panel de Controles Superior ---
        control_panel = QHBoxLayout()
        label = QLabel("Formación Táctica:")
        
        self.combo_formations = QComboBox()
        self.combo_formations.addItems(list(self.FORMATIONS.keys()))
        # Conectar el evento de cambio de índice a la función de actualización
        self.combo_formations.currentTextChanged.connect(self.change_formation)

        control_panel.addWidget(label)
        control_panel.addWidget(self.combo_formations)
        control_panel.addStretch()

        layout.addLayout(control_panel)

        # --- Escena Gráfica de la Cancha ---
        self.scene = PitchScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints().Antialiasing)
        layout.addWidget(self.view)

        self.setCentralWidget(main_widget)

        # Inicializar los 11 jugadores en la cancha
        self._init_players()

    def _init_players(self):
        """Crea las referencias de los 11 jugadores en la escena."""
        initial_coords = self.FORMATIONS["4-2-3-1"]
        for idx, (x, y) in enumerate(initial_coords):
            is_gk = (idx == 0)
            color = "#FDD835" if is_gk else "#E53935"
            player = PlayerItem(x, y, color, is_gk)
            self.scene.addItem(player)
            self.home_players.append(player)

    def change_formation(self, formation_name):
        """Actualiza la posición de los jugadores según la formación elegida."""
        coords = self.FORMATIONS.get(formation_name)
        if not coords:
            return

        for player, (new_x, new_y) in zip(self.home_players, coords):
            player.setPos(new_x, new_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TacticalManagerWindow()
    window.show()
    sys.exit(app.exec())
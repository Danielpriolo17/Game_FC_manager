# main.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QGraphicsView
)
from PyQt6.QtCore import Qt

from graphics.pitch import PitchScene, PlayerItem, BallItem
from tactics.tactics import FORMATIONS, Player  # Corregido: Player sin el '0'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FC manager")
        self.resize(980, 680)

        self.home_players_ui = []
        self._setup_ui()

    def _setup_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        # Barra Superior de Control Táctico
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Formación Local:"))
        
        self.combo_formations = QComboBox()
        self.combo_formations.addItems(list(FORMATIONS.keys()))
        self.combo_formations.currentTextChanged.connect(self._update_formation)
        top_bar.addWidget(self.combo_formations)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        # Escena e Integración con Pitch
        self.scene = PitchScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints().Antialiasing)
        layout.addWidget(self.view)

        self.setCentralWidget(main_widget)

        # Cargar Balón y Jugadores Iniciales
        self.scene.addItem(BallItem(450, 290))
        self._spawn_initial_team()

    def _spawn_initial_team(self):
        coords = FORMATIONS["4-2-3-1"]
        for idx, (x, y) in enumerate(coords):
            is_gk = (idx == 0)
            color = "#FDD835" if is_gk else "#E53935"
            player_item = PlayerItem(x, y, color, is_gk)
            self.scene.addItem(player_item)
            self.home_players_ui.append(player_item)

    def _update_formation(self, formation_name):
        coords = FORMATIONS.get(formation_name, [])
        for item, (new_x, new_y) in zip(self.home_players_ui, coords):
            item.setPos(new_x, new_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
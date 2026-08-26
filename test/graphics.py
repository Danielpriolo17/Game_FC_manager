import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, 
    QGraphicsScene, QGraphicsEllipseItem
)
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QBrush, QColor, QPen

class PlayerItem(QGraphicsEllipseItem):
    """Representa a un jugador como un círculo en el campo con un objetivo de movimiento."""
    def __init__(self, x, y, color_hex):
        super().__init__(-10, -10, 20, 20)  # Radio de 10px (diámetro 20px)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(color_hex)))
        self.setPen(QPen(Qt.GlobalColor.white, 1.5))
        
        self.target = QPointF(x, y)
        self.speed = 2.5
        self.set_new_target()

    def set_new_target(self):
        """Asigna un punto aleatorio dentro del terreno de juego."""
        self.target = QPointF(random.uniform(50, 750), random.uniform(50, 450))

    def update_position(self):
        """Mueve al jugador progresivamente hacia su objetivo."""
        current_pos = self.pos()
        direction = self.target - current_pos
        distance = (direction.x()**2 + direction.y()**2)**0.5

        # Si llegó cerca del objetivo, selecciona uno nuevo
        if distance < 5:
            self.set_new_target()
        else:
            # Normalizar vector y aplicar velocidad
            dx = (direction.x() / distance) * self.speed
            dy = (direction.y() / distance) * self.speed
            self.setPos(current_pos.x() + dx, current_pos.y() + dy)


class PitchScene(QGraphicsScene):
    """Dibuja el terreno de juego y sus líneas de demarcación."""
    def __init__(self):
        super().__init__(0, 0, 800, 500)
        self.setBackgroundBrush(QBrush(QColor("#2e7d32")))  # Verde césped
        self._draw_lines()

    def _draw_lines(self):
        pen = QPen(Qt.GlobalColor.white, 2)
        
        # Borde exterior
        self.addRect(QRectF(30, 30, 740, 440), pen)
        # Línea media
        self.addLine(400, 30, 400, 470, pen)
        # Círculo central
        self.addEllipse(340, 190, 120, 120, pen)
        # Áreas grandes
        self.addRect(30, 140, 100, 220, pen)
        self.addRect(670, 140, 100, 220, pen)


class MatchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador 2D - Motor de Partido")
        self.resize(850, 550)

        # Configuración del visor gráfico
        self.scene = PitchScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(self.view.renderHints().Antialiasing)
        self.setCentralWidget(self.view)

        self.players = []
        self._spawn_teams()

        # Bucle principal de simulación (30 FPS -> ~33ms)
        self.timer = QTimer()
        self.timer.timeout.connect(self._game_loop)
        self.timer.start(33)

    def _spawn_teams(self):
        # Equipo Local (Rojo)
        for _ in range(5):
            p = PlayerItem(random.randint(100, 350), random.randint(50, 450), "#e53935")
            self.scene.addItem(p)
            self.players.append(p)

        # Equipo Visitante (Azul)
        for _ in range(5):
            p = PlayerItem(random.randint(450, 700), random.randint(50, 450), "#1e88e5")
            self.scene.addItem(p)
            self.players.append(p)

    def _game_loop(self):
        for player in self.players:
            player.update_position()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatchWindow()
    window.show()
    sys.exit(app.exec())
# pitch.py
import sys
from PyQt6.QtWidgets import (
    QGraphicsScene, QGraphicsEllipseItem, QGraphicsItemGroup,
    QGraphicsDropShadowEffect, QGraphicsView, QApplication, QMainWindow
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QBrush, QColor, QPen, QLinearGradient, QPainterPath


class PlayerItem(QGraphicsEllipseItem):
    """Jugador con diámetro de 12px y efecto de sombra real."""
    def __init__(self, x, y, color_hex, is_gk=False):
        radius = 6  # Diámetro de 12px
        super().__init__(-radius, -radius, radius * 2, radius * 2)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(color_hex)))
        
        pen_color = Qt.GlobalColor.yellow if is_gk else Qt.GlobalColor.white
        self.setPen(QPen(pen_color, 1.2))

        # Sombra proyectada para realismo 3D
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(6)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(2, 3)
        self.setGraphicsEffect(shadow)


class BallItem(QGraphicsItemGroup):
    """Balón un 25% más pequeño que el jugador (9px de diámetro)."""
    def __init__(self, x, y):
        super().__init__()
        self.setPos(x, y)
        
        radius = 4.5  # Diámetro de 9px

        # Base blanca
        base = QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
        base.setBrush(QBrush(QColor("#FFFFFF")))
        base.setPen(QPen(QColor("#111111"), 0.8))
        self.addToGroup(base)

        # Detalles inspirados en el Mundial 2026 (Rojo, Azul y Dorado)
        center = QGraphicsEllipseItem(-1, -1, 2, 2)
        center.setBrush(QBrush(QColor("#D32F2F")))
        center.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(center)

        blue_dot = QGraphicsEllipseItem(-2.5, -1.5, 1.5, 1.5)
        blue_dot.setBrush(QBrush(QColor("#1976D2")))
        blue_dot.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(blue_dot)

        gold_dot = QGraphicsEllipseItem(1, 0.5, 1.5, 1.5)
        gold_dot.setBrush(QBrush(QColor("#FBC02D")))
        gold_dot.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(gold_dot)

        # Sombra suave para el balón
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(1.5, 2)
        self.setGraphicsEffect(shadow)


class PitchScene(QGraphicsScene):
    """Cancha realista con franjas de césped, tribunas y marcas oficiales."""
    def __init__(self):
        super().__init__(0, 0, 900, 580)
        self._draw_stadium()
        self._draw_grass()
        self._draw_lines()

    def _draw_stadium(self):
        """Dibuja la estructura exterior y gradas del estadio."""
        self.setBackgroundBrush(QBrush(QColor("#1e1e1e")))
        
        pen_tribuna = QPen(QColor("#333333"), 1)
        
        # Tribuna Superior
        top_stand_gradient = QLinearGradient(0, 0, 0, 40)
        top_stand_gradient.setColorAt(0, QColor("#3f4c6b"))
        top_stand_gradient.setColorAt(1, QColor("#606c88"))
        self.addRect(QRectF(10, 5, 880, 35), pen_tribuna, QBrush(top_stand_gradient))
        
        # Tribuna Inferior
        bottom_stand_gradient = QLinearGradient(0, 540, 0, 575)
        bottom_stand_gradient.setColorAt(0, QColor("#606c88"))
        bottom_stand_gradient.setColorAt(1, QColor("#3f4c6b"))
        self.addRect(QRectF(10, 540, 880, 35), pen_tribuna, QBrush(bottom_stand_gradient))

        # Borde exterior / Pista
        self.addRect(QRectF(40, 40, 820, 500), QPen(Qt.PenStyle.NoPen), QBrush(QColor("#151515")))

    def _draw_grass(self):
        """Dibuja el césped con patrón de franjas cortadas alternadas."""
        pitch_x, pitch_y = 50, 50
        pitch_w, pitch_h = 800, 480
        stripe_width = pitch_w / 12

        color_dark = QColor("#246b27")
        color_light = QColor("#2e7d32")

        for i in range(12):
            color = color_dark if i % 2 == 0 else color_light
            x = pitch_x + (i * stripe_width)
            self.addRect(QRectF(x, pitch_y, stripe_width, pitch_h), QPen(Qt.PenStyle.NoPen), QBrush(color))

    def _draw_lines(self):
        """Marca las líneas de juego con dimensiones y arcos matemáticos exactos."""
        pen_lines = QPen(QColor(255, 255, 255, 230), 2)
        
        # Línea de banda exterior
        self.addRect(QRectF(50, 50, 800, 480), pen_lines)
        
        # Línea central y Círculo Central
        self.addLine(450, 50, 450, 530, pen_lines)
        self.addEllipse(385, 225, 130, 130, pen_lines)
        self.addEllipse(447, 287, 6, 6, pen_lines, QBrush(Qt.GlobalColor.white))

        # Áreas Grandes (110x260 px)
        self.addRect(50, 160, 110, 260, pen_lines)
        self.addRect(740, 160, 110, 260, pen_lines)

        # Áreas Chicas (40x140 px)
        self.addRect(50, 220, 40, 140, pen_lines)
        self.addRect(810, 220, 40, 140, pen_lines)

        # Puntos de Penal (Centrados a Y = 290)
        self.addEllipse(138, 288, 4, 4, pen_lines, QBrush(Qt.GlobalColor.white))
        self.addEllipse(758, 288, 4, 4, pen_lines, QBrush(Qt.GlobalColor.white))

        # --- MEDIAS LUNAS (ARCOS DE ÁREA) PERFECTAS ---
        # Media Luna Izquierda: Circunferencia con centro en (140, 290) y Radio = 60px
        path_left = QPainterPath()
        path_left.arcMoveTo(80, 230, 120, 120, -70.5)
        path_left.arcTo(80, 230, 120, 120, -70.5, 141)
        self.addPath(path_left, pen_lines)

        # Media Luna Derecha: Circunferencia con centro en (760, 290) y Radio = 60px
        path_right = QPainterPath()
        path_right.arcMoveTo(700, 230, 120, 120, 109.5)
        path_right.arcTo(700, 230, 120, 120, 109.5, 141)
        self.addPath(path_right, pen_lines)

        # Porterías
        pen_goal = QPen(QColor("#E0E0E0"), 3)
        self.addRect(42, 245, 8, 90, pen_goal, QBrush(QColor(255, 255, 255, 60)))
        self.addRect(850, 245, 8, 90, pen_goal, QBrush(QColor(255, 255, 255, 60)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Vista de Cancha - pitch.py")
    window.resize(950, 630)

    scene = PitchScene()
    view = QGraphicsView(scene)
    view.setRenderHint(view.renderHints().Antialiasing)
    window.setCentralWidget(view)

    # Elementos de prueba
    scene.addItem(PlayerItem(450, 290, "#E53935"))
    scene.addItem(BallItem(450, 290))

    window.show()
    sys.exit(app.exec())
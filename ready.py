import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import QTimer, QRectF

class RoundedTimer(QWidget):
    def __init__(self):
        super().__init__()
        
        # Настройки окна
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Получение размеров экрана
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Динамические размеры окна
        self.outer_width = int(screen_width * 0.2)  # 10% от ширины экрана
        self.outer_height = int(screen_height * 0.2)  # 10% от высоты экрана
        self.inner_width = int(self.outer_width * 0.6)  # 80% от внешнего прямоугольника
        self.inner_height = int(self.outer_height * 0.45)  # 60% от внешнего прямоугольника

        # Центрирование окна
        self.setGeometry(
            (screen_width - self.outer_width) // 2,
            (screen_height - self.outer_height) - 50,
            self.outer_width,
            self.outer_height,
        )

        # Параметры таймера
        self.timer_time = 5
        self.time_left = self.timer_time
        self.timer_started = False
        self.start_time = None
        self.fail_displayed = False
        
        # Создаем таймер для обновления
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(100)
        
        # Метка для отображения текста
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: black; font-weight: bold; font-size: 16pt;")
        self.label.setGeometry(
            (self.outer_width - self.inner_width) // 2,
            (self.outer_height - self.inner_height) // 2,
            self.inner_width,
            self.inner_height,
        )

        # Параметры свечения
        self.glow_steps = 20  # Количество слоев свечения
        self.glow_intensity = 10  # Начальная интенсивность свечения
        self.glow_spread = 60  # Размер распространения свечения

    def set_glow_intensity(self, value):
        """Установить интенсивность свечения (0-255)"""
        self.glow_intensity = max(0, min(255, value))
        self.update()

    def set_glow_spread(self, value):
        """Установить размер распространения свечения (1-20)"""
        self.glow_spread = max(1, min(20, value))
        self.update()

    def set_glow_steps(self, value):
        """Установить количество слоев свечения (5-30)"""
        self.glow_steps = max(5, min(30, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Внешнее свечение (фон позади рамки)
        outer_rect = QRectF(
            (self.outer_width - self.inner_width) // 2,
            (self.outer_height - self.inner_height) // 2,
            self.inner_width,
            self.inner_height,
        ).adjusted(-self.glow_spread, -self.glow_spread, 
                self.glow_spread, self.glow_spread)
        
        for i in range(self.glow_steps):
            alpha = max(0, self.glow_intensity - i * (self.glow_intensity / self.glow_steps))
            glow_color = QColor(255, 127, 0, int(alpha))
            glow_path = QPainterPath()
            spread = (i * self.glow_spread) / self.glow_steps
            glow_path.addRoundedRect(
                outer_rect.adjusted(spread, spread, -spread, -spread),
                8 + spread, 8 + spread,
            )
            painter.setPen(Qt.NoPen)
            painter.setBrush(glow_color)
            painter.drawPath(glow_path)

        # Внутренний прямоугольник (белый фон)
        inner_path = QPainterPath()
        inner_path.addRoundedRect(
            (self.outer_width - self.inner_width) // 2,
            (self.outer_height - self.inner_height) // 2,
            self.inner_width,
            self.inner_height,
            8,
            8,
        )


        # Белый фон
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawPath(inner_path)

    def update_display(self):
        if self.timer_started:
            elapsed_time = time.time() - self.start_time
            self.time_left = self.timer_time - int(elapsed_time)

            if self.time_left <= 0:
                self.time_left = 0
                self.timer_started = False
                self.fail_displayed = True  # Отображение "ФЕЙЛ"

        if self.fail_displayed:
            self.label.setText("ФЕЙЛ")
        elif not self.timer_started:
            self.label.setText("ГОТОВ?")
        else:
            self.label.setText(str(self.time_left))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_C and not self.fail_displayed:  # Кнопка C для старта/перезапуска
            if self.timer_started:
                self.start_time = time.time()  # Перезапуск таймера
                self.fail_displayed = False  # Скрываем "ФЕЙЛ" при новом запуске
            else:
                self.timer_started = True
                self.start_time = time.time()
                self.fail_displayed = False
        elif event.key() == Qt.Key_F1:  # Сброс таймера
            self.timer_started = False
            self.time_left = self.timer_time
            self.fail_displayed = False  # Скрываем "ФЕЙЛ"
        elif event.key() == Qt.Key_0:  # Закрытие по '0'
            self.close()

def main():
    app = QApplication(sys.argv)
    timer = RoundedTimer()
    timer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

import tkinter as tk
import time
import ctypes

# Координаты и размеры окна
RECT_X = 1120  # Горизонтальная позиция
RECT_Y = 150   # Вертикальная позиция
RECT_WIDTH = 240  # Ширина окна
RECT_HEIGHT = 80   # Высота окна

def update_time():
    """Обновление времени каждую секунду."""
    current_time = time.strftime("%H:%M:%S")  # Формат времени
    time_label.config(text=current_time)
    root.after(1000, update_time)

# Настройка окна
root = tk.Tk()
root.geometry(f"{RECT_WIDTH}x{RECT_HEIGHT}+{RECT_X}+{RECT_Y}")  # Размер и позиция окна
root.overrideredirect(True)  # Убираем рамки окна
root.wm_attributes("-transparentcolor", "black")  # Черный цвет фона становится прозрачным

# Привязываем окно к рабочему столу
hwnd = ctypes.windll.user32.FindWindowW(None, root.title())  # Получаем дескриптор окна
ctypes.windll.user32.SetParent(hwnd, ctypes.windll.user32.GetShellWindow())  # Привязываем к рабочему столу

# Настройка метки с часами
time_label = tk.Label(
    root,
    text="",
    font=("Digital-7 Mono", 48, "bold"),  # Жирный шрифт
    fg="white",                          # Цвет текста
    bg="black",                          # Черный фон (становится прозрачным)
    justify="center",                    # Выравнивание текста
    anchor="center"                      # Централизуем текст в метке
)
time_label.pack(fill="both", expand=True)

# Обновляем время
update_time()

# Запускаем главное окно
root.mainloop()

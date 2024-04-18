from pyray import draw_circle, init_window, window_should_close, begin_drawing, \
    clear_background, \
    WHITE, draw_text, VIOLET, end_drawing, close_window, draw_pixel, draw_line, gui_slider, Rectangle
from raylib import ffi

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


def draw_circle_by_function(x, y, radius, color):
    """Diese Funktion ist bereits in raylib/pyray enthalten"""
    draw_circle(x, y, radius, color)


def draw_circle_by_points(x, y, radius, steps, color):
    """Diese Funktion zeichnet einen Kreis über Punkte. Die Anzahl der Punkte bestimmt die Qualität des Kreises.
    Die Punkte sind zusätzlich über Linien verbunden. Die Punkte werden über die Formel eines Kreises berechnet.
    Die Formel lautet:
    x = x + r * cos(2 * PI / steps * i)
    y = y + r * sin(2 * PI / steps * i)
    siehe hierzu https://de.wikipedia.org/wiki/Kreis#Parameterdarstellung
    """
    from math import cos, sin, pi as PI

    for i in range(steps):
        x1 = x + radius * cos(2 * PI / steps * i)
        y1 = y + radius * sin(2 * PI / steps * i)
        x2 = x + radius * cos(2 * PI / steps * (i + 1))
        y2 = y + radius * sin(2 * PI / steps * (i + 1))
        # wir brauchen integer
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        draw_line(x1, y1, x2, y2, color)
        draw_pixel(x1, y1, color)
        draw_pixel(x2, y2, color)


def main():
    init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Hallo")
    steps_value = ffi.new("float *", 4.0)
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)
        draw_text("Kreis zeichnen", 0, 0, 50, VIOLET)
        draw_text("--------------", 0, 50, 20, VIOLET)
        draw_text("Option 1: Wir nutzen die Funktion draw_circle() von raylib/pyray", 0, 100, 20, VIOLET)
        draw_circle_by_function(300, 300, 100, VIOLET)
        draw_text("Option 2: Wir zeichnen den Kreis über Punkte", 0, 500, 20, VIOLET)
        steps_min = 4.0
        steps_max = 20.0
        gui_slider(Rectangle(0, 550, 100, 10), "Wähle die Anzahl der Punkte", "Punkte", steps_value, steps_min, steps_max)
        draw_circle_by_points(300, 700, 100, int(steps_value[0]), VIOLET)
        end_drawing()
    close_window()


if __name__ == "__main__":
    main()

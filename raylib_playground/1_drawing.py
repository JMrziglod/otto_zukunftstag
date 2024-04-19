# Lass uns zuerst auf die 1. Aufgabe konzentrieren: 
# Etwas auf den Bildschirm malen.
# 
# Unten siehst du ein Beispiel für eine ganz einfache App,
# die nur ein schwarzes Fenster öffnet und "Hallo!" darauf schreibt.

import pyray as ry

# erstelle ein Fenster, das 800x600 Pixel groß ist
ry.init_window(800, 600, "Meine App malt")

# solange das Fenster nicht geschlossen wird
while not ry.window_should_close():
    # starte den Mal-Modus
    ry.begin_drawing()

    # übermale alles Vorherige mit der Farbe SCHWARZ
    ry.clear_background(ry.BLACK)

    # zeichne einen Text an Position (0, 0) mit der Schriftgröße 30 und der Farbe VIOLET
    ry.draw_text("Hallo!", 0, 0, 30, ry.VIOLET)

    # beenende den Mal-Modus und zeige alles auf dem Bildschirm an
    ry.end_drawing() 

# Schließe das Fenster
ry.close_window()
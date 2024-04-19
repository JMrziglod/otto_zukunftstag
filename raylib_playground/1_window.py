from random import random

import pyray as ry

# erstelle ein Fenster, das 800x600 Pixel groß ist
ry.init_window(800, 600, "Mein erstes Fenster")

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
ry.close_window()
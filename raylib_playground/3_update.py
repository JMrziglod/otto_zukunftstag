# Die 3. Aufgabe für alle Apps und Videospiele ist:
# AKTUALISIEREN den Zustand des Programms 
# 
# Unten siehst du ein Beispiel für eine ganz einfache App,
# die nur ein schwarzes Fenster öffnet und "Hallo!" darauf schreibt.

from datetime import datetime
import pyray as ry

# erstelle ein Fenster, das 800x600 Pixel groß ist
ry.init_window(800, 600, "Meine App updated sich ständig")

# Position und Geschwindigkeit des Textes
position = [0, 0]
velocity = [50, 50]

# solange das Fenster nicht geschlossen wird
while not ry.window_should_close():
    # starte den Mal-Modus
    ry.begin_drawing()

    # übermale alles Vorherige mit der Farbe SCHWARZ
    ry.clear_background(ry.BLACK)

    # aktualisiere die Position des Textes
    position[0] += velocity[0] * ry.get_frame_time()
    position[1] += velocity[1] * ry.get_frame_time()

    ry.draw_text(f"Aktuelle Uhrzeit: {datetime.now()}", 
                 int(position[0]), int(position[1]), 30, ry.VIOLET)

    # beenende den Mal-Modus und zeige alles auf dem Bildschirm an
    ry.end_drawing() 

# Schließe das Fenster
ry.close_window()
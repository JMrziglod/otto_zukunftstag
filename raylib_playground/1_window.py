# Apps oder Videospiele basieren auf einer While-Schleife, die so lange laufen,
# bis der Benutzer das Programm schließt.
# Drei Dinge werden in dieser While-Schleife gemacht:
# 1. die EINGABEN überprüft, z.B. hat der Benutzer eine Taste gedrückt oder eine Maus bewegt?
# 2. den Zustand des Programms AKTUALISIERT, z.B. ändert sich die Position des Raumschiffes?
# 3. den Zustand des Programms auf den Bildschirm gemalt, z.B. ein Bild des Raumschiffes oder ein Text.
# 
# Lass uns zuerst auf die letzte Aufgabe konzentrieren: 
# den Zustand des Programms auf den Bildschirm malen.
# 
# Unten siehst du ein Beispiel für eine ganz einfache App,
# die nur ein schwarzes Fenster öffnet und "Hallo!" darauf schreibt.

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

# Schließe das Fenster
ry.close_window()
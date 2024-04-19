# Lass uns nun die 2. Aufgabe erledigen: 
# Eingaben des Benutzers überprüfen und zwar die Mausposition.

import pyray as ry

# erstelle ein Fenster, das 800x600 Pixel groß ist
ry.init_window(800, 600, "Meine App kann mit Eingaben umgehen")

# solange das Fenster nicht geschlossen wird
while not ry.window_should_close():
    # starte den Mal-Modus
    ry.begin_drawing()

    # übermale alles Vorherige mit der Farbe SCHWARZ
    ry.clear_background(ry.BLACK)

    # !NEU! Ermittle die Mausposition und schreibe an diese Stelle einen Text
    mouse = ry.get_mouse_position()
    ry.draw_text("Ich folge dir überall hin", int(mouse.x), int(mouse.y), 30, ry.VIOLET)

    # beende den Mal-Modus und zeige alles auf dem Bildschirm an
    ry.end_drawing() 

    
# Schließe das Fenster
ry.close_window()
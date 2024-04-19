# Lass uns nun die 2. Aufgabe erledigen: 
# Eingaben des Benutzers überprüfen und zwar die Tastatureingaben.

import pyray as ry

# erstelle ein Fenster, das 800x600 Pixel groß ist
ry.init_window(800, 600, "Meine App kann mit Eingaben umgehen")

# solange das Fenster nicht geschlossen wird
while not ry.window_should_close():
    # starte den Mal-Modus
    ry.begin_drawing()

    # übermale alles Vorherige mit der Farbe SCHWARZ
    ry.clear_background(ry.BLACK)

    # !NEU! Überprüfe die Eingaben des Benutzers
    # Wenn der Benutzer die ESCAPE-Taste drückt, schließe das Fenster
    if ry.is_key_pressed(ry.KEY_ESCAPE):
        break

    # !NEU! Wenn der Benutzer die Leertaste drückt, zeige eine Nachricht
    if ry.is_key_down(ry.KEY_SPACE):
        ry.draw_text("Du drückst die Leertaste!", 0, 0, 30, ry.VIOLET)
    else:
        ry.draw_text("Drücke die <Leertaste> oder <Escape>", 0, 0, 30, ry.VIOLET)

    # beende den Mal-Modus und zeige alles auf dem Bildschirm an
    ry.end_drawing() 


# Schließe das Fenster
ry.close_window()
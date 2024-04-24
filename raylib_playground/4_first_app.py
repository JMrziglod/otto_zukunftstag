# Lass uns alle drei Aufgaben zusammenfügen und eine App erstellen,
# in der man ein Quadrat mit den Pfeiltasten bewegen kann.
# Ein weiteres Quadrat bewegt sich automatisch auf das Spieler-Quadrat zu.
# Das wird später mal die böse A.I. sein, die uns jagen wird und der wir 
# entkommen müssen.

import pyray as ry

# erstelle ein Fenster, das 800x600 Pixel groß ist
ry.init_window(800, 600, "Meine App")

# Position und Geschwindigkeit des Textes
our_position = [0, 0]
our_speed = 200

ai_position = [700, 500]
ai_speed = 100

# solange das Fenster nicht geschlossen wird
while not ry.window_should_close():
    # starte den Mal-Modus
    ry.begin_drawing()

    # übermale alles Vorherige mit der Farbe SCHWARZ
    ry.clear_background(ry.BLACK)

    # zeige eine Anleitung an
    ry.draw_text("Bewege dein Rechteck mit den Pfeiltasten", 200, 400, 20, ry.VIOLET)

    # überprüfe, ob die Pfeiltasten gedrückt wurden
    our_velocity = [0, 0]
    if ry.is_key_down(ry.KEY_RIGHT): 
        our_velocity[0] = our_speed
    if ry.is_key_down(ry.KEY_LEFT):
        our_velocity[0] = -our_speed
    if ry.is_key_down(ry.KEY_DOWN):
        our_velocity[1] = our_speed
    if ry.is_key_down(ry.KEY_UP):
        our_velocity[1] = -our_speed

    # aktualisiere die Position unseres Rechtecks
    our_position[0] += our_velocity[0] * ry.get_frame_time()
    our_position[1] += our_velocity[1] * ry.get_frame_time()

    # male ein Rechteck an unserer Position mit der Größe 50x50 und Farbe Blau
    ry.draw_rectangle(int(our_position[0]), int(our_position[1]), 50, 50, ry.BLUE)

    # Wir machen eine KI, die sich immer auf uns zubewegt:
    ai_velocity = [0, 0]
    if ai_position[0] < our_position[0]:
        ai_velocity[0] = ai_speed
    else:
        ai_velocity[0] = -ai_speed

    if ai_position[1] < our_position[1]:
        ai_velocity[1] = ai_speed
    else:
        ai_velocity[1] = -ai_speed

    # aktualisiere die Position des AI Rechtecks
    ai_position[0] += ai_velocity[0] * ry.get_frame_time()
    ai_position[1] += ai_velocity[1] * ry.get_frame_time()

    # male ein Rechteck an der AI Position mit der Größe 50x50 und Farbe Rot
    ry.draw_rectangle(int(ai_position[0]), int(ai_position[1]), 50, 50, ry.RED)

    # beenende den Mal-Modus und zeige alles auf dem Bildschirm an
    ry.end_drawing() 

# Schließe das Fenster
ry.close_window()
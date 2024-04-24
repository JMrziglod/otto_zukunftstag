# Bravo! Wir sind fast fertig! Was brauchen wir noch für unser Spiel?
# - Ein Spielzustand: Wir müssen wissen, ob wir spielen, gewonnen oder verloren haben.
# - Wir gewinnenn, wenn wir mit unserem Rechteck den gelben Kreis berühren.
# - Wir verlieren, wenn das AI-Rechteck uns vorher berührt.

import pyray as ry

# erstelle ein Fenster, das 800x600 Pixel groß ist
ry.init_window(800, 600, "Meine App")

# Position und Geschwindigkeit des Textes
our_position = [0, 0]
our_speed = 200

ai_position = [700, 500]
ai_speed = 100

# Spielzustand: kann "playing", "won" oder "lost" sein
state = "playing"

# solange das Fenster nicht geschlossen wird
while not ry.window_should_close():
    # starte den Mal-Modus
    ry.begin_drawing()

    # übermale alles Vorherige mit der Farbe SCHWARZ
    ry.clear_background(ry.BLACK)

    if state != "playing":
        if state == "won":
            ry.draw_text("Du hast gewonnen!", 200, 200, 20, ry.GREEN) 
        elif state == "lost":
            ry.draw_text("Du hast verloren!", 200, 200, 20, ry.RED)

        ry.draw_text("Drücke <LEERTASTE>, um nochmal zu spielen", 200, 250, 20, ry.VIOLET)
        if ry.is_key_down(ry.KEY_SPACE):
            state = "playing"
            our_position = [0, 0]
            ai_position = [700, 500]

        ry.end_drawing()

        # springe wieder zum Anfang der While-Schleife
        continue

    # zeige eine Anleitung an
    ry.draw_text("Fliehe vor ROT und erreiche GELB!", 200, 400, 20, ry.VIOLET)

    # male einen gelben Kreis als Ziel:
    ry.draw_circle(700, 500, 30, ry.YELLOW)

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

    # Überprüfe, ob wir gewonnen oder verloren haben
    if ry.check_collision_circles(
            ry.Vector2(our_position[0], our_position[1]), 25, 
            ry.Vector2(700, 500), 30):
        state = "won"

    our_rectangle = ry.Rectangle(our_position[0], our_position[1], 50, 50)
    ai_rectangle = ry.Rectangle(ai_position[0], ai_position[1], 50, 50)
    if ry.check_collision_recs(our_rectangle, ai_rectangle):
        state = "lost"

    # beenende den Mal-Modus und zeige alles auf dem Bildschirm an
    ry.end_drawing() 

# Schließe das Fenster
ry.close_window()
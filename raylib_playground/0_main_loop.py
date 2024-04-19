# Dies ist ein Python-Programm
# Kommentare starten mit einer Raute (#),
# und werden vom Computer ignoriert.

# Es gibt viele Python-Befehle, die der Computer verstehen kann.
# Einer davon ist der Befehl "print()" (englisch für "drucken").
print("Hallo!")

# Man kann Befehle wiederholen:
print("Hallo!")
print("Hallo!")
print("Hallo!")

# Das ist aber nicht sehr effizient.
# Besser ist es, eine Schleife zu verwenden.
# Es gibt zwei verschiedene Arten von Schleifen in Python:
# 1. Die "for"-Schleife
# Du kannst Befehle damit explizit N-Mal wiederholen:
for i in range(3):
    print("Hallo!")

# 2. Die "while"-Schleife
# Du kannst Befehle damit so lange wiederholen wie eine Bedingung erfüllt ist:
while True:
    print("Unendlich mal hallo!") # Vorsicht! Das wird unendlich oft mal ausgeführt!


# Alle Apps oder Videospiele basieren auf einer While-Schleife, die so lange läuft,
# bis der Benutzer das Programm schließt.
# Drei Aufgaben werden in dieser While-Schleife erledigt:
# 1. MALE etwas auf den Bildschirm, z.B. ein Bild der Spielerfigur oder ein Text.
# 2. EINGABEN des Benutzers überprüfen, z.B. wurde eine Taste gedrückt oder die Maus bewegt?
# 3. AKTUALISIERE den Zustand des Programms, z.B. ändert sich die Position des Spielers?
"""
Title: Secret Santa Program
Reference: https://stackoverflow.com/questions/19696542/secret-santa-program
Author: Benjamin Toueg
"""

import random

participants = [
    "Damien",
    "Maxime",
    "Guy",
    "Christine",
    "Clément",
    "Gaëlle",
    "Denis",
    "Katia",
    "Maelys",
    "Josian",
    "Lucas",
    "Isabelle",
    "Pascal",
    "Julien"
]

random.shuffle(participants)

for idx in range(len(participants)):
    print(participants[idx], "buys for", participants[(idx + 1) % (len(participants))])

"""
OUTPUT:
Guy buys for Christine
Christine buys for Josian
Josian buys for Gaëlle
Gaëlle buys for Katia
Katia buys for Julien
Julien buys for Pascal
Pascal buys for Maxime
Maxime buys for Clément
Clément buys for Damien
Damien buys for Lucas
Lucas buys for Maelys
Maelys buys for Denis
Denis buys for Isabelle
Isabelle buys for Guy
"""

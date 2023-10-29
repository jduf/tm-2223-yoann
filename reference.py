from math import cos, sin, radians
from vector_finished import Vector

trajectory_dict = {}  # Dictionnaire pour stocker les coordonnées

# Première partie : ligne droite
for t in range(0, 218):
    t = round(t * 0.001, 3)  # Convertit le pas de temps en secondes
    x = 3.167 / 0.217 * t
    y = -0.069 + (-0.069 + 2.443) / 0.217 * t
    trajectory_dict[t] = Vector(x, y)

# Deuxième partie : orbite autour de la Lune
for t in range(218, 278):
    t = round(t * 0.001, 3)  # Convertit le pas de temps en secondes
    x = cos(radians(360 * t / 2.09)) * 4 + 0.019 * 0.019 * \
        cos(radians(127.38 - 360 * (t - 0.218) / 0.005714))
    y = sin(radians(360 * t / 2.09)) * 4 + 0.019 * \
        sin(radians(127.38 - 360 * (t - 0.218) / 0.005714))
    trajectory_dict[t] = Vector(x, y)

# traj retour
x_line_start = 2.704
y_line_start = 2.945

# Coordonnées d'arrivée de la ligne droite
x_line_end = 0
y_line_end = 0

dt_values = [round(i * 0.001, 3) for i in range(185)]
line_dict = {}

for dt in dt_values:
    t = 0.278 + dt
    x = (1 - t) * x_line_start + t * x_line_end
    y = (1 - t) * y_line_start + t * y_line_end
    line_dict[dt] = Vector(x, y)

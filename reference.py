"""import matplotlib.pyplot as plt
import numpy as np

# Paramètres du scénario
apollo_distance = 0.000019  # Distance d'Apollo à la Lune
moon_orbit_radius = 4.0  # Rayon de l'orbite lunaire autour de l'origine
moon_rotation_speed = 2.09  # Vitesse de rotation de la Lune
apollo_radius = 0.02  # Rayon d'Apollo (à des fins de visualisation)
num_orbits = 10  # Nombre d'orbites d'Apollo autour de la Lune

# Temps nécessaire pour chaque étape
time_to_earth_moon = 0.217
time_for_orbits = 0.06
time_return_to_earth = 0.184

# Créez une figure
fig, ax = plt.subplots()

# Paramètres d'affichage
ax.set_aspect('equal')
ax.set_xlabel('Position en unités')
ax.set_ylabel('Position en unités')
ax.set_title('Trajectoire d\'Apollo vers la Lune')

# Fonction pour tracer une orbite
def plot_orbit(radius, time):
    theta = np.linspace(0, 2 * np.pi * time / moon_rotation_speed, 100)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color='gray', linestyle='dotted')
    return x, y

# Trajectoire de la Lune
moon_x, moon_y = plot_orbit(moon_orbit_radius, time_to_earth_moon)

# Dessinez la Lune
moon = plt.Circle((moon_x[-1], moon_y[-1]), apollo_radius, color='gray')
ax.add_patch(moon)

# Trajectoire d'Apollo vers la Lune
apollo_x, apollo_y = plot_orbit(apollo_distance, time_to_earth_moon)
ax.plot(apollo_x, apollo_y, color='red')

# Trajectoires d'orbite d'Apollo autour de la Lune
for _ in range(num_orbits):
    ax.plot(apollo_x[-1], apollo_y[-1], 'o', color='blue')
    apollo_x, apollo_y = plot_orbit(apollo_distance, time_for_orbits)

# Trajectoire de retour d'Apollo
apollo_x, apollo_y = plot_orbit(apollo_distance, time_return_to_earth)
ax.plot(apollo_x, apollo_y, color='red')

# Affichez le graphique
plt.show()"""

# trajectoire de la lune
"""import numpy as np
import matplotlib.pyplot as plt

# Paramètres
rayon_lune = 0.1  # Rayon de la Lune pour l'affichage
temps_orbite_lune = 2.09  # Période de l'orbite lunaire en unités de temps

# Points de temps d'intérêt
temps_interet = [0, 0.217, 0.217 + 0.06, 0.217 + 0.06 + 0.184]

# Créez une liste pour stocker les coordonnées (x, y) de la Lune
trajectoire_lune = []

# Temps total
temps_total = temps_orbite_lune

# Temps minimal pour un pas
dt = 0.001

temps = 0.0  # Temps initial
while temps <= temps_total:
    # Calcul des coordonnées de la Lune (orbite circulaire)
    x = 4 * np.cos(2 * np.pi * temps / temps_orbite_lune)
    y = 4 * np.sin(2 * np.pi * temps / temps_orbite_lune)
    trajectoire_lune.append((x, y))
    temps += dt

trajectoire_lune = np.array(trajectoire_lune)

# Affichage de la trajectoire de la Lune autour de la Terre
plt.figure(figsize=(6, 6))
plt.plot(trajectoire_lune[:, 0], trajectoire_lune[:, 1], label='Lune')
plt.scatter(0, 0, c='0.4', s=rayon_lune * 100, marker='o', label='Terre')

# Mettre en évidence les points de temps d'intérêt
for t in temps_interet:
    indice = int(t * len(trajectoire_lune) / temps_total)
    x_point = trajectoire_lune[indice][0]
    y_point = trajectoire_lune[indice][1]
    plt.scatter(x_point, y_point, c='red', marker='o', s=50, label=f'T = {t}')

plt.xlabel('Position X')
plt.ylabel('Position Y')
plt.title('Trajectoire de la Lune autour de la Terre')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()"""

import numpy as np
import matplotlib.pyplot as plt

# Paramètres
rayon_lune = 0.1  # Rayon de la Lune pour l'affichage
temps_orbite_lune = 2.09  # Période de l'orbite lunaire en unités de temps
distance_orbit = 0.019  # Distance à laquelle Apollo orbite autour de la Lune

# Créez une liste pour stocker les coordonnées (x, y) de la Lune
trajectoire_lune = []

# Temps total
temps_total = temps_orbite_lune

# Temps minimal pour un pas
dt = 0.001

temps = 0.0  # Temps initial
while temps <= temps_total:
    # Calcul des coordonnées de la Lune (orbite circulaire)
    x = 4 * np.cos(2 * np.pi * temps / temps_orbite_lune)
    y = 4 * np.sin(2 * np.pi * temps / temps_orbite_lune)
    trajectoire_lune.append((x, y))
    temps += dt

trajectoire_lune = np.array(trajectoire_lune)

# Coordonnées de départ d'Apollo
x_apollo_start = 0
y_apollo_start = -0.069

# Coordonnées de fin d'Apollo en t=0.217
x_apollo_end = 3.167
y_apollo_end = 2.443

# Affichage de la trajectoire de la Lune autour de la Terre
plt.figure(figsize=(8, 8))
plt.plot(trajectoire_lune[:, 0], trajectoire_lune[:, 1], label='Lune')
plt.scatter(0, 0, c='0.4', s=rayon_lune * 100, marker='o', label='Terre')

# Ligne droite d'Apollo
plt.plot([x_apollo_start, x_apollo_end], [y_apollo_start, y_apollo_end], label='Apollo', linestyle='--', color='red')

# Orbites d'Apollo autour de la Lune entre t=0.217 et t=0.277
for t_orbite in np.arange(0.217, 0.277, 0.001):
    x_orbite = x_apollo_end + distance_orbit * np.cos(2 * np.pi * (t_orbite - 0.217) / 0.06)
    y_orbite = y_apollo_end + distance_orbit * np.sin(2 * np.pi * (t_orbite - 0.217) / 0.06)
    plt.plot(x_orbite, y_orbite, marker='o', markersize=3, color='red')


plt.xlabel('Position X')
plt.ylabel('Position Y')
plt.title('Trajectoire de la Lune et d\'Apollo autour de la Terre')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()



"""
from math import cos, sin, radians

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
    x = cos(radians(360 * t / 2.09)) * 4 + 0.019 * 0.019 * cos(radians(127.38 - 360 * (t - 0.218) / 0.005714))
    y = sin(radians(360 * t / 2.09)) * 4 + 0.019 * sin(radians(127.38 - 360 * (t - 0.218) / 0.005714))
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
"""
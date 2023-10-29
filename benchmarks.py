from anim import Anim
from integrator import *
from nbody import NBody, Body, Active_Body
from math import sqrt
v_init = sqrt(0.5)
n_body = NBody(
    [
            Body(1, 0, 0, 0, -v_init),
            Body(1, 1, 0, 0, v_init)
    ]
)
integrator = RK_4Integrator(0.001, n_body)
anim = Anim(integrator)
anim.go(1)

# période pour 1 révolution
# Base: 4.472
# Verlet: 4.466
# RK4_final: 4.464
# RK_4Integrator: 66.8
# RK2_Integrator: 88.5

n_body = NBody(
        [
            Body(597, 0, 0, 0, 0),
            Body(7.34, 2.69, 2.959, -8.2205, 9.037),
            Active_Body(0.2887e-17, 2.704, 2.945,
                        9.29595, -16.117, 0.002678, 10, False)

        ]
    )
integrator = RK_4Integrator(0.001, n_body)
anim = Anim(integrator)
anim.go(1)


import matplotlib.pyplot as plt
from math import cos, sin, radians
x_positions = []
y_positions = []

# Première partie : ligne droite
for t in range(0, 218):
    t = round(t * 0.001, 3)  # Convertit le pas de temps en secondes
    x_positions.append(3.167 / 0.217 * t)
    y_positions.append(-0.069 + (-0.069 + 2.443) / 0.217 * t)

# Deuxième partie : orbite autour de la Lune
for t in range(218, 278):
    t = round(t * 0.001, 3)  # Convertit le pas de temps en secondes
    x_positions.append(cos(radians(360*t / 2.09)) * 4 +
                       0.019 * 0.019 *
                       cos(radians(127.3779 - 360 * (t - 0.218) / 0.005714)))
    y_positions.append(sin(radians(360*t / 2.09)) * 4 +
                       0.019 *
                       sin(radians(127.3779 - 360 * (t - 0.218) / 0.005714)))

# Créer le graphe
plt.figure(figsize=(8, 6))
plt.plot(x_positions, y_positions, label='Trajectoire d\'Apollo')

# Marquer les points de temps d'intérêt
for t in [0.0, 0.217, 0.277]:
    plt.scatter(x_positions[int(t*1000)],
                y_positions[int(t*1000)], label=f'T = {t}', s=50)

# Configurer l'aspect du graphe
plt.title('Trajectoire d\'Apollo')
plt.xlabel('Position X')
plt.ylabel('Position Y')
plt.legend()
plt.grid(True)

# Afficher le graphe
plt.show()

from vector_finished import Vector
from distance_matrix import DistanceMatrix
from nbody import NBody
from nbody import Body
from main import RK_ordre4
import matplotlib as plt

Astre1 = Body(1, 500, 300, 0, -200)
Astre2 = Body(1, 100, 300, 0, 200)

Astres_liste = [Astre1, Astre2]

Astres = NBody(Astres_liste)
t = 0
dt = 0.1
len_astres = len(Astres_liste)
x1 = []
y1 = []

x2 = []
y2 = []

while t < 50:
    for i in range(len_astres):
        if i == 0:
            x1.append(Astres_liste[i].x)
            y1.append(Astres_liste[i].y)
        if i == 1:
            x2.append(Astres_liste[i].x)
            y2.append(Astres_liste[i].y)

    RK_ordre4(Astres_liste)
    print(Astres.compute_resultante(), Astres.compute_emec())
    t += dt

colors = ["blue", "red"]

for i in range(len_astres):
    for j in range(len(x1)):
        if i == 0:
            plt.scatter(x1[j], y1[j], c=colors[i], marker='+')
        if i == 1:
            plt.scatter(x2[j], y2[j], c=colors[i], marker='+')

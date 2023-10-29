from typing import Iterator
import keyboard
import random
import math
from distance_matrix import DistanceMatrix
from vector_finished import Vector


class Body:
    def __init__(self, m: float, x: float, y: float, vx: float, vy: float):
        """
        Contient les paramètres d'un objet (masse, position, vitesse,
        resultante)
        """
        self.m = m
        self.r = Vector(x, y)
        self.v = Vector(vx, vy)
        self.res_force = Vector(0, 0)

    def __sub__(self, other) -> Vector:
        """
        Retourne le vecteur distance séparant les deux cet objet de l'autre
        objet.

        Surcharger cet opérateur deviendra utile car l'attribut DistanceMatrix
        de NBody sera construit sur la base de Body. En effet, DistanceMatrix
        tient à jour la distance qui sépare les différents objets en faisant la
        différence de deux objets. Il faut donc définir cette opération pour la
        class Body
        """
        return self.r - other.r

    def ecin(self) -> float:
        """Retourne l'énergie cinétique de ce objet"""
        return 1/2 * self.m * self.v.norm_squared()

    def reset_force(self) -> None:
        """Remet la résultante des forces à zéro"""
        self.res_force = Vector(0, 0)

    def add_force(self, force: Vector) -> None:
        """Additionne la force à la résultante des forces"""
        self.res_force += force


class Active_Body(Body):
    def __init__(self,m ,x , y, vx, vy, propulsion, angle, boolean, increment=0):
        super().__init__(m, x, y, vx, vy)
        self.propulsion = propulsion
        self.angle = angle
        self.boolean = boolean
        self.increment = increment


    def reset_force(self) -> None:
        if self.boolean == True:
            self.res_force = Vector(math.cos(self.angle) * self.propulsion, math.sin(self.angle) * self.propulsion)
        else:
            self.res_force = Vector(0, 0)


class NBody:
    def __init__(self, n_body: list[Body]):
        """
        Contient une liste des objets ainsi qu'une instance de DistanceMatrix
        qui contient les distances entre les objets.
        """
        self.n_body = n_body
        self.len_n = len(self.n_body)
        self.ds = DistanceMatrix([body.r for body in self.n_body])
        self.emec = 0
    def __iter__(self) -> Iterator:
        """Permet de faire une boucle for sur l'ensemble des objets"""
        for body in self.n_body:
            yield body

    def compute_forces(self):
        G = 1  # 6.7e-11
        forces = []
        positions = [body.r for body in self.n_body]
        self.ds.update(positions)

        for i, body in enumerate(self.n_body):
            body.reset_force()
            for j, other_body in enumerate(self.n_body):
                if body.r != other_body.r:
                    force = G * body.m * other_body.m * \
                            self.ds.r_over_rcube(i, j)
                else:
                    force = Vector(0, 0)

                forces.append(force)
        return forces

    def compute_resultante(self) -> None:
        """Calcule résultante des forces agissant sur chaque objet"""
        forces = self.compute_forces()
        for i, body in enumerate(self.n_body):
            for j in range(self.len_n):
                body.add_force(forces[i*self.len_n + j])
        return [body.res_force for body in self.n_body]



    def compute_emec(self) -> None:
        """Calcule l'énergie mécanique totale du système de n objets"""
        ecin_tot = 0
        for body in self.n_body:
            ecin_tot += body.ecin()
        epot_tot = 0
        for j in range(self.len_n):
            epot_sur_j = 0
            for m in range(self.len_n):
                if j < m:
                    epot_sur_j += \
                        self.compute_forces()[self.len_n * j + m].norm() * \
                        self.ds._get(j, m).norm()
            epot_tot += epot_sur_j
            # print("epot", epot_tot)
        self.emec = ecin_tot + epot_tot




def test_n_body():
    body_list = [
        Body(1, 0, 0, 0, 0),
        Body(1, 0, 1, 0, 0),
        Body(1, 1, 0, 0, 0),
    ]

    assert (body_list[0] - body_list[1]) == Vector(0, -1)
    assert (body_list[0] - body_list[2]) == Vector(-1, 0)
    assert (body_list[1] - body_list[2]) == Vector(-1, 1)

    nb = NBody(body_list)
    nb.compute_resultante()

    from math import sqrt
    a = sqrt(2)
    a = 1/(a*a*a)
    vector_list = [
        Vector(1, 1),
        Vector(a, -1-a),
        Vector(-1-a, a),
    ]
    for i, body in enumerate(nb.n_body):
        assert body.res_force == vector_list[i]

    nb.compute_emec()
    print(nb.compute_emec())
    assert nb.emec == 2.7071067811865475

    for i, body in enumerate(nb):
        assert nb.compute_resultante()[i] == vector_list[i]


if __name__ == "__main__":
    test_n_body()

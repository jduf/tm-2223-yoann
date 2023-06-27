from typing import Iterator
from distance_matrix import DistanceMatrix
from vector_finished import Vector


class Body:
    def __init__(self, m: float, x: float, y: float, vx: float, vy: float):
        """
        Contient les paramètres d'un objet (masse, position, vitesse,
        resultante)
        """
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = Vector(x, y)
        self.v = Vector(vx, vy)

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
        self.d = self.other = Vector(0, 0)
        self.other = other
        self.d.x = self.x - self.other.x
        self.d.y = self.y - self.other.y
        return self.d

    def ecin(self) -> float:
        """Retourne l'énergie cinétique de ce objet"""
        ecin = 1/2 * self.m * self.v.norm_squared()
        return ecin

    def reset_force(self) -> None:
        """Remet la résultante des forces à zéro"""
        self.res_force = 0
        return self.res_force

    def add_force(self, force: Vector) -> None:
        """Additionne la force à la résultante des forces"""
        self.res_force += force
        return self.res_force


class NBody:
    def __init__(self, n_body: list[Body]):
        """
        Contient une liste des objets ainsi qu'une instance de DistanceMatrix
        qui contient les distances entre les objets.
        """
        self.n_body = n_body
        self.len = len(n_body)
        self.r_all = []
        for i in range(self.len):
            self.r_all.append(self.n_body[i].r)
        self.ds = DistanceMatrix(self.r_all)
    def __iter__(self) -> Iterator:
        """Permet de faire une boucle for sur l'ensemble des objets"""
        for body in self.n_body:
            yield body

    def compute_forces(self):
        G = 1  # 6.7e-11
        forces = []
        self.r_all = []
        for i in range(self.len):
            self.r_all.append(self.n_body[i].r)
        self.ds.update(self.r_all)
        for i, body in enumerate(self.n_body):
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
        resultantes = []
        forces = self.compute_forces()
        for j in range(self.len):
            forces_sur_j = []
            for m in range(self.len):
                forces_sur_j.append(forces[self.len * j + m])
# l'intervalle des forces s'appliquant sur l'objet j

            resultante_sur_j = Vector(0, 0)
            for k in range(self.len):
                resultante_sur_j += forces_sur_j[k]

            resultantes.append(resultante_sur_j)

        return resultantes

    def compute_emec(self) -> None:
        """Calcule l'énergie mécanique totale du système de n objets"""
        ecin_tot = 0
        for i in range(self.len - 1):
            ecin_tot += self.n_body[i].ecin()

        epot_tot = 0
        for j in range(self.len):
            epot_sur_j = 0
            for m in range(self.len):
                if j == m:
                    pass
                else:
                    epot_sur_j += \
                        self.compute_forces()[self.len * j + m].norm() * \
                        self.ds._get(j, m).norm()
        emec = ecin_tot + epot_tot
        return emec


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
        assert nb.compute_resultante()[i] == vector_list[i]

    nb.compute_emec()
    print(nb.compute_emec())
    assert nb.compute_emec() == 2.7071067811865475

    for i, body in enumerate(nb):
        assert nb.compute_resultante()[i] == vector_list[i]


if __name__ == "__main__":
    test_n_body()

from vector_finished import Vector

# Comme vous allez étudier le comportement de n planètes/satellites/...
# interagissent par la force gravitationnelle, il est utile de définir une
# class qui tient à jour la distance entre chaque objets. Pour ce faire, vous
# allez implémenter une class DistanceMatrix qui simplifiera ensuite le calcul
# des forces et des énergie potentielles.

# Pour commencer, définissez dans la méthode self.update() une variable
# self._rij qui contiendra les Vecteurs rij représentant la distance en l'objet
# i et l'objet j. Par convention, les attributs de class qui commencent par "_"
# sont privés. Cela signifie qu'ils ne doivent pas être utilisés hors de la
# classe. Comme on veut cacher à l'utilisateur les détails d'implémentation de
# cette matrice afin qu'il n'utilise que les fonctions "unit_vector", "norm",
# "norm_squared" et "r_over_rcubed", on définit la variable self._rij comme
# privée.
# La définition de self._rij peut se faire de plusieurs façon, c'est à vous de
# choisir laquelle. La façon la plus simple est de définir une liste de liste
# self._rij = [
#     [
#         (self.objects[i] - self.objects[j])
#         for i in range(self.n)
#     ]
#     for j in range(self.n)
# ]
# Cette matrice ressemble à:
# 0 -1 -2 -4
# 1  0 -3 -5
# 2  3  0 -6
# 4  5  6  0

# Je n'ai pas testé cette implémentation car elle n'est pas efficace... en
# effet, comme rij=-rji, il ne sert à rien de stocker les Vecteurs à double.
# Similairement, comme rii=0, il est inutile de les stocker. Ainsi une façon
# plus efficace de stocker ces données est d'utiliser une liste plus courte
# pour laquelle le kième élément est la kième entrée non nulle d'une matrice
# strictement triangulaire inférieure. Une telle matrice ressemble à cela:
# 0 0 0 0
# 1 0 0 0
# 2 3 0 0
# 4 5 6 0
# et la liste correspondante est [1,2,3,4,5,6]. Remarquez qu'au lieu de stocker
# 16 Vecteurs, seuls 6 vecteurs son stockés. La contrepartie négative à cette
# façon de procéder est qu'il n'est pas intuitif d'accéder à la distance qui
# sépare l'objet 3 de l'objet 2 (correspondant à la dernière ligne/deuxième
# colonne de la matrice, la valeur 5). C'est pour cela qu'il est nécessaire de
# définir la méthode self._get(i,j) qui retourne le bon Vecteur.


class DistanceMatrix:
    """
    Cette class fournit des outils simplifiant le suivi des distances entre
    les objets.
    """
    def __init__(self, objects: list[Vector]):
        self.objects = objects
        self.n = len(objects)
        self.update(objects)

    def update(self, new_objects) -> None:
        """Met à jour les distances entre les objets"""
        self.rij = []
        for j in range(self.n):
            for i in range(self.n):
                if j < i:
                    b = new_objects[i] - new_objects[j]
                    self.rij.append(b)
                else:
                    pass

    def _get(self, i: int, j: int) -> Vector:
        """
        Retourne le vecteur de distance entre l'objet i et j
        """
        if j < i:
            a = j * (2 * self.n - j - 3) / 2 + i
            a = a.__int__()
            distance = -self.rij[a-1]
        elif i == j:
            distance = Vector(0, 0)
        else:
            k = i
            i = j
            j = k
            a = j * (2 * self.n - j - 3) / 2 + i
            a = a.__int__()
            distance = self.rij[a-1]

        return distance

    def unit_vector(self, i: int, j: int) -> Vector:
        """
        Retourne le vecteur unitaire partant de l'objet i et pointant vers
        l'objet j.
        """
        d = self._get(i, j)
        a = d.norm()
        if a == 0:
            raise AssertionError
        else:
            u = Vector(0, 0)
            u.x = d.x / a
            u.y = d.y / a
        return Vector(u.x, u.y)

    def norm(self, i: int, j: int) -> float:
        """
        Retourne la norme du vecteur distance partant de l'objet i et pointant
        vers l'objet j.
        """
        d = self._get(i, j)
        a = d.norm()
        return a

    def norm_squared(self, i: int, j: int) -> float:
        """
        Retourne la norme au carré du vecteur distance partant de l'objet i et
        pointant vers l'objet j.
        """
        d = self._get(i, j)
        a = d.norm_squared()
        return a

    def r_over_rcube(self, i: int, j: int) -> Vector:
        """
        Retourne le vecteur distance partant de l'objet i et pointant vers
        l'objet j divisé par le cube de ce vecteur.
        """
        r = self._get(i, j)
        a = r.norm()
        if a != 0:
            r_over_rcube = r/a**3

        else:
            raise AssertionError

        return r_over_rcube


def test_distance_matrix() -> None:
    objs = [
        Vector(0, 3),
        Vector(4, 0),
        Vector(0, 0),
    ]
    ds = DistanceMatrix(objs)

    assert ds._get(1, 0) == Vector(-4, 3)
    assert ds._get(0, 1) == Vector(4, -3)

    assert ds._get(2, 0) == Vector(0, 3)
    assert ds._get(0, 2) == Vector(0, -3)

    assert ds._get(2, 1) == Vector(4, 0)
    assert ds._get(1, 2) == Vector(-4, 0)

    assert ds.norm_squared(0, 0) == 0
    assert ds.norm_squared(1, 1) == 0
    assert ds.norm_squared(2, 2) == 0

    assert ds.norm_squared(1, 0) == 25
    assert ds.norm_squared(0, 1) == 25

    assert ds.norm_squared(1, 2) == 16
    assert ds.norm_squared(2, 1) == 16

    assert ds.norm_squared(2, 0) == 9
    assert ds.norm_squared(0, 2) == 9

    assert ds.r_over_rcube(0, 1) == Vector(0.032, -0.024)
    assert ds.r_over_rcube(1, 0) == Vector(-0.032, 0.024)

    objs[2] = Vector(4, 0)
    ds.update()
    assert ds.norm_squared(1, 2) == 0


if __name__ == "__main__":
    test_distance_matrix()

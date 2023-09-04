import keyboard
import random
from vector_finished import Vector
from nbody import *
import copy

# On implémente ici un algorithme pour faire évoluer le système dans le temps.
# Il existe de nombreux algorithmes différents et j'ai déjà mentionné celui de
# Runge-Kutta.
# Je vous propose ici d'implémenter un algorithme basique qui repose sur une
# approche naïve: chaque objet avance en MRU durant un petit intervalle de
# temps à la suite duquel, la vitesse est modifiée selon les MRUA (notez bien
# que l'on mélange MRU et MRUA mais cela 'fonctionne' si le pas de temps est
# suffisamment petit). La seule méthode à implémenter ici est
# get_new_positions.


class BaseIntegrator:
    def __init__(self, dt: float, n_body: NBody):
        """Contient le système qui doit évoluer par pas de temps dt"""
        self.n_body = n_body
        self.dt = dt
        self.t = 0  # temps écoulé depuis le début de la simulation
        self.len_n_body = len(self.n_body.n_body)

    def get_new_positions(self):
        """
        Met à jour les nouvelles positions et vitesse de tous les Body après un
        pas de temps et retourne les nouvelles positions.
        """

        new_vitesses = []
        new_positions = []
        self.t += self.dt
        for body in self.n_body.n_body:
            body.r += body.v * self.dt
            new_positions.append(body.r)

        self.n_body.compute_resultante()
        for body in self.n_body.n_body:
            body.v += body.res_force / \
                body.m * self.dt

            new_vitesses.append(body.v)
            body.reset_force()

        return new_positions


class RK_4Integrator:

    def __init__(self, dt, n_body: NBody):
        self.dt = dt
        self.t = 0
        self.n_body = n_body
        self.len_n = len(self.n_body.n_body)

    def get_new_positions(self):
        new_positions = []
        """if self.t > 3.3 and self.t < 3.4:
            print("pos lune", self.n_body.n_body[1].r.x, self.n_body.n_body[1].r.y)
            print("pos apollo", self.n_body.n_body[2].r.x, self.n_body.n_body[2].r.y)"""

        for body in self.n_body.n_body:
            k1 = body.v * self.dt
            k2 = self.dt / 2 * (body.v + self.dt / 2 * k1)
            k3 = self.dt / 2 * (body.v + self.dt / 2 * k2)
            k4 = self.dt * (body.v + self.dt / 2 * k3)
            r_i = body.r + self.dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            body.r = r_i

            new_positions.append(r_i)

        new_vitesses = []
        self.n_body.compute_resultante()

        for body in self.n_body.n_body:
            a_i = body.res_force / body.m

            k1_v = a_i * self.dt
            k2_v = self.dt / 2 * (a_i + self.dt / 2 * k1_v)
            k3_v = self.dt / 2 * (a_i + self.dt / 2 * k2_v)
            k4_v = self.dt * (a_i + self.dt / 2 * k3_v)
            v_i = body.v + self.dt / 6 * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)
            body.v = v_i

            new_vitesses.append(v_i)
            body.reset_force()
            if isinstance(body, Active_Body) == True and self.t < 0.00223 and body.boolean == True:
                body.propulsion = 1.623e-15
            elif isinstance(body, Active_Body) == True and self.t > 0.00223 and self.t < 0.0071 and body.boolean == True:
                body.propulsion = 2.453e-16
                body.m = 8.8e-17 # 3.06687e-16 - 2.18e-16
            elif isinstance(body,Active_Body) == True and self.t > 0.0071 and self.t < 0.00927 and body.boolean == True:
                body.propulsion = 4.8e-17
                body.m = 3.99e-17 # 8.8e-17 - 4.81e-17
            elif isinstance(body, Active_Body) == True and body.boolean:
                body.angle += body.increment
            elif isinstance(body,Active_Body) == True and self.t > 0.00927 and body.boolean == True:
                body.propulsion = 0

        self.t += self.dt

        return new_positions

class RK_4_ajuste:
    def __init__(self, dt, n_body: NBody):
        self.dt = dt
        self.t = 0
        self.n_body = n_body
        self.len_n = len(self.n_body.n_body)

    def get_new_positions(self):
        new_positions = []
        new_vitesses = []
        self.n_body.compute_resultante()

        """if self.t > 3.3 and self.t < 3.4:
            print("pos lune", self.n_body.n_body[1].r.x, self.n_body.n_body[1].r.y)
            print("pos apollo", self.n_body.n_body[2].r.x, self.n_body.n_body[2].r.y)"""

        a_i = [body.res_force / body.m for body in self.n_body.n_body]

        k1 = [body.v * self.dt for body in self.n_body.n_body]
        k1_v = [a * self.dt for a in a_i]


        temp_n_body_k2 = copy.deepcopy(self.n_body)
        self.n_body.compute_resultante()
        a_i = [body.res_force / body.m for body in self.n_body.n_body]
        for body, a in zip(temp_n_body_k2.n_body, a_i):
            body.r += body.v * self.dt / 2
            body.v += a * self.dt / 2

        k2 = [self.dt / 2 * (v + self.dt / 2 * k) for v, k in zip([body.v for body in temp_n_body_k2.n_body], k1)]
        k2_v = [self.dt / 2 * (a + self.dt / 2 * k1) for a, k1 in zip(a_i, k1_v)]


        temp_n_body_k3 = copy.deepcopy(self.n_body)
        self.n_body.compute_resultante()
        a_i = [body.res_force / body.m for body in self.n_body.n_body]
        for body, a, k2_val in zip(temp_n_body_k3.n_body, a_i, k2_v):
            body.r += body.v * self.dt / 2
            body.v += k2_val * self.dt / 2

        k3 = [self.dt / 2 * (v + self.dt / 2 * k) for v, k in zip([body.v for body in temp_n_body_k3.n_body], k2)]
        k3_v = [self.dt / 2 * (a + self.dt / 2 * k2) for a, k2 in zip(a_i, k2_v)]


        temp_n_body_k4 = copy.deepcopy(self.n_body)
        self.n_body.compute_resultante()
        a_i = [body.res_force / body.m for body in self.n_body.n_body]
        for body, a, k3_val in zip(temp_n_body_k4.n_body, a_i, k3_v):
            body.r += body.v * self.dt
            body.v += k3_val * self.dt

        k4 = [self.dt * (v + self.dt / 2 * k) for v, k in zip([body.v for body in temp_n_body_k4.n_body], k3)]
        k4_v = [self.dt * (a + self.dt / 2 * k3) for a, k3 in zip(a_i, k3_v)]

        for i, body in enumerate(self.n_body.n_body):
            r_i = body.r + self.dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
            body.r = r_i
            new_positions.append(r_i)

        for i, body in enumerate(self.n_body.n_body):
            v_i = body.v + self.dt / 6 * (k1_v[i] + 2 * k2_v[i] + 2 * k3_v[i] + k4_v[i])
            body.v = v_i
            new_vitesses.append(v_i)
            body.reset_force()
            if i == 2:
                print(body.r.x, body.r.y)

        self.t += self.dt

        return new_positions

class RK_2Integrator:
    def __init__(self, dt, n_body: NBody):
        self.dt = dt
        self.t = 0
        self.n_body = n_body
        self.len_n = len(self.n_body.n_body)

    def get_new_positions(self):
        new_positions = []
        new_vitesses = []
        self.n_body.compute_resultante()

        for body in self.n_body.n_body:
            r_i = body.r + self.dt ** 2 / 2 * body.v * (1 + self.dt ** 2 / 2)
            body.r = r_i
            new_positions.append(r_i)

            a_i = body.res_force / body.m
            v_i = body.v + self.dt ** 2 / 2 * a_i * (1 + self.dt ** 2 / 2)
            body.v = v_i
            new_vitesses.append(v_i)
            body.reset_force()
        self.t += self.dt

        return new_positions

class VerletIntegrator:
    def __init__(self, dt, n_body: NBody):
        self.dt = dt
        self.n_body = n_body
        self.previous_positions = []
        for body in self.n_body:
            self.previous_positions.append(body.r)
        self.t = 0

    def get_new_positions(self):
        self.n_body.compute_resultante()

        if self.t == 0:
            for body in self.n_body:

                body.r += body.v * self.dt
                body.v += 0.5 * body.res_force / body.m * self.dt

        else:
            for i, body in enumerate(self.n_body):
                new_position = 2 * body.r - self.previous_positions[i] + body.res_force / body.m * self.dt ** 2
                body.v = (new_position - self.previous_positions[i]) / (2 * self.dt)
                self.previous_positions[i] = body.r
                body.r = new_position

        self.t += self.dt




def test_integrator():
    from nbody import Body
    from vector_finished import Vector
    n_body = NBody(
        [
            Body(1, 0, 0, 0, -0.5),
            Body(1, 2, 0, 0, 0.5),
        ]
    )
    step_one = [
        Vector(0, -0.005),
        Vector(2, 0.005),
    ]

    integrator = BaseIntegrator(0.01, n_body)
    for pos, step in zip(integrator.get_new_positions(), step_one):
        assert pos == step

    step_two = [
        Vector(2.5e-05, -0.01),
        Vector(1.999975, 0.01)
    ]
    for pos, step in zip(integrator.get_new_positions(), step_two):
        assert pos == step


if __name__ == "__main__":
    test_integrator()

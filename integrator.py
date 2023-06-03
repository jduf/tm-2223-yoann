from nbody import NBody

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
        for i in range(self.len_n_body):
            self.n_body.n_body[i].r += self.n_body.n_body[i].v * self.dt
            new_positions.append(self.n_body.n_body[i].r)

        resultantes = self.n_body.compute_resultante()
        for i in range(self.len_n_body):
            self.n_body.n_body[i].v += resultantes[i] / \
                self.n_body.n_body[i].m * self.dt

            new_vitesses.append(self.n_body.n_body[i].v)

        return new_positions


class RK_4Integrator:

    def __init__(self, dt, n_body: NBody):
        self.dt = dt
        self.t = 0
        self.n_body = n_body
        self.len_n = len(self.n_body.n_body)

    def get_new_positions(self):
        new_positions = []

        for i in range(self.len_n):

            k1 = self.n_body.n_body[i].v * self.dt
            k2 = self.dt / 2 * (self.n_body.n_body[i].v + self.dt / 2 * k1)
            k3 = self.dt / 2 * (self.n_body.n_body[i].v + self.dt / 2 * k2)
            k4 = self.dt * (self.n_body.n_body[i].v + self.dt / 2 * k3)
            r_i = self.n_body.n_body[i].r + self.dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            self.n_body.n_body[i].r = r_i

            new_positions.append(r_i)

        new_vitesses = []
        resultantes = self.n_body.compute_resultante()

        for i in range(self.len_n):
            a_i = resultantes[i] / self.n_body.n_body[i].m

            k1_v = a_i * self.dt
            k2_v = self.dt / 2 * (a_i + self.dt / 2 * k1_v)
            k3_v = self.dt / 2 * (a_i + self.dt / 2 * k2_v)
            k4_v = self.dt * (a_i + self.dt / 2 * k3_v)
            v_i = self.n_body.n_body[i].v + self.dt / 6 * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)
            self.n_body.n_body[i].v = v_i

            new_vitesses.append(v_i)

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
        resultantes = self.n_body.compute_resultante()

        for i in range(self.len_n):
            r_i = self.n_body.n_body[i].r + self.dt ** 2 / 2 * self.n_body.n_body[i].v * (1 + self.dt ** 2 / 2)
            self.n_body.n_body[i].r = r_i
            print(r_i.x, r_i.y)
            new_positions.append(r_i)

            a_i = resultantes[i] / self.n_body.n_body[i].m
            v_i = self.n_body.n_body[i].v + self.dt ** 2 / 2 * a_i * (1 + self.dt ** 2 / 2)
            self.n_body.n_body[i].v = v_i
            new_vitesses.append(v_i)
        self.t += self.dt

        return new_positions




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

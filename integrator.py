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

    def get_new_positions(self):
        """
        Met à jour les nouvelles positions et vitesse de tous les Body après un
        pas de temps et retourne les nouvelles positions.
        """
        for body in self.n_body.n_body:
            body.r += body.v * self.dt

        self.n_body.compute_resultante()
        for body in self.n_body.n_body:
            body.v += body.res_force / body.m * self.dt

        self.t += self.dt
        return [body.r for body in self.n_body.n_body]


class RK_4Integrator:

    def __init__(self, dt, n_body: NBody):
        self.dt = dt
        self.t = 0
        self.n_body = n_body
        self.len_n = len(self.n_body.n_body)

    def get_new_positions(self):
        new_positions = []

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
            """if isinstance(body, Active_Body) == True and self.t < 0.00223 and body.boolean == True:
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
                body.propulsion = 0"""
            # partie du code utile pour la mise en orbite autour de la Terre

        self.t += self.dt

        return new_positions, new_vitesses

class RK_4_ajuste:
    # sorte de version intermédiaire entre RK4_Integrator et le final mais il est complètement faux
    def __init__(self, dt, n_body: NBody):
        self.dt = dt
        self.t = 0
        self.n_body = n_body
        self.len_n = len(self.n_body.n_body)

    def get_new_positions(self):
        new_positions = []
        new_vitesses = []

        self.n_body.compute_resultante()
        for k, body in enumerate(self.n_body.n_body):
            if k == 1:
                print(body.res_force.x, body.res_force.y)

        a_i = [body.res_force / body.m for body in self.n_body.n_body]
        k1 = [body.v * self.dt for body in self.n_body.n_body]
        k1_v = [a * self.dt for a in a_i]


        temp_n_body_k2 = copy.deepcopy(self.n_body)
        for body, a in zip(temp_n_body_k2.n_body, a_i):
            body.r += body.v * self.dt / 2
            body.v += a * self.dt / 2
        temp_n_body_k2.compute_resultante()
        a_i2 = [body.res_force / body.m for body in temp_n_body_k2]

        k2 = [self.dt / 2 * (v + self.dt / 2 * k) for v, k in zip([body.v for body in temp_n_body_k2.n_body], k1)]
        k2_v = [self.dt / 2 * (a + self.dt / 2 * k1) for a, k1 in zip(a_i2, k1_v)]


        temp_n_body_k3 = copy.deepcopy(self.n_body)
        for body, a, k2_val in zip(temp_n_body_k3.n_body, a_i, k2_v):
            body.r += body.v * self.dt / 2
            body.v += k2_val * self.dt / 2
        temp_n_body_k3.compute_resultante()
        a_i3 = [body.res_force / body.m for body in temp_n_body_k3]

        k3 = [self.dt / 2 * (v + self.dt / 2 * k) for v, k in zip([body.v for body in temp_n_body_k3.n_body], k2)]
        k3_v = [self.dt / 2 * (a + self.dt / 2 * k2) for a, k2 in zip(a_i3, k2_v)]


        temp_n_body_k4 = copy.deepcopy(self.n_body)
        for body, a, k3_val in zip(temp_n_body_k4.n_body, a_i, k3_v):
            body.r += body.v * self.dt
            body.v += k3_val * self.dt
        temp_n_body_k4.compute_resultante()
        a_i4 = [body.res_force / body.m for body in temp_n_body_k4]

        k4 = [self.dt * (v + self.dt / 2 * k) for v, k in zip([body.v for body in temp_n_body_k4.n_body], k3)]
        k4_v = [self.dt * (a + self.dt / 2 * k3) for a, k3 in zip(a_i4, k3_v)]

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


class RK_4_total:
    # pareil que le ajuste mais en un peu mieux
    def __init__(self, dt, n_body):
        self.dt = dt
        self.t = 0
        self.n_body = n_body

    def get_new_positions(self):
        new_positions = []
        new_vitesses = []

        self.n_body.compute_resultante()
        a_i = [body.res_force / body.m for body in self.n_body.n_body]

        for i, body in enumerate(self.n_body.n_body):
            if i == 0:
                print(body.ecin())
            k1x = self.dt * body.v
            k1v = self.dt * a_i[i]

            temp_n_body_k2 = copy.deepcopy(self.n_body)
            temp_n_body_k2.n_body[i].r += k1x / 2
            temp_n_body_k2.n_body[i].v += k1v / 2
            temp_n_body_k2.compute_resultante()
            a_i2 = [body.res_force / body.m for body in temp_n_body_k2.n_body]

            k2x = self.dt * (body.v + k1v / 2)
            k2v = self.dt * a_i2[i]

            temp_n_body_k3 = copy.deepcopy(self.n_body)
            temp_n_body_k3.n_body[i].r += k2x / 2
            temp_n_body_k3.n_body[i].v += k2v / 2
            temp_n_body_k3.compute_resultante()
            a_i3 = [body.res_force / body.m for body in temp_n_body_k3.n_body]

            k3x = self.dt * (body.v + k2v / 2)
            k3v = self.dt * a_i3[i]

            temp_n_body_k4 = copy.deepcopy(self.n_body)
            temp_n_body_k4.n_body[i].r += k3x
            temp_n_body_k4.n_body[i].v += k3v
            temp_n_body_k4.compute_resultante()
            a_i4 = [body.res_force / body.m for body in temp_n_body_k4.n_body]

            k4x = self.dt * (body.v + k3v)
            k4v = self.dt * a_i4[i]

            r_i = body.r + (1/6) * (k1x + 2*k2x + 2*k3x + k4x)
            v_i = body.v + (1/6) * (k1v + 2*k2v + 2*k3v + k4v)

            body.r = r_i
            body.v = v_i
            body.reset_force()

            new_positions.append(r_i)
            new_vitesses.append(v_i)

        self.t += self.dt

        return new_positions, new_vitesses

class RK4_killian:
    # une des versions de Killian qu'il m'a donnée pour comparer
    def __init__(self,dt: float, n_body: NBody):
        self.n_body = n_body
        self.dt = dt
        self.t = 0

    def get_new_positions(self):
        l = len(self.n_body.n_body)
        v=[]#vecteur vitesse de chaque objet
        for body in self.n_body.n_body:
            v.append(body.v)
        k1=[]#fixer k1
        self.n_body.compute_resultante()
        for i in range(l):
            k1.append(Vector(0,0))
            k1[i]=self.n_body.n_body[i].r*(1/self.n_body.n_body[i].m)
        k2=[]#k2
        BINT1=BaseIntegrator(self.dt/2,self.n_body)
        BINT1.get_new_positions()
        for i in range(l):
            k2.append(Vector(0,0))
            k2[i]=BINT1.n_body.n_body[i].r*(1/BINT1.n_body.n_body[i].m)
        k3=[]#k3
        pos3 = []
        bodyk3=[]
        for i in range(l):
            pos3.append(Vector(0,0))
            pos3[i] =BINT1.n_body.n_body[i].r +(pow(self.dt,2)/4) * k1[i] #self.n_body.n_body[i].vitesse + (pow(self.dt,2)/4) * k1[i]
            bodyk3.append(Body(BINT1.n_body.n_body[i].m,pos3[i].x,pos3[i].y,0,0))
        n_body3 = NBody(bodyk3)
        n_body3.compute_resultante()
        for i in range(l):
            k3.append(Vector(0,0))
            k3[i]=n_body3.n_body[i].r*(1/self.n_body.n_body[i].m)
        k4=[]#k4
        pos4=[]
        bodyk4=[]
        for i in range(l):
            pos4.append(Vector(0,0))
            bodyk4.append(Body(0,0,0,0,0))
            pos4[i]= self.n_body.n_body[i].r + self.dt * self.n_body.n_body[i].v + (pow(self.dt,2)/2)*k2[i]
            bodyk4[i]=Body(self.n_body.n_body[i].m,pos4[i].x,pos4[i].y,0,0)
        n_body4 = NBody([bodyk4[i]for i in range(l)])
        n_body4.compute_resultante()
        for i in range(l):
            k4.append(Vector(0,0))
            k4[i]=n_body4.n_body[i].r*(1/self.n_body.n_body[i].m)
        for i in range(l):
            self.n_body.n_body[i].r += self.dt*self.n_body.n_body[i].v + (pow(self.dt,2)/6)*(k1[i] + k2[i]+k3[i])
            self.n_body.n_body[i].v += (self.dt/6)*(k1[i]+2*k2[i]+2*k3[i]+k4[i])


class RK4_final:
    def __init__(self, dt, n_body):
        self.dt = dt
        self.t = 0
        self.n_body = n_body
        self.len_n = len(self.n_body.n_body)

    def get_new_positions(self):
        self.n_body.compute_resultante()
        a1 = [body.res_force / body.m for body in self.n_body.n_body]
        k1v = [a1[i] * self.dt for i in range(self.len_n)]
        k1x = [body.v * self.dt for body in self.n_body.n_body]

        # créer une nouvelle liste de Body mais avec les variations de vitesse et de position
        nbody2 = NBody([
            Body(body.m, body.r.x + k1x[i].x/2, body.r.y + k1x[i].y/2, body.v.x + k1v[i].x/2, body.v.y + k1v[1].y/2)
            for i, body in enumerate(self.n_body.n_body)
        ])
        nbody2.compute_resultante()
        a2 = [body.res_force / body.m for body in nbody2]
        k2v = [a2[i] * self.dt for i in range(self.len_n)]
        k2x = [(body.v + k1v[i]/2) * self.dt for i, body in enumerate(nbody2)]

        nbody3 = NBody([Body(body.m, body.r.x + k2x[i].x / 2, body.r.y + k2x[i].y / 2, body.v.x + k2v[i].x / 2, body.v.y + k2v[1].y / 2)
                        for i, body in enumerate(self.n_body.n_body)
        ])
        nbody3.compute_resultante()
        a3 = [body.res_force / body.m for body in nbody3]
        k3v = [a3[i] * self.dt for i in range(self.len_n)]
        k3x = [(body.v + k2v[i] / 2) * self.dt for i, body in enumerate(nbody3)]

        nbody4 = NBody([Body(body.m, body.r.x + k3x[i].y, body.r.y + k3x[i].y, body.v.x + k3v[i].x, body.v.y + k3v[1].y)
                       for i, body in enumerate(self.n_body.n_body)
        ])
        nbody4.compute_resultante()
        a4 = [body.res_force / body.m for body in nbody4]
        k4v = [a4[i] * self.dt for i in range(self.len_n)]
        k4x = [(body.v + k3v[i]) * self.dt for i, body in enumerate(nbody4)]

        for i, body in enumerate(self.n_body.n_body):
            body.v += 1/6 * (k1v[i] + 2*k2v[i] + 2*k3v[i] + k4v[i])
            body.r += 1/6 * (k1x[i] + 2*k2x[i] + 2*k3x[i] + k4x[i])
            #if self.t > 0.217 and self.t < 0.218:
                #print("pos lune", self.n_body.n_body[1].r.x, self.n_body.n_body[1].r.y, "pos apollo", self.n_body.n_body[2].r.x, self.n_body.n_body[2].r.y)

        self.t += self.dt

class RK_final2:
    def __init__(self, dt, n_body):
        self.dt = dt
        self.t = 0
        self.n_body = n_body
        self.len_n = len(self.n_body.n_body)

    def RK_new_step(self, factor, kx_avant, kv_avant):
        n_body = NBody([
            Body(body.m, body.r.x + kx_avant[i].x * factor, body.r.y + kx_avant[i].y * factor, body.v.x + kv_avant[i].x * factor,
                    body.v.y + kv_avant[i].y * factor)
            for i, body in enumerate(self.n_body.n_body)
        ])
        n_body.compute_resultante()
        a = [body.res_force / body.m for body in n_body]
        kv = [a[i] * self.dt for i in range(self.len_n)]
        kx = [(body.v + kv_avant[i] * factor) * self.dt for i, body in enumerate(n_body)]

        return kx, kv

    def get_new_positions(self):
        print((self.n_body.n_body[1].r-self.n_body.n_body[0].r).norm())
        k1x, k1v = self.RK_new_step(1, [Vector(0, 0)]*self.len_n, [Vector(0, 0)]*self.len_n)
        k2x, k2v = self.RK_new_step(1/2, k1x, k1v)
        k3x, k3v = self.RK_new_step(1/2, k2x, k2v)
        k4x, k4v = self.RK_new_step(1, k3x, k3v)

        for i, body in enumerate(self.n_body.n_body):
            body.v += 1/6 * (k1v[i] + 2 * k2v[i] + 2 * k3v[i] + k4v[i])
            body.r += 1/6 * (k1x[i] + 2 * k2x[i] + 2 * k3x[i] + k4x[i])
        self.t += self.dt


class RK_2Integrator:
    def __init__(self, dt, n_body: NBody):
        self.dt = dt
        self.t = 0
        self.n_body = n_body
        self.len_n = len(self.n_body.n_body)

    def get_new_positions(self):
        for body in self.n_body.n_body:
            r_i = body.r + self.dt**2 / 2 * body.v * (1 + self.dt**2 / 2)
            body.r = r_i
        self.n_body.compute_resultante()
        for body in self.n_body.n_body:
            a_i = body.res_force / body.m
            v_i = body.v + self.dt ** 2 / 2 * a_i * (1 + self.dt ** 2 / 2)
            body.v = v_i
        self.t += self.dt


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
    new_pos2 = integrator.get_new_positions()
    for pos in new_pos2:
        print(pos.x, pos.y)

    for pos, step in zip(new_pos2, step_two):
        print(pos.x, pos.y)
        assert pos == step


if __name__ == "__main__":
    test_integrator()

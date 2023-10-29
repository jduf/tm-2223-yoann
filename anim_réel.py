from nbody import NBody, Body, Active_Body
from anim import Anim
import integrator

# 4 unités = 380 000 km
# orbite de parquage autour terre = 185,2 + 6371 km =~ 0.069 unités
# moteur saturn 5 poussée = 6.77e6 N

n_body = NBody(
    [
            Body(597, 0, 0, 0, 0),
            Body(7.34, 4, 0, 0, 12.21679),
            Active_Body(0.2887e-17, 0, -0.069, 107.437192,
                        39.995938, 0.002678, 10, False)
    ]
)
integrator = integrator.BaseIntegrator(0.001, n_body)
anim = Anim(integrator)
anim.go(1)

# avec un depart depuis une orbite de la terre
# 60.91213 26.28682
# 60.97561 26.24743
# 60.88594 26.36512
# 60.88548 26.3684
# 60.93973 26.25656
# 60.73182 26.37955

# ajustement pour bonne durée TLI
# 52.14554, 41.73039
# 52.16908, 41.69628
# 52.14836, 41.73467
# 52.14483, 41.74083
# 52.12725, 41.76994
# 51.53146, 41.7082#
# vitesse lune avec RK4_Integrator : 12.42156

# avec BaseIntegrator ou RK4_final
# pour BseIntegrator: 105.412113, 43.33549
# Ca devrait ressembler à un truc comme ça 120.925, -58.396
# 120.831801, -58.399155 score: 127.12998182245744
# 120.873657, -58.31436
# 120.868546, -58.324764
# 120.928594, -58.401248
# 118.76168, -62.92793
# 119.74375, -60.72582


# pour le retour
# 9.29595, -16.117 score: 13.29421183539738
# 9.27417, -16.133 score: 13.29477263045773
# 9.30122, -14.674 score: 13.295429304133346

# avec Verlet
# 16.795, 17.187

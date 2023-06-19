from nbody import (NBody, Body)
from anim import Anim
from integrator import *

n_body = NBody(
    [
            Body(597, 0, 0, 0, 0),
            Body(7.34, 4, 0, 0, 12),
            Body(0.2887e-17, 0, 0, 59.2626, 28.4432)
    ]
)
integrator = RK_4Integrator_reel(0.1, n_body, 8e-16)
anim = Anim(integrator)
anim.go(100)
# 59.2822 28.4103 (donne environ 16 périodes stable vitesse plutôt régulière)
# 59.2577 28.4273 (rotation plus rapide)
# 59.2863 28.4038 (rota plus lente au début)

# à partir de maintenant stable au moins jusqu'à t=40
# 59.2626 28.4432
# 59.2547 28.4407 (rayon rota plus serré, à comparer à des valeurs réelles)
# 59.2613 28.4379

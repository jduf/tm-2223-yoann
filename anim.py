import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from integrator import BaseIntegrator

# Pour effectuer l'animation je vous propose d'utiliser FuncAnimation de
# matplotlib. L'idée de base de cette fonction est d'appeler une fonction de
# mise à jour à chaque nouvelle frame (image). 
# Vous prouvez trouver de la documentation sur les sites suivants:
# https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
# https://www.geeksforgeeks.org/matplotlib-animation-funcanimation-class-in-python/


class Anim:
    def __init__(self, integrator):
        """Prépare l'animation"""
        self.integrator = integrator
        self.fig, self.ax = plt.subplots()  # crée une figure
        self.ax.set_xlim(-10, 10)  # définit la longueur de l'axe x
        self.ax.set_ylim(-10, 10)  # définit la longueur de l'axe y
        # initialise chaque position à afficher
        self.display_pos = [
            self.ax.plot([], [], 'o')[0]
            for _ in self.integrator.n_body
        ]

    def _update(self, frame):
        """
        Pour chaque self.display_pos, utilise set_data pour fixer la position
        au pas de temps suivant créé par self.integrator.get_new_positions().
        Retourne ensuite self.display_pos.
        """
        new_positions = self.integrator.get_new_positions()
        print("énergie mécanique :", self.integrator.n_body.compute_emec(),
              "temps écoulé :", self.integrator.t)
        for i, body in enumerate(self.integrator.n_body):
            x, y = new_positions[i].x, new_positions[i].y
            self.display_pos[i].set_data(x, y)

        return self.display_pos

    def go(self, interval: int):
        """
        Affiche l'animation en choisissant l'intervalle de temps entre chaque
        frame
        """
        self.anim = FuncAnimation(
            fig=self.fig,
            func=self._update,
            interval=interval,
            repeat=False,
            cache_frame_data=False,
        )
        plt.show()


def test_anim():
    from nbody import (
        NBody,
        Body
    )
    from integrator import BaseIntegrator
    n_body = NBody(
        [
            Body(100, 0, 0, 0, 0),
            Body(1, 5, 0, 0, 5),
            Body(0.1, 0.1, 0, 0, 20)
        ]
    )
    integrator = BaseIntegrator(0.01, n_body)
    anim = Anim(integrator)
    anim.go(10)

if __name__ == "__main__":
    test_anim()

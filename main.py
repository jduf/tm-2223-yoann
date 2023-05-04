import tkinter
from tkinter import *
import math
from distance_matrix import DistanceMatrix

# create the GUI
window = Tk()
window.config(background='black')
window.geometry("1080x720")
window.title("Gravitation's simulation")


f = Frame(bg='black', width=800, height=40)
b = Button(f, text="Launch simulation", activebackground='red', bg='black', foreground='white', bd=8,
           font="Consolas 20")
# add the option (command = "function") to the button to call a function when button is clicked
b_moon = Button(f, text="With the moon moving", activebackground='red', bg='black', foreground='white', bd=6,
                 font="Consolas 20")
b_pause = Button(f, text="Pause/Restart", activebackground='red', bg='black', foreground='white', bd=6,
                 font="Consolas 20")
b_quit = Button(f, text="Quit", activebackground='red', bg='black', foreground='white', bd=6,
                 font="Consolas 20", command=window.destroy)

L = Label(window, text="Apollo VIII travel's simulation", font="Consolas 25", bg='black', fg='white')
c = tkinter.Canvas(f, bg='black', height=1200, width=1600, bd=8)
c.create_arc(300, 300,350, 350, start=0, extent=360, fill='white') # Earth = r2



# m2 = 732784  # real earth mass
# G = 6.67 * 10 ** -11
# time_interval = 0.01  # seconds
# coefficient_transfo_pixel_vers_mètre = 717272
# x_r1 = 122 * coefficient_transfo_pixel_vers_mètre # object1's x_position in pixels
# x_r2 = 743 * coefficient_transfo_pixel_vers_mètre # objects2's x_position in pixels
# y_r1 = 532 * coefficient_transfo_pixel_vers_mètre # object1's y_position in pixels
# y_r2 = 232 * coefficient_transfo_pixel_vers_mètre # objects2's y_position in pixels


# class Astre:
    # def __init__(self, x_speed):
        # self.x_speed += (G * m2 * time_interval) / (x_r1 - x_r2)  # projeté sur axe x

    # def __init__(self, x_position):
       # self.x_position += self.x_speed * time_interval

    # def __init__(self, y_speed):
       # self.y_speed += (G * m2 * time_interval) / (y_r1 - y_r2)  # projeté sur axe y

    # def __init__(self, y_position):
       # self.y_position += self.y_speed * time_interval


# def apollo_trajectory():
# create circle at(x=x_r1, y=y_r1, diameter=4)
#  while x_r1!=x_r2 and y_r1!=y_r2 :
# wait time_interval
# create circle2 at(x=x_r1, y=y_r1, diameter=4)
# c.create_line(x_r1, y_r1, x_r2, y_r2, fill='white')
# delete circle
# circle2 = circle


#for i in range(1000000):
    # x_speed += (G * m2 * time_interval) / (x_r1 - x_r2)
    # y_speed += (G * m2 * time_interval) / (y_r1 - y_r2)
    # x_position += self.x_speed * time_interval
    # y_position += self.y_speed * time_interval
class Vector:
    
    def __init__(self, x: float, y: float) -> None:
      
        self.x = x
        self.y = y
        ...

    def __add__(self, other):
        
        self.add = self.other = Vector(0,0)
        self.other = other
        self.add.x = self.x + self.other.x
        self.add.y = self.y + self.other.y
        return(self.add)
    
    def __sub__(self, other):
      
        self.sub = self.other = Vector(0,0)
        self.other = other
        self.sub.x = self.x - self.other.x
        self.sub.y = self.y - self.other.y
        return(self.sub)
        ...

    def __neg__(self):
        
        self.neg = Vector(0, 0)
        self.neg.x = -self.x
        self.neg.y = -self.y
        return(self.neg)
        ...

    def __mul__(self, a):
        
        self.mul = Vector(0, 0)
        self.mul.x = self.x * a
        self.mul.y = self.y * a
        return(self.mul)
        ...

    __rmul__ = __mul__

    def __eq__(self, other):
       
        self.other = Vector(0, 0)
        self.other = other
        
        if self.other.x == self.x and self.other.y == self.y:
            return(True)
        else:
            return(False)
        ...

    def norm_squared(self):
       
        norm_squared = ((self.x)**2 + (self.y)**2)
        return(norm_squared)
        ...
 
    def norm(self):
        norm = math.sqrt((self.x)**2 + (self.y)**2)
        # norm = ((self.x)**2 + (self.y)**2)**(1/2)
        return(norm)
        ...

    def dot(self, other):
        self.other = Vector(0, 0)
        self.other = other
        dot = self.x * self.other.x + self.y * self.other.y
        return(dot)
        ...
    
    def __truediv__(self, d):
        self.div = Vector(0, 0)
        self.div.x = self.x / d
        self.div.y = self.y / d
        return(self.div)
    
    def angle(self, other):
        self.other = Vector(0, 0)
        self.other = other
        angle = math.acos((self.x * self.other.x + self.y * self.other.y)/
                          (math.sqrt((self.x)**2 + (self.y)**2) * 
                           math.sqrt((self.other.x)**2 + (self.other.y)**2)))
        angle = math.degrees(angle)
        return(angle)
        
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    # angle entre la droite formée par les deux points et l'horizontale
    def angle_points(self, other):
        self.other = Point(0, 0)
        self.other = other
        angle_points = math.atan((self.y-self.other.y)/(self.x-self.other.x))
        angle_points = math.degrees(angle_points)
        return(angle_points)
    
    def distance(self, other):
        self.other = Point(0, 0)
        self.other = other
        distance = math.sqrt((self.x-self.other.x)**2 + (self.y-self.other.y)**2)
        return(distance)
        
        
class Force:
    def __init__(self, f, angle):
        self.f = f
        self.angle = angle
    def vectorisation_force(self, f, angle):
        force = Vector(0, 0)
        force.x = self.f * math.cos(self.angle)
        force.y = self.f * math.sin(self.angle)
        return(force)
    
class Acceleration:
    def __init__(self, force, masse):
        self.force = Vector(0, 0)
        self.force = force
        self.masse = masse
        
    def acceleration(self, force, masse):
        acceleration = Vector(0, 0)
        acceleration.x = force.x / masse
        acceleration.y = force.y / masse
        return(acceleration)
    
class Vitesse:
    def __init__(self, acceleration, delta_t):
        self.acceleration = Vector(0, 0)
        self.acceleration = acceleration
        self.delta_t = delta_t
        
    def vitesse(self, acceleration, delta_t):
        vitesse = Vector(0, 0)
        vitesse.x = acceleration.x * delta_t
        vitesse.y = acceleration.y * delta_t 
        return(vitesse)
        
class Position:
    def __init__(self, vitesse, delta_t):
        self.vitesse = Vector(0, 0)
        self.vitesse = vitesse 
        self.delta_t = delta_t
        
    def position(self, vitesse, delta_t):
        position = Point(0, 0)
        position.x = vitesse.x * delta_t
        position.y = vitesse.y * delta_t
        return(position)
        
"""def force_sur_Apollo():
	force_sur_Apollo = Vector(0, 0)
	force_sur_Apollo = (G*m_terre*m_Apollo)/(distance(r_terre, r_Apollo))**2 + (G*m_lune*m_Apollo)/(distance(r_lune, r_Apollo))**2"""
	

while True:
	r_terre = Point(0, 0)
	r_Apollo = Point(0, 500)
	force_sur_Apollo = force_sur_Apollo()
	unitaire_x = Vector(1, 0)
	angle_f_Apollo = angle_points(r_Apollo, r_terre)
	vectorisation_force
	
"""def RK_ordre4(n_Body: list):
	dt = 0.1
	G = 1
	n_Body.r.update()
	len.body = len(n_Body)
	forces = []
	for j in range(len.body):
		for i in range(len.body):
			rij = n_Body.r._get(i, j)
			fij = G * n_Body.m[i] * n_Body.m[j] * rij.r_over_rcube
			forces.append(fij)
			
	for i in range(len.body):
	
		forces_sur_i = [forces[i, j] for j in range(len.body)] 
		force_sur_i = sum(forces_sur_i)
		a_i = force_sur_i/ n_Body.m[i]

		F1 = n_Body.r[i]
		F2 = 0.5 * a_i *dt**2 / 4 + n_Body.v[i] * dt / 2 + F1 * dt / 2
		F3 = 0.5 * a_i *dt**2 / 4 + n_Body.v[i] * dt / 2 + F2 * dt / 2
		F4 = 0.5 * a_i *dt**2 + n_Body.v[i] * dt + F3 * dt
		r_i = n_Body.r[i] + 1/6 * (F1+2*F2+2*F3+F4)*dt
		n_Body.r[i] = r_i
		
		F1_v = n_Body.v[i]
		F2_v = a_i * dt/2 + n_Body.v[i] + n_Body.v[i] * dt/2
		F3_v = a_i * dt/2 + n_Body.v[i] + F2_v * dt/2
		F4_v = a_i * dt + n_Body.v[i] + F3_v * dt 
		v_i = n_Body.v[i] + dt/6 * (F1_v + 2*F2_v + 2*F3_v + F4_v)
		n_Body.v[i] = v_i"""
	

c.pack(side=tkinter.TOP)
L.pack(side=tkinter.TOP)
f.pack(side=tkinter.BOTTOM)
b_quit.pack(side=tkinter.RIGHT)
b.pack(side=tkinter.LEFT)
b_pause.pack(side=tkinter.RIGHT)
b_moon.pack()

window.mainloop()
"""import math 
import numpy as np 
class ApolloEnvironment: 
	def __init__(self): 
	    self.fuel = 5000 # quantité de carburant maximale en kg 
		self.mass = 28801.7 # masse du vaisseau en kg 
		self.gravity = 1.62 # accélération de la gravité lunaire en m/s^2 
		self.time_step = 0.1 # temps écoulé à chaque étape en secondes 
		self.velocity = Vector(0, 0) # vitesse du vaisseau en m/s 
		self.position = Vector(0, 0n) # position du vaisseau en m 
		self.goal_position = np.array([384400, 0]) # position de l'objectif (la Lune) 
		self.thrust = 0 # force de poussée du moteur en Newtons 
		self.engine_on = False # moteur allumé ou éteint 
		self.engine_duration = 0 # temps depuis le début de l'allumage du moteur 
		self.engine_max_duration = 20 # durée maximale d'allumage du moteur en secondes 
		self.engine_max_thrust = 15000 # force maximale de poussée du moteur en Newtons 
		self.engine_fuel_consumption = 100 # consommation de carburant par seconde en kg 
		self.engine_fuel_consumed = 0 # quantité de carburant consommée depuis le début de l'allumage du moteur 
	
	def step(self, action): 
		assert action in [-1, 0, 1], "Action doit être -1, 0 ou 1." 
		if action == 1: 
			self.thrust = self.engine_max_thrust 
			self.engine_on = True 
			self.engine_duration = min(self.engine_duration + self.time_step, self.engine_max_duration) 
			self.engine_fuel_consumed += self.engine_fuel_consumption * self.time_step 
			self.fuel = max(0, self.fuel - self.engine_fuel_consumption * self.time_step) 
			
		elif action == -1: 
			self.thrust = 0
			self.engine_on = False 
			self.engine_duration = 0 
			
		else: 
			self.thrust = 0 
			self.engine_on = True 
			self.engine_duration = min(self.engine_duration + self.time_step, self.engine_max_duration) 
			self.engine_fuel_consumed += self.engine_fuel_consumption * self.time_step 
			self.fuel = max(0, self.fuel - self.engine_fuel_consumption * self.time_step) 
			
		self.mass = self.mass - self.engine_fuel_consumed 
			
		acceleration = np.array([0, -self.gravity]) + self.thrust / self.mass * np.array([math.cos(math.radians(90)), math.sin(math.radians(90))]) 
		self.velocity += acceleration * self.time_step 
		self.position += self.velocity * self.time_step 
		
		done = False 
		if np.linalg.norm(self.position - self.goal_position) <= 1000: 
			done = True 
			
		if self.fuel <= 0: 
			done = True 
		
		reward = -np.linalg.norm(self.position - self.goal_position) 
		return self.position, reward, done, {}"""
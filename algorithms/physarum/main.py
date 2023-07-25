import math
import random

import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
import matplotlib.animation as animation


def simple_mean_filter(array):
    # Create an output array of the same shape as the input array
    output = np.zeros_like(array)

    # Get the dimensions of the input array
    rows, cols = array.shape

    # Iterate over each pixel in the input array
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # Extract the 3x3 kernel centered at the current pixel
            kernel = array[i-1:i+2, j-1:j+2]

            # Compute the mean of the kernel and assign it to the corresponding pixel in the output array
            output[i, j] = np.mean(kernel)

    return output

class Agent:
    def __init__(self, SO, SA, RA, SS, pos, env, L, W):
        self.SO = SO
        self.SA = SA
        self.RA = RA
        self.SS = SS
        self.CA = 2*np.pi*np.random.random()
        self.pos = pos
        self.env = env
        self.L = L
        self.W = W
        self.strength = 1

    def move(self):
        delta_x = self.SS * np.cos(self.CA)
        delta_y = self.SS * np.sin(self.CA)
        point = np.where(self.pos + np.array([round(delta_x), round(delta_y)], dtype=int)>self.L-1,self.L-1,self.pos + np.array([round(delta_x), round(delta_y)], dtype=int))
        try:
            if env.isValid(point):
                env.dmap[point[0],point[1]] = 1
                env.dmap[self.pos[0],self.pos[1]] = 0
                self.pos = point
                env.tmap[self.pos[0],self.pos[1]] = self.strength
            else:
                self.CA = 2*np.pi*np.random.random()
                self.pos = self.pos
        except:
            self.CA = 2*np.pi*np.random.random()
    def sense(self):
        h, w = env.tmap.shape
        n, m = self.pos
        Fr_sensor = np.array([round(self.SO*np.cos(self.CA+self.SA)), round(self.SO*np.sin(self.CA+self.SA))])
        Fl_sensor = np.array([round(self.SO*np.cos(self.CA-self.SA)), round(self.SO*np.sin(self.CA-self.SA))])
        F_sensor = np.array([round(self.SO * np.cos(self.CA)), round(self.SO * np.sin(self.CA))])
        F = env.tmap[(n-F_sensor[0])%h, (m-F_sensor[1])%w]
        Fr = env.tmap[(n-Fr_sensor[0])%h, (m-Fr_sensor[1])%w]
        Fl = env.tmap[(n-Fl_sensor[0])%h, (m-Fl_sensor[1])%w]
       # print(self.pos, [(n-F_sensor[0])%h, (m-F_sensor[1])%w], [(n-Fr_sensor[0])%h, (m-Fr_sensor[1])%w], [(n-Fl_sensor[0])%h, (m-Fl_sensor[1])%w])
        if (F > Fl) & (F > Fr):
            pass
        elif (F < Fl) & (F < Fr):
            if np.random.randint(0,2) == 1:
                self.CA -= self.RA
            else:
                self.CA += self.RA
        elif (Fl < Fr):
            self.CA += self.RA
        elif (Fr < Fl):
            self.CA -= self.RA
        else:
            pass


class Environment:
    def __init__(self, L=200, W=200, pp=0.07, fp=0.1, strength=3):
        self.L = L
        self.W = W
        self.fp = fp
        self.strength = strength
        self.dmap = np.zeros(shape=(L, W))
        self.tmap = np.zeros(shape=(L, W))
        self.pop = int((L*W)*pp)
        self.agents = []

    def populate(self, SO=9, SA=np.pi/8, RA=np.pi/4, SS=1):
        while len(self.agents) < self.pop:
            rL = np.random.randint(0,self.L)
            rW = np.random.randint(0,self.W)
            if self.dmap[rL, rW] == 0:
                self.dmap[rL, rW] = 1
                self.agents.append(Agent(SO, SA, RA, SS, [rL, rW], self, self.L, self.W))

    def deposit_random_food(self, strength=3):
        S = strength
        N = int((self.L*self.W)*self.fp)
        array = self.tmap
        mask = np.zeros_like(array)
        indices = np.random.choice(np.arange(array.size), N, replace=False)
        mask.flat[indices] = 1
        array[mask.astype(bool)] = S

    def deposit_circular_food(self, radius=6):
        shape = self.tmap.shape
        center = (shape[0] // 2, shape[1] // 2)
        Y, X = np.ogrid[:shape[0], :shape[1]]
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)
        mask = dist_from_center <= radius
        self.tmap[mask] = self.strength*10

    def diffuse_trail_map(self, sigma=0.6, alpha=2):
        # https://github.com/ecbaum/physarum/blob/8280cd131b68ed8dff2f0af58ca5685989b8cce7/species.py#L52
        # self.tmap = simple_mean_filter(self.tmap)
        self.tmap = alpha * ndimage.gaussian_filter(self.tmap,sigma)

    def isValid(self, point):
        if self.dmap[point[0],point[1]].any() != 1:
            return True
        else:
            return False

    def motor_stage(self):
        self.agents = random.sample(self.agents, len(self.agents))
        for agent in self.agents:
            agent.move()

    def sensory_stage(self):
        self.agents = random.sample(self.agents, len(self.agents))
        for agent in self.agents:
            agent.sense()


if __name__ == "__main__":
    env = Environment()
    env.populate()
    fig, ax = plt.subplots()
    im = plt.imshow(env.tmap)
    """def update(f):
        env.motor_stage()
        env.sensory_stage()
        env.diffuse_trail_map()
        im = plt.imshow(env.tmap)
        return im
    animation = animation.FuncAnimation(fig, update)
    plt.show()
    """
    for i in range(96):
        env.motor_stage()
        env.sensory_stage()
        env.diffuse_trail_map()
    plt.imshow(env.tmap)
    plt.show()
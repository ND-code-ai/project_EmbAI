import numpy as np
import pygame
import time, threading
from threading import Timer

from typing import Tuple
from experiments.aggregation.config import config

from simulation.agent import Agent
from experiments.aggregation.config import config
from simulation.utils import *


class Cockroach(Agent):
    """ """
    def __init__(
            self, pos, v, aggregate, index: int, image: str = "experiments/aggregation/images/ant.png"
    ) -> None:

        super(Cockroach, self).__init__(
            pos,
            v,
            image,
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=config["agent"]["width"],
            height=config["agent"]["height"],
            dT=config["agent"]["dt"],
            index=index
        )

        self.aggregation = aggregate
        self.state = "wander"




    def change_state(self, state) -> None:
        state = self.state
        for obstacle in self.flock.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.sensing = "site"

        if state == "wander":
            force = self.wander(wander_dist, wander_radius, wander_angle)
        elif state == "still":
            self.max_speed, self.min_speed = 0, 0
        #elif state == "leave":






    def site_behavior(self) -> None:
        for site in self.aggregations.objects.sites:
            collide = pygame.sprite.collide_mask(self, site)
            if bool(collide):
                sensing = "site"
        join_constant = 0.3
        num_neighbors =  len(self.flock.find_neighbors(self, config["cockroach"]["radius_view"]))
        p_join = min(1, num_neighbors / 100 + join_constant)

        #join state
        if sensing == "site" and p_join > np.random.rand() :
            r = np.random.uniform(0, 0.5) #random noise
            time.sleep(0.3 + r) #time function for join -> still
            self.change_state(state="still")
        else:
            self.change_state(state="wander")

            #join behavior



            #leave



    def update_actions(self) -> None:
        # calculate how many seconds
              # if more than 10 seconds close the game

            #print(seconds)  # print how many seconds
            for obstacle in self.aggregation.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    self.avoid_obstacle()

            count = self.read_counter()
            for site in self.aggregation.objects.sites:
                col = pygame.sprite.collide_mask(self, site)
                if bool(col):
                    self.write_counter(count)
                    if count == 5:
                        self.reset_counter()
                        self.min_speed = 0
                        self.max_speed = 0



        #if self.max_speed == 0 and self.min_speed == 0:

           # if self.max_speed == 0:

                #threading.Timer(1.0)
                #num_neighbors = len(self.flock.find_neighbors(self, config["cockroach"]["radius_view"]))
               # p_leave = min(1, num_neighbors / 100 + leave_constant)
                #self.change_state(state="leave")

    def reset_counter(self):
        file = open(
            r'experiments/aggregation/Counter.txt',
            'r+')
        file.seek(0)
        file.truncate()
        file.write('%d' % 0)
        file.close()


    def read_counter(self):
        # Read Counter
        file = open(
            r'experiments/aggregation/Counter.txt')
        read_input = file.read()
        file.close()
        count = int(read_input)
        return count

    def write_counter(self,count):
        #count = self.read_counter()
        file = open(
            r'experiments/aggregation/Counter.txt',
            'r+')
        file.seek(0)
        file.truncate()
        file.write('%d' % (count + 1))
        file.close()
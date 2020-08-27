#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:41:39 2020

@author: stellarremnants
"""

import numpy as np
from copy import copy
import PhysLab_Utility_Functions as puf


# =============================================================================
# BASE OBJECT DEFAULTS
# =============================================================================

DEFAULT_POSITION=np.asarray([0,0,0], dtype=float)
DEFAULT_VELOCITY=np.asarray([0,0,0], dtype=float)
DEFAULT_FORCE=np.asarray([0,0,0], dtype=float)
DEFAULT_RADIUS=0.1
DEFAULT_FPS = 60
DEFAULT_MASS = 1
DEFAULT_DT=DEFAULT_FPS**-1
DEFAULT_FLAGS_DICT={
        "movable":True,
        "collide_walls":True,
        "collide_objects":True,
        "point_mass":True,
        }

# =============================================================================
# BASE OBJECT DEFINITION
# =============================================================================

class base_object:
    name_counter = 0
    
    def enforce_float(self):
        self.position.dtype = float
        self.velocity.dtype = float
        
    def __str__(self):
        return_string = f"{self.name}<"
        return_string += "r="+str(self.position)+", "
        return_string += "v="+str(self.velocity)+", "
        return_string += "m="+str(self.mass) + ">"
        return return_string
        
    def __repr__(self):
        return self.__str__()
    
    def __init__(self,
                 position=copy(DEFAULT_POSITION),
                 velocity=copy(DEFAULT_VELOCITY),
                 radius=DEFAULT_RADIUS,
                 mass = DEFAULT_MASS,
                 flags_dict=copy(DEFAULT_FLAGS_DICT),
                 name=None):
        self.position=copy(position)
        self.velocity=copy(velocity)
        self.radius=radius
        self.flags_dict = copy(flags_dict)
        self.mass = mass
        if len(self.position) != len(self.velocity):
            raise ValueError("Position and velocity must have the same dimensions")
            
        self.enforce_float()
            
        if name is None:
            self.name = f"object#{base_object.name_counter}"
            base_object.name_counter += 1
        else:
            self.name = name
        
    def dimensions(self):
        
        if len(self.position) != len(self.velocity):
            raise ValueError("Position and velocity must have the same dimensions")
        else:
            return len(self.position)
        
    def update_position(self, dt=DEFAULT_DT):
        self.enforce_float()
        self.position += self.velocity * dt
            
    def update_velocity(self, force = DEFAULT_FORCE, dt=DEFAULT_DT):   
        self.enforce_float()
        if len(self.velocity) != len(force):
            raise ValueError("Force and velocity must have the same dimensions")
        else:
            if puf.VERBOSE:
                print(f"{self.name}: previous velocity {self.velocity}")
            dv = force / self.mass * dt
            self.velocity += dv
            if puf.VERBOSE:
                print(f"dv={dv}, ", end="")
                print()
                print(f"{self.name}: new velocity {self.velocity}")
                
    def plot(self, ax, velocity_scale=.05, radius_scale=50):
        ax.scatter(*self.position, s=self.radius*radius_scale)
        starting_point = self.position
        numpoints=10
        line_points = np.zeros([len(self.position), numpoints])
        for i in range(len(starting_point)):
            line_points[i, :] = np.linspace(starting_point[i], starting_point[i]+self.velocity[i]*velocity_scale, numpoints)
        ax.plot(*line_points)
            
            
            
            
            
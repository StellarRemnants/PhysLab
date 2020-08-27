# -*- coding: utf-8 -*-

import PhysLab_Utility_Functions as puf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =============================================================================
# PHYSICS BOX DEFAULTS
# =============================================================================

DEFAULT_BOUNDARIES = {
        "shape":"rectangle",
        "left":0,
        "right":1,
        "bottom":0,
        "top":1
        }

# =============================================================================
# PHYSICS BOX DEFINITION
# =============================================================================
class physics_box:
    
    def __str__(self):
        return_string = ""
        return_string += "Physics Box Objects\n"
        return_string += "===================\n"
        for obj in self.objects_list:
            return_string += str(obj) + "\n"
        return_string += "===================\n"
        return return_string
        
    def __repr__(self):
        return self.__str__()
    
    def __init__(self, boundaries=DEFAULT_BOUNDARIES,
                 objects_list=[], forces_list=[], dimensions=3):
        self.boundaries=boundaries
        self.objects_list=objects_list
        self.forces_list = forces_list
        self.dimensions=dimensions
        self.validate_object_list()
        self.create_plot()
        
    
    def update_positions(self, dt):
        for physics_object in self.objects_list:
            physics_object.update_position(dt)
            
    def update_velocities(self, dt):
        if len(self.objects_list) > 0:
            force_list = np.zeros([len(self.objects_list), self.objects_list[0].dimensions()])
            for force in self.forces_list:
                force_list += force.calculate_forces(self.objects_list)
            for i in range(len(self.objects_list)):
                self.objects_list[i].update_velocity(force_list[i], dt)
                
    def step_time(self, dt):
        self.update_positions(dt)
        self.update_velocities(dt)
    
    def validate_object_list(self):
        dimensions_valid = True
        for invalid_object in self.validate_object_list_dimensions():
            print(f"ERROR: {invalid_object.name} contains incorrect number of dimensions")
            dimensions_valid=False
        if not dimensions_valid:
            raise Exception("ERROR: at least one object in objects_list is invalid")
        
    def validate_object_list_dimensions(self):
        for obj in self.objects_list:
            if self.dimensions != obj.dimensions():
                yield obj
    
    def create_plot(self):
        self.fig = plt.figure()
        self.plottable = True
        if self.dimensions == 3:
            self.ax = self.fig.add_subplot(111, projection='3d')
            self.plot_box()
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.set_zlabel("z")
            
        elif self.dimesnsions == 2:
            self.ax = self.fig.add_subplot(111)
            for obj in self.objects_list:
                self.ax.scatter(*obj.position)
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
        else:
            self.plottable = False
        
    def plot_box(self):
        if self.plottable:
            self.ax.cla()
            self.ax.scatter(*np.zeros(self.dimensions), marker="^", color="k")
            for obj in self.objects_list:
                obj.plot(self.ax, velocity_scale=.5, radius_scale=50)
                
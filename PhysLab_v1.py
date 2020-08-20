# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

import numpy as np
import time
from copy import copy


# =============================================================================
# UTILITY FUNCTION DEFAULTS
# =============================================================================

DEFAULT_INTEROBJECT_FORCE_CONSTANT = -1
DEFAULT_UNIVERSAL_FORCE_CONSTANT = 1
DEFAULT_DIRECTION_VECTOR = np.asarray([0,-1,0], dtype=float)
VERBOSE = 0

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
# UTILITY FUNCTIONS
# =============================================================================

def np_vect_mag(np_vect):
    return np.sqrt(np_vect.dot(np_vect))

def DEFAULT_INTEROBJECT_FORCE_LAW(object_1, object_2, **kwargs):
    if "force_constant" in kwargs.keys():
        force_constant = kwargs["force_constant"]
    else:
        force_constant = DEFAULT_INTEROBJECT_FORCE_CONSTANT
    vector_1_to_2 = object_2.position-object_1.position
    inter_distance = np_vect_mag(vector_1_to_2)
    unit_vector_1_to_2 = vector_1_to_2/inter_distance
    
    force_magnitude = force_constant / (inter_distance**2)
    force_on_object_1 = force_magnitude * unit_vector_1_to_2
    force_on_object_2 = -1 * force_on_object_1
    return force_on_object_1, force_on_object_2

def DEFAULT_UNIVERSAL_FORCE_LAW(object_1, **kwargs):
    if "force_constant" in kwargs.keys():
        force_constant = kwargs["force_constant"]
    else:
        force_constant = DEFAULT_UNIVERSAL_FORCE_CONSTANT
    
    if "direction_vector" in kwargs.keys():
        direction_vector = kwargs["direction_vector"]
    else:
        direction_vector = DEFAULT_DIRECTION_VECTOR
    
    force_on_object_1 = force_constant * direction_vector
    
    return force_on_object_1
    

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
            if VERBOSE:
                print(f"{self.name}: previous velocity {self.velocity}")
            dv = force / self.mass * dt
            self.velocity += dv
            if VERBOSE:
                print(f"dv={dv}, ", end="")
                print()
                print(f"{self.name}: new velocity {self.velocity}")
                
                
class inter_object_force:
    
    def __init__(self, flags_list=[], force_law=copy(DEFAULT_INTEROBJECT_FORCE_LAW), **force_law_args):
        self.flags_list = flags_list
        self.force_law=force_law
        self.force_law_args = force_law_args
        
    def calculate_forces(self, object_1, object_2):
        valid_combintation=True
        
        for flag in self.flags_list:
            if flag not in object_1.flags_dict:
                valid_combintation = False
                break
            if flag not in object_2.flags_dict:
                valid_combintation = False
                break
            
        if valid_combintation:
            force_on_object_1, force_on_object_2 = self.force_law(object_1, object_2, **self.force_law_args)
            return force_on_object_1, force_on_object_2
        else:
            return np.zeros_like(object_1.position), np.zeros_like(object_2.position)
        
        
class universal_force:
    
    def __init__(self, flags_list=[], force_law = DEFAULT_UNIVERSAL_FORCE_LAW, **force_law_args):
        self.flags_list = flags_list
        self.force_law=force_law
        self.force_law_args = force_law_args
        
    def calculate_forces(self, object_1):
        object_1_force_valid = True
        for flag in self.flags_list:
            if flag not in object_1.flags_dict:
                object_1_force_valid = False
                break
            
        if object_1_force_valid:
            force_on_object_1 = self.force_law(object_1, **self.force_law_args)
            return force_on_object_1
        else:
            return np.zeros_like(object_1.position)
                
                
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
                 objects_list=[], inter_object_forces=[], universal_forces=[]):
        self.boundaries=boundaries
        self.objects_list=objects_list
        self.inter_object_forces = inter_object_forces
        self.universal_forces = universal_forces
    
    def update_positions(self, dt):
        for physics_object in self.objects_list:
            physics_object.update_position(dt)
            
    def update_velocities(self, dt):
        num_objects = len(self.objects_list)
        for force in self.inter_object_forces:
            for i in range(num_objects):
                for j in range(i, num_objects):
                    obj1 = self.objects_list[i]
                    obj2 = self.objects_list[j]
                    if i != j:
                        if VERBOSE:
                            print(f"Computing inter_object force for {obj1} & {obj2}")
                        force_1, force_2 = force.calculate_forces(obj1, obj2)
                        if VERBOSE:
                            print(f"Forces are <{force_1}> & <{force_2}>")
                            print()
                        obj1.update_velocity(force_1, dt)
                        obj2.update_velocity(force_2, dt)
                        
        for force in self.universal_forces:
            for obj in self.objects_list:
                force_1 = force.calculate_forces(obj)
                if VERBOSE:
                    print(f"force_1 {force_1}")
                obj.update_velocity(force_1, dt)
    
    def step_time(self, dt):
        self.update_positions(dt)
        self.update_velocities(dt)
    
#%%
object_1 = copy(base_object(position=np.asarray([0,0,1], dtype=float)))
object_2 = copy(base_object(position=np.asarray([0,1,0], dtype=float)))
objects_list = [object_1,object_2]  
#uforce = universal_force()
#test_box = physics_box(objects_list=objects_list, universal_forces=[uforce])
iforce = inter_object_force()
test_box = physics_box(objects_list=objects_list, inter_object_forces=[iforce], universal_forces=[])
print(test_box)

for t in range(5):
    test_box.step_time(1)
    print(test_box)
    time.sleep(.1)
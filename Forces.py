# -*- coding: utf-8 -*-

import numpy as np
from copy import copy
import sys
import PhysLab_Utility_Functions as puf

DEFAULT_INTEROBJECT_FORCE_CONSTANT = -1
DEFAULT_UNIVERSAL_FORCE_CONSTANT = 1
DEFAULT_DIRECTION_VECTOR = np.asarray([0,-1,0], dtype=float)

class force_class:
    
    def __init__(self, flags_list=["movable"], force_constant=1, object_count=2, **force_law_args):
        self.flags_list = flags_list
        self.force_constant=force_constant
        self.object_count = object_count
        self.force_law_args = force_law_args
    
        
    def force_law(self):
        def return_function(object_list, **kwargs):
            if len(object_list) > 0:
                force_list = np.zeros([len(object_list), object_list[0].dimensions()])
                #Calculate forces here
                return force_list
            else:
                return []
        
        return return_function
        
    def calculate_forces(self, object_list):
        forces_list = self.force_law()(object_list, **self.force_law_args)
        return forces_list        
        
    def validate_object(self, obj):
        valid = True
        for flag in self.flags_list:
            if flag not in obj.flags_dict:
                valid=False
                break
        return valid
            
class laminar_drag_force(force_class):
    
    def __init__(self, flags_list=["movable"], force_constant=1, **force_law_args):
        object_count=1
        super().__init__(flags_list, force_constant, object_count, **force_law_args)
        
    def force_law(self):
        def return_function(object_list, **force_law_args):
            total_objects = len(object_list)
            if len(object_list) > 0:
                force_list = np.zeros([len(object_list), object_list[0].dimensions()])
                for i in range(total_objects):
                    if self.validate_object(object_list[i]):                
                        force_list[i] = - self.force_constant * object_list[i].velocity * np.pi * object_list[i].radius**2
                return force_list
            else:
                return []
        return return_function
    
    def calculate_forces(self, object_list):
        return super().calculate_forces(object_list)
    
    def validate_object(self, obj):
        return super().validate_object(obj)
    
class gravitational_force(force_class):
    
    def __init__(self, flags_list=["movable"], force_constant=1, **force_law_args):
        object_count=2
        super().__init__(flags_list, force_constant, object_count, **force_law_args)
        
    def force_law(self):
        def return_function(object_list, **force_law_args):
            total_objects = len(object_list)
            if len(object_list) > 0:
                
                force_list = np.zeros([len(object_list), object_list[0].dimensions()])
                
                for i in range(total_objects):
                    for j in range(i+1, total_objects):
                        if self.validate_object(object_list[i]) and self.validate_object(object_list[j]):     
                            r_i_j = object_list[j].position - object_list[i].position
                            f_i_j = self.force_constant * r_i_j / puf.np_vect_mag(r_i_j)**3
                            force_list[i] += f_i_j
                            force_list[j] -= f_i_j
                        
                return force_list
            
            else:
                return []
        return return_function
    
    def calculate_forces(self, object_list):
        return super().calculate_forces(object_list)
    
    def validate_object(self, obj):
        return super().validate_object(obj)
    
# %%


# =============================================================================
# Default Force Laws
# =============================================================================


#def DEFAULT_INTEROBJECT_FORCE_LAW(object_list, **kwargs):
#    # Check that there are exactly 2 objects in list
#    if len(object_list) != 2:
#        raise Exception("Interobject force requires exactly 2 objects")
#    else:
#        object_1 = object_list[0]
#        object_2 = object_list[1]
#        
#    # Check for specified force constant
#    if "force_constant" in kwargs.keys():
#        force_constant = kwargs["force_constant"]
#    else:
#        force_constant = DEFAULT_INTEROBJECT_FORCE_CONSTANT
#     
#    # Calculate vectors
#    vector_1_to_2 = object_2.position-object_1.position
#    inter_distance = puf.np_vect_mag(vector_1_to_2)
#    unit_vector_1_to_2 = vector_1_to_2/inter_distance
#    
#    # Calculate forces
#    force_magnitude = force_constant / (inter_distance**2)
#    force_on_object_1 = force_magnitude * unit_vector_1_to_2
#    force_on_object_2 = -1 * force_on_object_1
#    
#    return [force_on_object_1, force_on_object_2]
#
#def DEFAULT_UNIVERSAL_FORCE_LAW(object_list, **kwargs):
#    # Check that there is exactly 1 object in list
#    if len(object_list) != 1:
#        raise Exception("Universal force requires exactly 1 object")
#    else:
#        object_1 = object_list[0]
#        
#    if "force_constant" in kwargs.keys():
#        force_constant = kwargs["force_constant"]
#    else:
#        force_constant = DEFAULT_UNIVERSAL_FORCE_CONSTANT
#    
#    if "direction_vector" in kwargs.keys():
#        direction_vector = kwargs["direction_vector"]
#    else:
#        direction_vector = DEFAULT_DIRECTION_VECTOR
#    
#    force_on_object_1 = force_constant * direction_vector
#    
#    return [force_on_object_1]
#
#def DEFAULT_UNIVERSAL_ACCELERATION_FORCE_LAW(object_list, **kwargs):
#    # Check that there is exactly 1 object in list
#    if len(object_list) != 1:
#        raise Exception("Universal force requires exactly 1 object")
#    else:
#        object_1 = object_list[0]
#        
#    if "force_constant" in kwargs.keys():
#        force_constant = kwargs["force_constant"]
#    else:
#        force_constant = DEFAULT_UNIVERSAL_FORCE_CONSTANT
#    
#    if "direction_vector" in kwargs.keys():
#        direction_vector = kwargs["direction_vector"]
#    else:
#        direction_vector = DEFAULT_DIRECTION_VECTOR
#    
#    force_on_object_1 = force_constant * direction_vector * object_1.mass
#    
#    return [force_on_object_1]
#
#def DEFAULT_DRAG_FORCE_LAW(object_list, **kwargs):
#    # Check that there is exactly 1 object in list
#    if len(object_list) != 1:
#        raise Exception("Universal force requires exactly 1 object")
#    else:
#        object_1 = object_list[0]
#        
#    if "force_constant" in kwargs.keys():
#        force_constant = kwargs["force_constant"]
#    else:
#        force_constant = DEFAULT_UNIVERSAL_FORCE_CONSTANT
#    
#    direction_vector = -object_1.velocity / puf.np_vect_mag(object_1.velocity)
#    
#    force_on_object_1 = force_constant * direction_vector
#    
#    return [force_on_object_1]















# =============================================================================
# 
# =============================================================================
#class inter_object_force:
#    
#    def __init__(self, flags_list=[], force_law=copy(puf.DEFAULT_INTEROBJECT_FORCE_LAW), **force_law_args):
#        self.flags_list = flags_list
#        self.force_law=force_law
#        self.force_law_args = force_law_args
#        
#    def calculate_forces(self, object_1, object_2):
#        valid_combintation=True
#        
#        for flag in self.flags_list:
#            if flag not in object_1.flags_dict:
#                valid_combintation = False
#                break
#            if flag not in object_2.flags_dict:
#                valid_combintation = False
#                break
#            
#        if valid_combintation:
#            force_on_object_1, force_on_object_2 = self.force_law(object_1, object_2, **self.force_law_args)
#            return force_on_object_1, force_on_object_2
#        else:
#            return np.zeros_like(object_1.position), np.zeros_like(object_2.position)
#        
#        
#class universal_force:
#    
#    def __init__(self, flags_list=[], force_law = puf.DEFAULT_UNIVERSAL_FORCE_LAW, **force_law_args):
#        self.flags_list = flags_list
#        self.force_law=force_law
#        self.force_law_args = force_law_args
#        
#    def calculate_forces(self, object_1):
#        object_1_force_valid = True
#        for flag in self.flags_list:
#            if flag not in object_1.flags_dict:
#                object_1_force_valid = False
#                break
#            
#        if object_1_force_valid:
#            force_on_object_1 = self.force_law(object_1, **self.force_law_args)
#            return force_on_object_1
#        else:
#            return np.zeros_like(object_1.position)
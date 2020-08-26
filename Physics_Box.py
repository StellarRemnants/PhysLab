# -*- coding: utf-8 -*-

import PhysLab_Utility_Functions as puf

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
                        if puf.VERBOSE:
                            print(f"Computing inter_object force for {obj1} & {obj2}")
                        force_1, force_2 = force.calculate_forces(obj1, obj2)
                        if puf.VERBOSE:
                            print(f"Forces are <{force_1}> & <{force_2}>")
                            print()
                        obj1.update_velocity(force_1, dt)
                        obj2.update_velocity(force_2, dt)
                        
        for force in self.universal_forces:
            for obj in self.objects_list:
                force_1 = force.calculate_forces(obj)
                if puf.VERBOSE:
                    print(f"force_1 {force_1}")
                obj.update_velocity(force_1, dt)
    
    def step_time(self, dt):
        self.update_positions(dt)
        self.update_velocities(dt)
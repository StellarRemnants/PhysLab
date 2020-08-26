#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:38:32 2020

@author: stellarremnants
"""

import numpy as np

# =============================================================================
# UTILITY FUNCTION DEFAULTS
# =============================================================================

DEFAULT_INTEROBJECT_FORCE_CONSTANT = -1
DEFAULT_UNIVERSAL_FORCE_CONSTANT = 1
DEFAULT_DIRECTION_VECTOR = np.asarray([0,-1,0], dtype=float)
VERBOSE = 0


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
    
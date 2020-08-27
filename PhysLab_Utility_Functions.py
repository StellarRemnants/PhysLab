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

VERBOSE = 0


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def np_vect_mag(np_vect):
    return np.sqrt(np_vect.dot(np_vect))

def np_vect_norm(np_vect):
    return np_vect/np_vect_mag(np_vect)
    
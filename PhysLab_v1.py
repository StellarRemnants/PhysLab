# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

import numpy as np
import time
from copy import copy
from Base_Object import base_object as bo
from Physics_Box import physics_box as pb
import Forces as f


    
    # %%
    

#f2 = f.laminar_drag_force()
f2 = f.gravitational_force()

objects_list = []
np.random.seed(100184)
for i in range(10):
    objects_list.append(bo(
            position=np.asarray([np.random.random(), np.random.random(), np.random.random()])*2-1,
            velocity=np.asarray([np.random.random(), np.random.random(), np.random.random()])*2-1,
                           ))
    
box = pb(objects_list=objects_list, forces_list=[f2])
box.plot_box()

# %%
#start_time = time.time()
#frame_count = 0
#frame_time = .25
#while True:
#    time_now = time.time()
#    dt = time_now-start_time
#    if dt > frame_count * frame_time:
#        box.step_time(frame_time)
#        frame_count += 1
#        box.plot_box()

# %%

box.step_time(.25)
box.plot_box()

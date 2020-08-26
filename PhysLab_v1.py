# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

import numpy as np
import time
from copy import copy
import Base_Object as bo
import Forces
import Physics_Box as pb

    
#%%
object_1 = copy(bo.base_object(position=np.asarray([0,0,1], dtype=float)))
object_2 = copy(bo.base_object(position=np.asarray([0,1,0], dtype=float)))
objects_list = [object_1,object_2]  
#uforce = universal_force()
#test_box = physics_box(objects_list=objects_list, universal_forces=[uforce])
iforce = Forces.inter_object_force()
test_box = pb.physics_box(objects_list=objects_list, inter_object_forces=[iforce], universal_forces=[])
print(test_box)

for t in range(5):
    test_box.step_time(1)
    print(test_box)
    time.sleep(.1)
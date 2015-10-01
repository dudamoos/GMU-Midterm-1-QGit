from common import *
import math
import hubo_ach as ha

# Robot lifts its arms over 1 second
arm_lift_time = 1
def arm_lift(ref, phase_time):
	# IK
	gamma = (math.pi / 6) * (1 - math.cos(math.pi * phase_time))
	# Ref output
	ref.ref[ha.RSR] = -gamma
	ref.ref[ha.LSR] = gamma

# Robot lowers its arms over 1 second
def arm_lower(ref, phase_time):
	arm_lift(ref, arm_lift_time - phase_time)

# Robot eases into new support polygon over 2 seconds
lean_time = 2
def lean(ref, phase_time, distance):
	# IK
	w = (distance/2) * (1 - math.cos((math.pi / 2) * phase_time))
	theta = math.asin(w / LEG_TOTAL)
	# Ref output
	ref.ref[ha.RHR] = ref.ref[ha.LHR] = theta
	ref.ref[ha.RAR] = ref.ref[ha.LAR] = -theta

def lean_left(ref, phase_time): lean(ref, phase_time, -HIP_TO_MID)
def lean_right(ref, phase_time): lean(ref, phase_time, HIP_TO_MID)
def unlean_left(ref, phase_time): lean(ref, phase_time + lean_time, -HIP_TO_MID)
def unlean_right(ref, phase_time): lean(ref, phase_time + lean_time, HIP_TO_MID)

def pause(ref, phase_time): pass # just wait for the robot to stabilize

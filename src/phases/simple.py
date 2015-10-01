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

# Robot stands fully upright in 3 seconds
leg_reset_time = 3
def leg_reset(ref, phase_time):
	# Based on reset code
	multiplier = 1
	if (phase_time < 1): multiplier = 0.98
	else if (phase_time < 2): multiplier = 0.96
	else if (phase_time < 3): multiplier = 0.9
	else: multiplier = 0
	# Only reset leg related joints
	for joint in (ha.RHR, ha.LHR, ha.RHP, ha.LHP, ha.RKN, ha.LKN, ha.RAR, ha.LAR, ha.RAP, ha.LAP):
		ref.ref[joint] *= multiplier

# Robot cycles its leg with a period of 4 seconds per full cycle
leg_time = 2 # time for half-cycle (single lift or extend)
LEG_MID = H_TOP/2 + 50
LEG_AMP = H_TOP/2 - 50
def change_leg(ref, phase_time, hip, knee, ankle):
	# IK
	l = LEG_AMP * math.cos((math.pi / leg_time) * phase_time) + LEG_MID
	phi = math.acos(( LEG_UPPER**2 + LEG_LOWER**2 - l**2) / (2*LEG_UPPER*LEG_LOWER))
	a   = math.acos(( LEG_UPPER**2 - LEG_LOWER**2 + l**2) / (2*LEG_UPPER*l))
	b   = math.acos((-LEG_UPPER**2 + LEG_LOWER**2 + l**2) / (2*LEG_LOWER*l))
	psi = math.pi - phi
	# Ref output
	ref.ref[hip] = -a
	ref.ref[knee] = psi
	ref.ref[ankle] = -b

def lift_left(ref, phase_time):
	# Lift left leg with left hip, knee, ankle joints
	change_leg(ref, phase_time, ha.LHP, ha.LKN, ha.LAP)

def lift_right(ref, phase_time):
	# Lift right leg with right hip, knee, ankle joints
	change_leg(ref, phase_time, ha.RHP, ha.RKN, ha.RAP)

def extend_left(ref, phase_time):
	# Extend left leg by phase shifting lift cycle by 2 seconds
	change_leg(ref, phase_time + leg_time, ha.LHP, ha.LKN, ha.LAP)

def extend_right(ref, phase_time):
	# Extend right leg by phase shifting lift cycle by 2 seconds
	change_leg(ref, phase_time + leg_time, ha.RHP, ha.RKN, ha.RAP)


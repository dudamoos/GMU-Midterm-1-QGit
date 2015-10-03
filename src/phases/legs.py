from common import *
import math
import hubo_ach as ha

# Robot stands fully upright in 3 seconds
leg_reset_time = 1.0
def leg_reset(ref, phase_time, *args):
	# Reset desired joints to zero
	for joint in args: ref.ref[joint] = 0

def leg_reset_left(ref, phase_time):
	leg_reset(ref, phase_time, ha.LHP, ha.LKN, ha.LAP)
	
def leg_reset_right(ref, phase_time):
	leg_reset(ref, phase_time, ha.RHP, ha.RKN, ha.RAP)
	
def leg_reset_all(ref, phase_time):
	leg_reset(ref, phase_time, ha.LHP, ha.LKN, ha.LAP, ha.RHP, ha.RKN, ha.RAP)

# Robot cycles its leg with a period of 4 seconds per full cycle
leg_time = 2.0 # time for half-cycle (single lift or extend)
LEG_MID = H_TOP/2 + 50
LEG_AMP = H_TOP/2 - 50
def change_leg(ref, phase_time, hip, knee, ankle, ankle_roll_dir, ankle_roll):
	# IK
	l = LEG_AMP * math.cos((math.pi / leg_time) * phase_time) + LEG_MID
	phi = math.acos(( LEG_UPPER**2 + LEG_LOWER**2 - l**2) / (2*LEG_UPPER*LEG_LOWER))
	a   = math.acos(( LEG_UPPER**2 - LEG_LOWER**2 + l**2) / (2*LEG_UPPER*l))
	b   = math.acos((-LEG_UPPER**2 + LEG_LOWER**2 + l**2) / (2*LEG_LOWER*l))
	psi = math.pi - phi
	theta = (THETA_LEAN/2) * (1 + math.cos((math.pi / leg_time) * phase_time))
	# Ref output
	ref.ref[hip] = -a
	ref.ref[knee] = psi
	ref.ref[ankle] = -b
	ref.ref[ankle_roll] = ankle_roll_dir * theta

def lift_left(ref, phase_time):
	# Lift left leg with left hip, knee, ankle joints
	change_leg(ref, phase_time, ha.LHP, ha.LKN, ha.LAP, -1, ha.LAR)

def lift_right(ref, phase_time):
	# Lift right leg with right hip, knee, ankle joints
	change_leg(ref, phase_time, ha.RHP, ha.RKN, ha.RAP, 1, ha.RAR)

def extend_left(ref, phase_time):
	# Extend left leg by phase shifting lift cycle by 2 seconds
	change_leg(ref, phase_time + leg_time, ha.LHP, ha.LKN, ha.LAP, -1, ha.LAR)

def extend_right(ref, phase_time):
	# Extend right leg by phase shifting lift cycle by 2 seconds
	change_leg(ref, phase_time + leg_time, ha.RHP, ha.RKN, ha.RAP, 1, ha.RAR)


from common import *
import math
import hubo_ach as ha

# Robot moves up and down with a period of 5 seconds
hop_time = 10
HOP_MID = H_TOP - 200
HOP_AMP = 200
def hop(ref, phase_time):
	# IK
	h = HOP_AMP * math.cos((0.4 * math.pi) * phase_time) + HOP_MID
	l = math.sqrt(h**2 + HIP_TO_MID**2)
	theta = math.atan(HIP_TO_MID / h)
	phi = acos_clamped(( LEG_UPPER**2 + LEG_LOWER**2 - l**2) / (2*LEG_UPPER*LEG_LOWER))
	a   = acos_clamped(( LEG_UPPER**2 - LEG_LOWER**2 + l**2) / (2*LEG_UPPER*l))
	b   = acos_clamped((-LEG_UPPER**2 + LEG_LOWER**2 + l**2) / (2*LEG_LOWER*l))
	psi = math.pi - phi
	# Ref output
	ref.ref[ha.RHR] = ref.ref[ha.LHR] = theta
	ref.ref[ha.RAR] = -theta
	ref.ref[ha.LAR] = 0
	ref.ref[ha.RHP] = -a
	ref.ref[ha.RKN] = psi
	ref.ref[ha.RAP] = -b

# Robot stands on fully extended right leg starting from any height in 3 seconds
hop_stand_time = 2
LAR_THETA_GOAL = math.asin(HIP_TO_MID / LEG_TOTAL)
def hop_stand(ref, phase_time):
	#ref.ref[ha.LAR] = LAR_THETA_GOAL * (1 - math.cos((math.pi / 2) * phase_time))
	
	# Based on reset code
	multiplier = 1
	if (phase_time < 0.5): multiplier = 0.95
	else if (phase_time < 1.0): multiplier = 0.9
	else if (phase_time < 1.5): multiplier = 0.8
	else if (phase_time < 1.9): multiplier = 0.5
	else: multiplier = 0
	
	for joint in (ha.RHR, ha.LHR, ha.RHP, ha.LHP, ha.RKN, ha.LKN, ha.RAR, ha.LAR, ha.RAP, ha.LAP):
		ref.ref[joint] *= multiplier
	

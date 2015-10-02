from common import *
import math
import hubo_ach as ha

# Robot moves up and down with a period of 5 seconds
hop_time = 10.0
HOP_MID = H_TOP - 200
HOP_AMP = 200
def hop(ref, phase_time):
	# IK
	h = HOP_AMP * math.cos((0.4 * math.pi) * phase_time) + HOP_MID
	l = math.sqrt(h**2 + HIP_TO_MID**2)
	theta = math.atan2(HIP_TO_MID, h)
	phi = acos_clamped(( LEG_UPPER**2 + LEG_LOWER**2 - l**2) / (2*LEG_UPPER*LEG_LOWER))
	a   = acos_clamped(( LEG_UPPER**2 - LEG_LOWER**2 + l**2) / (2*LEG_UPPER*l))
	b   = acos_clamped((-LEG_UPPER**2 + LEG_LOWER**2 + l**2) / (2*LEG_LOWER*l))
	psi = math.pi - phi
	# Ref output
	ref.ref[ha.RHR] = ref.ref[ha.LHR] = theta
	ref.ref[ha.RAR] = -theta
	ref.ref[ha.RHP] = -a
	ref.ref[ha.RKN] = psi
	ref.ref[ha.RAP] = -b
	

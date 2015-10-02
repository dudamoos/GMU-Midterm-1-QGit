from common import *
import math
import hubo_ach as ha
import legs

PLANE_ANGLE = math.pi / 2

# Robot leans over 5 seconds, using its arms for balance
plane_time = 4.0
def do_plane(ref, phase_time):
	# IK
	theta = (PLANE_ANGLE / 2) * (1 - math.cos((math.pi / plane_time) * phase_time))
	x = (HIP_TO_WAIST / 2) * (1 - math.cos((math.pi / plane_time) * phase_time))
	gamma = math.asin(x / C_STAND)
	o = (math.pi / 4) * (1 - math.cos((math.pi / plane_time) * phase_time))
	#gamma = (GAMMA_STAND / 2) * (1 - math.cos((math.pi / plane_time) * phase_time))
	# Ref output
	ref.ref[ha.LHP] = -theta - gamma
	ref.ref[ha.LAP] = gamma
	ref.ref[ha.RSP] = ref.ref[ha.LSP] = o

# Robot leans forward parallel to ground over 5 seconds
def plane(ref, phase_time):
	do_plane(ref, phase_time)
	legs.extend_right(ref, (legs.leg_time / plane_time) * phase_time)

# Robot straightens so be perpendicular to ground over 5 seconds
def unplane(ref, phase_time):
	do_plane(ref, phase_time + plane_time)
	legs.lift_right(ref, (legs.leg_time / plane_time) * phase_time)

# Robot moves up and down with a period of 5 seconds
dance_time = 10.0
DANCE_MID = H_STAND - 100
DANCE_AMP = 100
def dance(ref, phase_time):
	#TODO
	# IK - f/b
	h = DANCE_AMP * math.cos((0.4 * math.pi) * phase_time) + DANCE_MID
	c = math.sqrt(h**2 + HIP_TO_MID**2)
	gamma = math.atan2(HIP_TO_MID, h)
	# IK - l/r
	l = math.sqrt(c**2 + HIP_TO_MID**2)
	theta = math.atan2(HIP_TO_MID, c)
	# IK - u/d
	phi = acos_clamped(( LEG_UPPER**2 + LEG_LOWER**2 - l**2) / (2*LEG_UPPER*LEG_LOWER))
	a   = acos_clamped(( LEG_UPPER**2 - LEG_LOWER**2 + l**2) / (2*LEG_UPPER*l))
	b   = acos_clamped((-LEG_UPPER**2 + LEG_LOWER**2 + l**2) / (2*LEG_LOWER*l))
	psi = math.pi - phi
	# Ref output
	ref.ref[ha.LHR] = -theta
	ref.ref[ha.LAR] = -theta
	ref.ref[ha.LHP] = -PLANE_ANGLE - gamma - a
	ref.ref[ha.LKN] = psi
	ref.ref[ha.LAP] = gamma - b

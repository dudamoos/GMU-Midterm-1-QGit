from common import *
import math
import hubo_ach as ha

# Robot leans over 5 seconds, using its arms for balance
plane_time = 4.0
LEG_PLANED_H = 400
LEG_AMP = LEG_PLANED_H/2 - 50
LEG_MID = LEG_PLANED_H/2 + 50
def do_plane(ref, phase_time):
	# IK - lean forward/backward
	theta = (PLANE_ANGLE / 2) * (1 - math.cos((math.pi / plane_time) * phase_time))
	x = (COM_OFFSET / 2) * (1 - math.cos((math.pi / plane_time) * phase_time))
	gamma = math.asin(x / C_STAND)
	o = (PLANE_ANGLE / 2) * (1 - math.cos((math.pi / plane_time) * phase_time))
	# Ref output - lean forward/backward
	ref.ref[ha.LHP] = -theta - gamma
	ref.ref[ha.LAP] = gamma
	ref.ref[ha.RSP] = ref.ref[ha.LSP] = -o
	
	# IK - leg extend/lift
	l = LEG_MID - LEG_AMP * math.cos((math.pi / plane_time) * phase_time)
	phi = math.acos(( LEG_UPPER**2 + LEG_LOWER**2 - l**2) / (2*LEG_UPPER*LEG_LOWER))
	a   = math.acos(( LEG_UPPER**2 - LEG_LOWER**2 + l**2) / (2*LEG_UPPER*l))
	b   = math.acos((-LEG_UPPER**2 + LEG_LOWER**2 + l**2) / (2*LEG_LOWER*l))
	psi = math.pi - phi
	# Ref output - leg extend/lift
	ref.ref[ha.RHP] = -a
	ref.ref[ha.RKN] = psi
	ref.ref[ha.RAP] = -b
	
	# IK - lean left/right - shift from hip roll to hip yaw
	w1 = (HIP_TO_MID/2) * (1 + math.cos((math.pi / 2) * phase_time))
	theta1 = math.asin(w1 / LEG_TOTAL)
	w2 = (HIP_TO_MID/2) * (1 - math.cos((math.pi / 2) * phase_time))
	theta2 = math.asin(w2 / LEG_TOTAL)
	# Ref output - lean left/right
	ref.ref[ha.RHR] = ref.ref[ha.LHR] = -theta1
	ref.ref[ha.RHY] = ref.ref[ha.LHY] = -theta2

# Robot leans forward parallel to ground over 5 seconds
def plane(ref, phase_time): do_plane(ref, phase_time)

# Robot straightens so be perpendicular to ground over 5 seconds
def unplane(ref, phase_time): do_plane(ref, phase_time + plane_time)

# Robot moves up and down with a period of 5 seconds
dance_time = 10.0
#DANCE_AMP = 100
DANCE_AMP = 50
DANCE_MID = H_STAND - DANCE_AMP
def dance(ref, phase_time):
	#TODO
	# IK - f/b
	h = DANCE_AMP * math.cos((0.4 * math.pi) * phase_time) + DANCE_MID
	c = math.sqrt(h**2 + COM_OFFSET**2)
	gamma = math.atan2(COM_OFFSET, h)
	# IK - l/r
	l = math.sqrt(c**2 + HIP_TO_MID**2)
	theta = math.atan2(HIP_TO_MID, c)
	# IK - u/d
	phi = acos_clamped(( LEG_UPPER**2 + LEG_LOWER**2 - l**2) / (2*LEG_UPPER*LEG_LOWER))
	a   = acos_clamped(( LEG_UPPER**2 - LEG_LOWER**2 + l**2) / (2*LEG_UPPER*l))
	b   = acos_clamped((-LEG_UPPER**2 + LEG_LOWER**2 + l**2) / (2*LEG_LOWER*l))
	psi = math.pi - phi
	# Ref output
	ref.ref[ha.LHY] = -theta # yaw instead of roll because of order of actuators
	ref.ref[ha.LAR] = theta # moving in opposite direction of hop
	ref.ref[ha.LHP] = -PLANE_ANGLE - gamma - a
	ref.ref[ha.LKN] = psi
	ref.ref[ha.LAP] = gamma - b

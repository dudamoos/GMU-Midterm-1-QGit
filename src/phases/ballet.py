from common import *
import math
import hubo_ach as ha

# Robot leans forward parallel to ground over XXX seconds
plane_time = -1
def plane(ref, phase_time):
	#TODO
	pass

# Robot straightens so be perpendicular to ground over XXX seconds
unplane_time = -1
def unplane(ref, phase_time):
	#TODO
	pass

# Robot moves up and down with a period of 5 seconds
dance_time = 10
DANCE_MID = H_TOP - 100
DANCE_AMP = 100
def dance(ref, phase_time):
	#TODO
	pass

# Robot stands on fully extended left leg starting from any height in 3 seconds
dance_stand_time = 3
def dance_stand(ref, phase_time):
	# Based on reset code
	# Also need to roll right ankle (ha.RAR) so it's parallel to the ground again
	# TODO
	pass

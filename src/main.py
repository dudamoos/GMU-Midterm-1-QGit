#!/usr/bin/python

import hubo_ach as ha
import ach
from time import sleep
import math

from phases.common import *
import phases.simple as ps
import phases.hop as ph
import phases.ballet as pb

def debug_joint(name, index, ref, state):
	if (abs(ref.ref[index] - state.joint[index].pos) > 0.15):
		print "{0} is slipping! -> ref {1:3.4f}\tstate {2:3.4f}".format(name, ref.ref[index], state.joint[index].pos)

REF_INTERVAL = 0.05 # control loop runs at 20 Hz

PHASE_LIST = [
	(ps.arm_lift, ps.arm_lift_time, "lifting arms ..."),
	
	(ps.lean_right, ps.lean_time, "leaning right ..."),
	(ps.lift_left, ps.leg_time, "lifting left leg ..."),
	
	(ph.hop, ph.hop_time, "hopping ..."),
	(ps.leg_reset_right, ps.leg_reset_time, "standing ..."),
	(ps.extend_left, ps.leg_time, "extending left leg ..."),
	(ps.unlean_right, ps.lean_time, "centering ..."),
	
	(ps.lean_left, ps.lean_time, "leaning left ..."),
	(ps.lift_right, ps.leg_time, "lifting right leg ..."),
	#(pb.plane, pb.plane_time, "leaning forward ..."),
	(ps.extend_right, ps.leg_time, "extending right leg ..."),
	
	#(pb.dance, pb.dance_time, "dancing ..."),
	(ps.leg_reset_left, ps.leg_reset_time, "standing ..."),
	(ps.lift_right, ps.leg_time, "retracting right leg ..."),
	#(pb.unplane, pb.unplane_time, "straightening ..."),
	(ps.extend_right, ps.leg_time, "extending right leg ..."),
	(ps.unlean_right, ps.lean_time, "centering ..."),
	
	(ps.arm_lower, ps.arm_lift_time, "lowering arms ...")
]

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
chan_state = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
chan_ref = ach.Channel(ha.HUBO_CHAN_REF_NAME)

# Variables to hold state and reference
state = ha.HUBO_STATE()
ref = ha.HUBO_REF()

print "Python Code!"

for (phase_func, phase_length, phase_text) in PHASE_LIST:
	print phase_text
	
	[status, framesize] = chan_state.get(state, wait=False, last=True)
	time_init = state.time
	time_last = time_init + phase_length
	while True:
		# Adaptive delay (timing)
		[status, framesize] = chan_state.get(state, wait=False, last=True)
		time_cur = state.time
		# Debug
		print "\rSim time ...",time_cur,
		#debug_joint("RHP", ha.RHP, ref, state)
		#debug_joint("RKP", ha.RKN, ref, state)
		#debug_joint("RAP", ha.RAP, ref, state)
		# Phase time (emulate do-while)
		if (time_cur >= time_last): break
		# Step calculations
		phase_func(ref, time_cur - time_init)
		chan_ref.put(ref)
		# Adaptive delay (sleep)
		[status, framesize] = chan_state.get(state, wait=False, last=True)
		sleep(time_cur + REF_INTERVAL - state.time)
	# Ensure phase reaches its final point
	phase_func(ref, phase_length)
	chan_ref.put(ref)
	
	print
	sleep(0.5) # aribitrary inter-phase delay


#!/usr/bin/python -u

import hubo_ach as ha
import ach
from time import sleep
import math

from phases.common import *
import phases.simple as ps
import phases.legs as pl
import phases.hop as ph
import phases.ballet as pb

def debug_joint(name, index, ref, state):
	#if (abs(ref.ref[index] - state.joint[index].pos) > 0.15):
	print "{0} -> ref {1:3.4f}\tstate {2:3.4f}".format(name, ref.ref[index], state.joint[index].pos)
	

def sim_time_sleep(target, state, chan_state):
	while (state.time < target):
		[status, framesize] = chan_state.get(state, wait=True, last=True)

REF_INTERVAL = 0.05 # control loop runs at 20 Hz

PHASE_LIST = [
	(ps.arm_lift, ps.arm_lift_time, "lifting arms ..."),
	
	(ps.lean_right     , ps.lean_time,     "leaning right ..."),
	(pl.lift_left      , pl.leg_time      , "lifting left leg ..."),
	(ph.hop            , ph.hop_time      , "hopping ..."),
	(pl.extend_left    , pl.leg_time      , "extending left leg ..."),
	(pl.leg_reset_left , pl.leg_reset_time, "forcing both legs on ground ..."),
	(ps.unlean_right   , ps.lean_time     , "centering ..."),
	
	#(ps.pause, 3, "stabilizing ..."),
	
	(ps.lean_left      , ps.lean_time     , "leaning left ..."),
	(pl.lift_right     , pl.leg_time      , "lifting right leg ..."),
	(pb.plane          , pb.plane_time    , "leaning forward ..."),
	#(ps.pause, 2, "please inspect ..."),
	(pb.dance          , pb.dance_time    , "dancing ..."),
	(pb.unplane        , pb.plane_time    , "straightening ..."),
	(pl.extend_right   , pl.leg_time      , "extending right leg ..."),
	(ps.unlean_left    , ps.lean_time     , "centering ..."),
	
	(ps.arm_relax, ps.arm_lift_time, "relaxing arms ...")
]

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
chan_state = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
chan_ref = ach.Channel(ha.HUBO_CHAN_REF_NAME)

# Variables to hold state and reference
state = ha.HUBO_STATE()
ref = ha.HUBO_REF()

print "Python Code!"

for (phase_func, phase_length, phase_text) in PHASE_LIST:
	if (phase_func == ps.pause): print '\a',
	print phase_text,
	
	[status, framesize] = chan_state.get(state, wait=False, last=True)
	time_init = state.time
	time_last = time_init + phase_length
	while True:
		# Adaptive delay (timing)
		[status, framesize] = chan_state.get(state, wait=False, last=True)
		time_cur = state.time
		# Debug
		print "\r", phase_text, time_cur - time_init, "                              ",
		#if (phase_func == pb.dance):
		#	print
		#	debug_joint("LHP", ha.LHP, ref, state)
		#	debug_joint("LHR", ha.LHR, ref, state)
		#	debug_joint("LHY", ha.LHY, ref, state)
		#	debug_joint("LKP", ha.LKN, ref, state)
		#	debug_joint("LAP", ha.LAP, ref, state)
		#	debug_joint("LAR", ha.LAR, ref, state)
		# Phase time (emulate do-while)
		if (time_cur >= time_last): break
		# Step calculations
		phase_func(ref, time_cur - time_init)
		chan_ref.put(ref)
		# Adaptive delay (sleep)
		[status, framesize] = chan_state.get(state, wait=False, last=True)
		sim_time_sleep(time_cur + REF_INTERVAL, state, chan_state)
	# Ensure phase reaches its final point
	phase_func(ref, phase_length)
	chan_ref.put(ref)
	
	print
	# arbitrary inter-phase delay
	sim_time_sleep(time_cur + 4*REF_INTERVAL, state, chan_state)


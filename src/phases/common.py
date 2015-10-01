import math

def acos_clamped(ratio):
	return math.acos(max(min(ratio, 1.0), -1.0))

# Constants
LEG_UPPER = 300.3
LEG_LOWER = 300.38
LEG_TOTAL = LEG_UPPER + LEG_LOWER
HIP_TO_MID = 88.43

H_TOP = math.sqrt(LEG_TOTAL**2 - HIP_TO_MID**2)


import math

def acos_clamped(ratio):
	return math.acos(max(min(ratio, 1.0), -1.0))

# Constants
LEG_UPPER = 300.3
LEG_LOWER = 300.38
LEG_TOTAL = LEG_UPPER + LEG_LOWER
HIP_TO_MID = 88.43
HIP_TO_GUT = 289.47
WAIST_TO_GUT = 107.0
HIP_TO_WAIST = HIP_TO_GUT - WAIST_TO_GUT

H_TOP = math.sqrt(LEG_TOTAL**2 - HIP_TO_MID**2)
THETA_LEAN = math.asin(HIP_TO_MID / LEG_TOTAL)

C_STAND = H_TOP # for different notation
H_STAND = math.sqrt(C_STAND**2 - HIP_TO_WAIST**2)
GAMMA_STAND = math.asin(HIP_TO_WAIST / C_STAND)

#GAMMA_STAND = math.pi / 12 # stable standing LAP found empirically
#X_STAND = C_TOP * math.sin(GAMMA_STAND) # COM offset found empirically


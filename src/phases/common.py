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
COM_OFFSET_REAL = HIP_TO_WAIST / 2

H_TOP = math.sqrt(LEG_TOTAL**2 - HIP_TO_MID**2)
THETA_LEAN = math.asin(HIP_TO_MID / LEG_TOTAL)
LEG_LIFTED_H = 100

#COM_OFFSET = COM_OFFSET_REAL
#PLANE_ANGLE = math.pi / 2
PLANE_ANGLE = 4 * math.pi / 12.0
COM_OFFSET = COM_OFFSET_REAL * math.cos(math.pi / 2 - PLANE_ANGLE)
LEG_PLANED_H = 200

C_STAND = H_TOP # for different notation
H_STAND = math.sqrt(C_STAND**2 - COM_OFFSET**2)
GAMMA_STAND = math.asin(COM_OFFSET / C_STAND)
RHO_STAND = math.acos(COM_OFFSET / C_STAND)


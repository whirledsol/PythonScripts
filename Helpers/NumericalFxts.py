
def toDegree(radians):
    return radians*(180.0/math.pi)

def toRad(degree):
    return degree*(math.pi/180.0)

# determines if item s, is a number or not    
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
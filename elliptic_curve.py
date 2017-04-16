from gmpy2 import divm, powmod
from gmpy2 import gcd

#some ideas from here: https://jeremykun.com/2014/02/24/elliptic-curves-as-python-objects/
class Point(object):
	def __init__(self, curve, x, y, mod):
		self.x = x
		self.y = y
		self.curve = curve
		self.mod = mod		

		if not curve.testPoint(x, y, mod):
			raise Exception("Point %s not on given curve %s" % (self, curve))

	def __str__(self):
		return "(%G,%G)" % (self.x, self.y)
	
	def __neg__(self):
		return Point(self.curve, self.x, -self.y)
	
	def __add__(self, Q):
		if isinstance(Q, Ideal):
			return self
		
		x1, y1, x2, y2 = self.x, self.y, Q.x, Q.y
		lambda1 = 0	

		if (x1, y1) == (x2, y2):
			if y1 == 0:
				return Ideal(self.curve)
			
			lambda1 = divm((3 * powmod(x1,2,self.mod) + self.curve.a), (2*y1), self.mod)
			
		else:
			try:
				lambda1 = divm((y2-y1), (x2-x1), self.mod)
			except ZeroDivisionError:
#				print "x1-x2"
#				print x2-x1
				return x2-x1
				
		x3 = (powmod(lambda1,2,self.mod) - x1 - x2) % self.mod
		y3 = (lambda1*(x1 - x3) - y1) % self.mod

		return Point(self.curve, x3, y3, self.mod)

	def __sub__(self, Q):
		return self + -Q
	
	def __mul__(self, n):
		if not isinstance(n, int):
			raise Exception("Must multiply by an int")
	
		if n < 0:
			return -self * -n
		if n == 0:
			return Ideal(self.curve)
		
		Q = self
		R = self if n & 1 == 1 else Ideal(self.curve)
		
		i = 2
		while i <= n:
			Q = Q + Q
			
			if n & i == i:
				R = Q + R
			
			i = i << 1

		return R

	def __rmul__(self, n):
		return self * n

class Ideal(Point):
	def __init__(self, curve):
		self.curve = curve
	
	def __str__(self):
		return "Ideal"
	
	def __neg__(self):
		return self

	def __add__(self, Q):
		return Q
	def __mul__(self, n):
		if not isinstance(n, int):
			raise Exception("Can't scale by non int")

		return self

class EllipticCurve(object):
	def __init__(self, a, b):
		self.a = a
		self.b = b
	
		self.discrimant = -16 * (4*pow(a,3) + 27*pow(b,2))
		if self.discrimant == 0:
			raise Exception("Non smooth curve.")

	def testPoint(self, x, y, m):
		return ((powmod(y,2,m) % m) == (powmod(x,3,m) + self.a*x + self.b) % m)
	
	def __str__(self):
		return "y^2 = x^3 + %Gx + %G" % (self.a, self.b)

	def __eq__(self, other):
		return (self.a, self.b) == (other.a, other.b)

	

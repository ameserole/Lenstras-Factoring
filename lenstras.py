from elliptic_curve import EllipticCurve as EC
from elliptic_curve import Point as P
from gmpy2 import gcd
from random import randrange
import sys, os
import threading

def factor_thread(mod,r):
	for j in range(r):
		A = randrange(mod)
		a = randrange(mod)
		b = randrange(mod)
		B = (b**2 - a**3 - A*a) % mod
	
		c = EC(A, B)
		p = P(c, a, b, mod)
		
		break_flag = False
	
		fact = 1
	
		for i in range(2,50):
			try:
				fact *= i
				h = fact*p
			except:
				break
			if not isinstance(h, P):	
				g = gcd(h, mod)
				print g
				print (mod / g)
				break_flag = True
				os._exit(0)
		if break_flag:
			break

def main():
	mod = int(sys.argv[1])
	threads = []
        r = mod / 5**len(str(mod))
	for i in range(500):
		t = threading.Thread(target=factor_thread, args=(mod,r,))
		threads.append(t)
#		t.setDaemon(True)
		t.start()

if __name__ == '__main__':
	main()

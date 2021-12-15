def gcd(a, b):
	if a == 0:
		return b
		
	while(b != 0):
		b, a = a%b, b

	return a

if __name__ == "__main__":
	print(gcd(66528, 52920))

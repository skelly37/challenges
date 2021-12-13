import itertools 

KEY = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")

for i in range(256):
	result = ""
	for b in KEY:
		result += (chr(b^i))

	if "crypto{" in result:
		print(result)

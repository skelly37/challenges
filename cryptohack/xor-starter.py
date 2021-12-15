text = "label"
output = ""

for c in text:
	output += chr(ord(c)^13)

print(output)

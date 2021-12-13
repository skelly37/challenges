text = "label"
result = []

for c in text:
	result.append(ord(c)^13)

output = ""
for c in result:
	output += chr(c)

print(output)

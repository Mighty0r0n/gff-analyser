with open('GCF_001050915.2.fa', 'r') as file:
	a = 0
	b= False
	for line in file.readlines():
		if line.startswith('>'):
			b = True
		elif b == True and not line.startswith('>'):
			a += len(line.strip("\n"))
		
	print(a)

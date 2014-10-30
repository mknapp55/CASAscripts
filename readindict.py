# Read back in contents of file with stored variables:

fl=open('flaggingAug620142.txt', 'r')
lns = fl.readlines()
fl.close()

starts=[]
ends=[]
c1 = 0
c2 = 0
for idx, line in enumerate(lns):
	# Find start and end points
	if line.find('=[') != -1:
		starts.append(idx)
		c1+=1
	elif line.find(']\n') != -1:
		ends.append(idx)
		c2+=1
variables = {}		
for x in range(0,len(starts)):
	variables[x]= ''.join(lns[starts[x]:ends[x]+1])
	print x
	exec variables[x]



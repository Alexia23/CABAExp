import sys

victim = ""
attacker = ""
normal = 0
polluted = 0

def setHijack(a, v):
	global victim, attacker
	victim = v
	attacker = a

def analyzeResult(file):
	global victim, attacker, normal, polluted
	f = open(file)
	line = f.readline()
	while line:
		if line.find("RIB") >= 0:
			start = line.find("{")
			end = line.find("}")
			key = line[start:end+1]
			start = key.find("[")
			end = key.find("]")
			key = key[start+1:end]
			AS = key.split(", ")
			if AS[-1] == victim:
				normal += 1
			if AS[-1] == attacker:
				polluted += 1
		line = f.readline()
	f.close()

setHijack(sys.argv[2], sys.argv[3])
analyzeResult(sys.argv[1])

print "Normal AS:" + str(normal)
print "Polluted AS:" + str(polluted)
print "Polluted rate:" + str(polluted * 1.0 / (normal + polluted))
import time
import os
dir = os.getcwd()
f = 60 # this tell how manny operation per second 
f = float(1/f)
def CPU(ins,insL):
	"""This will simulate a pcu
	"""
	z=0
#	input("type anything to start\n")
	#utilities stuff
	start = float(time.time())
	wor = False
	jmp = False
	rng = False
	n2 = 0
	
	#main parts of the CPU 
	ram = [0]*256
	B = 0
	AB = None
	Or = None #overide reg
	Pc = 0#program counter
	Sp = 0#stack pointer
	Rng = 0#progresion counter/range

	#main loop
	while True:
		n1 = time.time()
		if rng is False:
			Rng -=1
		opc, val = ins[Pc]
		print(f"AB={AB}, B={B}, Rng={Rng},stack{Sp}={ram[Sp]},{Pc}:{opc},{val}")

		if Rng < 0:
			Rng = 0
		
		if Or is not None and wor is False:
			val = Or
			Or = None

		if opc == "halt":
			message ="stop cus halt"
			break
		elif opc == "wriB":
			B = val
		elif opc == "sub":
			AB = B - val
		elif opc == "biz" and AB == 0:
			Pc=val
			jmp= True
		elif opc == "jump":
			Pc=val-1
			jmp=True
		elif opc == "ABtB":
			B = AB
		elif opc == "wtc":
			Rng = val
			rng = True
		elif opc == "prcb" and rng is True:
			Rng-=1
			if Rng == -1:
				message = "stop cus range out"
				break
		elif opc == "wriS":
			ram[Sp] = val
		elif opc == "wSono":
			Or = ram[Sp]
		elif opc == "wABono":
			Or = AB
		elif opc == "worbf":
			Or = ram[Sp]
			wor = True
		elif opc == "povbf":
			if Or is None:
				ram[Sp] = 0
			else:
				ram[Sp] = Or
			wor = False
		elif opc=="pABtB":
			B = AB
		elif opc =="pABtS":
			ram[Sp] = AB
		elif opc == "add":
			AB = val + B
		elif opc == "push":
			if Sp == 255:
				Sp = 0
			else:
				Sp+=1
		elif opc == "pull":
			if Sp == 0:
				Sp = 255
			else:
				Sp-=1
		elif opc == "print":
			if val == 0:
				print("................................."+str(B))
			elif val == 1:
				print("................................."+str(AB))
			print("................................."+str(ram[Sp]))

		else:
			message = f"Error:Opcode name'{opc}' dont exist"
			return message, z
		if jmp is True:
			jmp = False
		elif jmp is False:
			Pc = Pc +1

	
		#everything heen to done after all thing settled 
		if insL == Pc:
			message = 'OpenProgramError: Assembly must ended by "halt"'
			break
		
		z+=1
		
		#this will make sure that the fastest operation per sec is f
		while True:
			i=n2-n1
			n2=time.time()
			if i >= f:
				break
	return message, z, start
#this is to chage the format of the ins file
def ins_fetch():
	insL = 0
	ins = []
	with open(f"{dir}/fib.as","r") as program:
		for line in program:
			name, op_code, val = line.strip().split()
			if int(name)-1 == insL:
				name=int(name)-1
				ins.append(name)
				ins[name] = op_code, int(val)
				insL += 1
			else:
				print("EOL Error while scanning .as")
	print("program has a leght of {}".format(insL))
	print(ins)
	message, z, start=CPU(ins, insL)
	return message, z, start

if __name__ == '__main__':
	message, z, start=ins_fetch()
	print(message)

print("total execution",z)
end = time.time()
print("total length",end - start)
input("type anything to exit \n")

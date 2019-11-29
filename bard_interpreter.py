#Import additional Python Objects.
import os, fnmatch
import sys
import datetime

#Import the Elements of the Bard Interpreter.
import bard_env as env
import bard_ide
import bard_run
import bard_ops as ops

def interpreter():
	print("BARD Programming Language. (Basic And Reduced Definition).\nVersion : " + env.version + " on " + sys.platform + "\n\nType Help or ? for Assistance or Quit/Exit/Q or E to exit.")
	print()
	
	intvalue=""
	filename=""
	
	while intvalue not in ["q","Q","Quit","quit","Exit","exit"]:
		intvalue=input("-->")

		if intvalue.upper()[0:4]=="LIST":
			print("Num. : Code")
			
			for x in range(len(env.prog)):
				print("{: 4}".format(x+1) + " : " +env.prog[x].rstrip())
		elif intvalue.upper()[0:3]=="RUN":
			if len(intvalue)>3:
				env.currentline=int(intvalue[4:len(intvalue)].strip())-1
			else:	
				env.currentline=0
				
			bard_run.run()
		elif intvalue.upper()[0:4]=="HELP" or intvalue[0]=="?":
			print("Interpreter Keywords: (" + str(len(env.inter_kywd)) + ")")
			print("-------------------------------------")
			
			env.inter_kywd.sort()
			
			for x in range(len(env.inter_kywd)):
				print("{:14}".format(">> " + env.inter_kywd[x])," : use ? " + env.inter_kywd[x])
				
			print("\n")
			print("Language Keywords: (" + str(len(env.token_kywd)) + ")")
			print("-------------------------------------")
			
			env.token_kywd.sort()
			
			for x in range(len(env.token_kywd)):
				print("{:14}".format(">> " + env.token_kywd[x])," : use ? " + env.token_kywd[x])
			
			print("\n")
		elif intvalue.upper()[0:3]=="DEL":
			if len(intvalue)>3:
				env.prog.pop(int(intvalue[4:len(intvalue)].strip())-1)
			else:
				ops.reset()
		elif intvalue.upper()[0:3]=="DIR":
			vfile=intvalue[5:].strip()
			vfiles=fnmatch.filter(os.listdir("."),vfile + "*.2b")
			
			for x in range(len(vfiles)):
				print(">> " + vfiles[x])
		elif intvalue.upper()[0:4]=="LOAD":
			filename=intvalue[5:]

			if len(filename)>0:
				ops.loadfile(filename)
		elif intvalue.upper()[0:4]=="SAVE":
			ops.savefile(intvalue[5:])
		elif intvalue.upper()[0:3]=="IDE":
			print("Opening IDE.....")
			
			bard_ide.open_ide()
		else:
			env.prog.append(intvalue + "\n")
			env.currentline=len(env.prog)-1
		
			bard_run.run()

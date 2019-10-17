import os
import bard_env as env
import datetime
import pprint

class bard_eval:
	def __init__(self):
		self.loopbegin=False
		self.loopincrem=0
		
	def eval_code(self,evalstr):
		#print("Test: ",evalstr)
		if evalstr is None:
			return None
		elif evalstr=="":
			return None
		elif evalstr[0]=="NUMBER":
			return ("Number",float(evalstr[1]))
		elif evalstr[0]=="STRING":
			return ("String",evalstr[1])
		elif evalstr[0]=="IDENTIFIER":
			try:
				if (evalstr[1])[0:1]=="$":
					return env.env_global[evalstr[1]]
				elif (evalstr[1])[0:1]=="_":
					return self.eval_code((env.env_objects[evalstr[1]])[4][0])
				else:
					return env.env_local[evalstr[1]]
			except:
				return ("String","")
		elif evalstr[1]=="Operation":
			argLeft=self.eval_code(evalstr[3])
			argRight=self.eval_code(evalstr[4])
			
			return self.eval_operation(evalstr[2],argLeft,argRight)
		elif evalstr[1]=="Assignment":
			if evalstr[2][0]=="FUNCTION":
				return self.eval_assignment(evalstr[2][1],evalstr[3],evalstr[4])
			else:
				return self.eval_assignment(evalstr[2][1],evalstr[3],None)
		elif evalstr[1]=="Call":
			#print(evalstr[3])
			#if evalstr[4] is not None:
			#	funcbody=env.env_objects[evalstr[2][1]]["body"]
				
			#if evalstr[3] is not None:
			#	funcparams=env.env_objects[evalstr[2][1]]["params"]

			callval=self.eval_code(evalstr[3][0])
			
			if evalstr[2][1]=="OPUT":
				print(callval[1])
			elif evalstr[2][1]=="STR":
				return (callval[0],str(callval[1]).strip())
			elif evalstr[2][1]=="TYPE":
				return (callval[1],callval[0])
			elif evalstr[2][1]=="DATE":
				return ("DateTime",datetime.datetime.now())
			elif evalstr[2][1]=="RTN":
				return self.eval_code(callval)
			elif evalstr[2][1]=="LOOP":
				if self.loopbegin==False:
					if len(evalstr[3])>1:
						loopid=evalstr[3][0]
						loopstart=self.eval_code(evalstr[3][1])
						loopend=self.eval_code(evalstr[3][2])
						
						if len(evalstr[3])==4:
							loopincrement=int((evalstr[3][3])[1])
						else:
							loopincrement=1
						
						if loopstart>loopend:
							loopincrement=abs(loopincrement)
						else:
							loopincrement=abs(loopincrement)
					else:
						loopid=(evalstr[3][0])[3][1]
						loopstart=("Number",0)
						loopincrement=0

					self.eval_assignment(loopid[1],loopstart,None)
					self.loopbegin=True

				if len(evalstr[3])>1:
					looplogic=self.eval_operation(("Operator","<="),self.eval_code(loopid),loopend)[1]
				else:
					looplogic=self.eval_code(evalstr[3][0])[1]
				
				if looplogic==True:
					self.eval_codebody(evalstr[4])
					
					env.env_local[loopid[1]][1]+=loopincrement
				else:
					self.loopbegin=False
					
			#elif evalstr[2][1]=="IPUT":
				#n=(self.eval_code(callval))[1]
				#print(n)
				#print(input("Name: "))
				#print(a)
				#return self.eval_code(("String",a))
				#pass
			elif evalstr[2][1][0:1]=="_":
				funcbody=env.env_objects[evalstr[2][1]]["body"]
				funcparams=env.env_objects[evalstr[2][1]]["params"]

				for p in range(0,len(funcparams)):
					if p<len(evalstr[3]):
						self.eval_assignment(funcparams[p][1],evalstr[3][p],"")
					else:
						self.eval_assignment(funcparams[p][1],("String",""),"")
						
				self.eval_codebody(funcbody)
						
				#for line in range(0,len(funcbody)):
				#	a=self.eval_code(funcbody[line])
				#	if a is not None: return a
			else:
				return None
		else:
			return evalstr


	def eval_operation(self,op,arg1,arg2):
		result=""
		print("OP: ",arg1,arg2)
		if arg1[0]!=arg2[0]:
			argleft=str(arg1[1])
			argright=str(arg2[1])
		else:
			argleft=arg1[1]
			argright=arg2[1]

		if op[1]=="+":		#Addition
			result=argleft + argright
		elif op[1]=="-":	#Subtraction
			result=argleft - argright
		elif op[1]=="*":	#Multiplication
			result=argleft * argright
		elif op[1]=="/":	#Division
			result=argleft / argright
		elif op[1]=="%":	#Percentage
			result=argleft/argright*100
		elif op[1]=="|":	#Modulus
			result=argleft-(int(argleft/argright)*argright)	
		elif op[1]=="<":	#Less Than
			result=argleft < argright
		elif op[1]=="<=":	#Less Than or Equal To
			result=argleft <= argright
		elif op[1]==">":	#Greater Than
			result=argleft > argright
		elif op[1]==">=":	#Greater Than or Equal
			result=argleft >= argright
		elif op[1]=="==":	#Equals To
			result=argleft == argright
		elif op[1]=="!=":	#Not Equal To
			result=argleft != argright

		if type(result)==float:
			return ("Number",result)
		elif type(result)==bool:
			return ("Boolean",result)
		else:
			return ("String",result)

	def eval_call(self):
		pass

	def eval_assignment(self,obj,args1,args2):
		if args1!=None:
			if obj[0:1]=="_":
				env.env_objects[obj]={"body" : args2,"params" : args1}
				env.env_global[obj]={"type" : "function"}
			elif obj[0:1]=="$":
				env.env_global[obj]=self.eval_code(args1)
			else:
				env.env_local[obj]=self.eval_code(args1)

	def eval_codebody(self,codebody):
		for line in range(0,len(codebody)):
			rtnstate=self.eval_code(codebody[line])
		
			if rtnstate is not None: 
				return rtnstate

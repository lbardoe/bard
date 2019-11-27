import os
import bard_env as env
import datetime
import time
import pprint
import re

class bard_eval:
	def __init__(self):
		self.loopbegin=False
		self.loopincrem=0
		
	def eval_code(self,evalstr):
		#if env.env_debug==True: print("AST: ",evalstr)
		
		if evalstr is None:
			return None
		elif evalstr=="":
			return None
		elif evalstr[0]=="NUMBER":
			return ("NUMBER",float(evalstr[1]))
		elif evalstr[0]=="STRING":
			return ("STRING",evalstr[1])
		elif evalstr[0]=="IDENTIFIER":
			try:
				if (evalstr[1])[0:1]=="_":
					return self.eval_code((env.env_objects[evalstr[1]])[4][0])
				else:
					return env.env_local[evalstr[1]]
			except:
				return ("STRING","")
		elif evalstr[1]=="Operation":
			argLeft=self.eval_code(evalstr[3])
			argRight=self.eval_code(evalstr[4])
			
			return self.eval_operation(evalstr[2],argLeft,argRight)
		elif evalstr[1]=="Assignment":
			return self.eval_assignment(evalstr[2][1],self.eval_code(evalstr[3]),evalstr[4])
		elif evalstr[1]=="Call":
			#print(evalstr[3])
			callval=self.eval_code(evalstr[3][0])

			if evalstr[2][1]=="PUT":
				print(callval[1])
			elif evalstr[2][1]=="WAIT":
				time.sleep(callval[1])
			elif evalstr[2][1]=="ASCII":
				if callval[0]=="STRING":
					return ("NUMBER",ord(callval[1]))
				else:
					return ("STRING",chr(int(callval[1])))
			elif evalstr[2][1]=="STR":
				return (callval[0],str(callval[1]).strip())
			elif evalstr[2][1]=="TYPE":
				return (callval[1],callval[0])
			elif evalstr[2][1]=="DATE":
				if evalstr[3]==[None] or evalstr[3]==None:
					return ("DateTime",datetime.datetime.now())
				else:
					dt=[0,0,0,0,0,0]
					
					for x in range(6):
						dt[x]=int((evalstr[3][x])[1])
						
					return ("DateTime",datetime.datetime(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5]))
			elif evalstr[2][1]=="RTN":
				return self.eval_code(callval)
			elif evalstr[2][1] in ["IF","ELSE"]:
				if (self.eval_code(evalstr[3][0]))[1]:
					self.eval_codebody(evalstr[4])
				else:
					self.eval_codebody(evalstr[5])
			elif evalstr[2][1]=="LOOP":
				#print("Test")
				#pprint.pprint(evalstr)
				if len(evalstr[3])==4:
					loopincrement=int((evalstr[3][3])[1])
				else:
					loopincrement=1

				if len(evalstr[3])>1:
					loopid=evalstr[3][0]
					loopstart=self.eval_code(evalstr[3][1])
					loopend=self.eval_code(evalstr[3][2])
				else:
					loopid=(evalstr[3][0])[3] #[1]
					loopstart=("NUMBER",1.0)
					loopend=("NUMBER",2.0)
					loopincrement=0
					
				if loopstart>loopend:
					optype=">="
					loopincrement=abs(loopincrement)*-1
				else:
					optype="<="
					loopincrement=abs(loopincrement)
				
				self.eval_assignment(loopid[1],loopstart,None)
				
				looplogic=True
				
				while looplogic==True:
					self.eval_codebody(evalstr[4])

					loopvalue=(env.env_local[loopid[1]][1])+loopincrement

					env.env_local[loopid[1]] = ("NUMBER",loopvalue)
					
					if len(evalstr[3])>1:
						looplogic=self.eval_operation(("Operator",optype),self.eval_code(loopid),loopend)[1]
					else:
						looplogic=self.eval_code(evalstr[3][0])[1]

				env.env_local[loopid[1]] = ("NUMBER",loopvalue-1)
			elif evalstr[2][1]=="GET":
				try:
					caption=(self.eval_code(callval))[1]
				except:
					caption=""
					
				#a=raw_input(n)
				
				return self.eval_code(("STRING",input(caption)))
			elif evalstr[2][1][0:1]=="_":
				funcbody=env.env_objects[evalstr[2][1]]["body"]
				funcparams=env.env_objects[evalstr[2][1]]["params"]

				for p in range(0,len(funcparams)):
					if p<len(evalstr[3]):
						self.eval_assignment(funcparams[p][1],evalstr[3][p],"")
					else:
						self.eval_assignment(funcparams[p][1],("STRING",""),"")
						
				return self.eval_codebody(funcbody)
			else:
				objtype,objval=self.eval_code(evalstr[2])

				if evalstr[3]==[None] or evalstr[3]==None:
					return ("NUMBER",len(str(objval)))
				else:
					if len(evalstr[3])>0: val1=self.eval_code(evalstr[3][0])[1]
					if len(evalstr[3])>1: val2=self.eval_code(evalstr[3][1])[1]
											
					if objtype=="DateTime":
						val1=val1.replace("d","%d")		#Day 			1-31
						val1=val1.replace("D","%a")		#Weekday 		Mon-Sun
						val1=val1.replace("w","%w")		#Weekday 		0-6 (Sun-Sat)
						val1=val1.replace("j","%j")		#Day of Year	365
						val1=val1.replace("W","%W")		#Week 			1-52
						val1=val1.replace("m","%m")		#Month			1-12
						val1=val1.replace("M","%b")		#Month			Jan-Dec
						val1=val1.replace("y","%y")		#Year			19
						val1=val1.replace("Y","%Y")		#Year			2019
						val1=val1.replace("p","%p")		#12 Hour AM/PM	AM
						val1=val1.replace("H","%I")		#Hour			1-12 (12 Hour)
						val1=val1.replace("h","%H")		#Hour			1-24 (24 Hour)
						val1=val1.replace("n","%M")		#Minute			0-59
						val1=val1.replace("s","%S")		#Second			0-59
						
						return ("STRING",objval.strftime(val1))
					elif objtype=="STRING":
						if (evalstr[3][0])[0]=="NUMBER":	
							if len(evalstr[3])==1:
								val1=int(val1)

							if len(evalstr[3])>1:
								val1=val2-1
								val2=int(self.eval_code(evalstr[3][1])[1])
							
							if val1<0:
								return ("STRING",(objval)[val1:])
							else:
								return ("STRING",(objval)[val1:val1+val2])
						else:
							if len(evalstr[3])==1:
								regex=re.search(val1,objval)
								
								if regex.group()==val1:
									return ("NUMBER",regex.start()+1)
								else:
									return("STRING",regex.group())
							else:
								return ("STRING",objval.replace(val1,val2))
					elif objtype=="NUMBER":
						lind=""
						lpad=""
						comma=""
						dot=""
						rpad=""
						rind=""
						
						if val1.find(",")>-1: comma=","
						if val1.find(".")>-1: 
							lpad="0" + str(len(val1[0:val1.find(".")]))
							rpad=str(len(val1[val1.find(".")+1:len(val1)])) + "f"
							dot="."
						else:
							lpad="0"
							objval=int(objval)
				
						if val1=="b": 
							lpad="b" 
							rpad=""
							objval=int(objval)
							
						if val1=="h": 
							lpad="x"
							rpad=""
							objval=int(objval)
						
						if "%" in val1: 
							rind="%"	
							
						strformat="{:" + lpad + comma + dot + rpad + "}"

						return ("STRING",lind+strformat.format(objval)+rind)	
					else:
						pass
					
				return objval
		else:
			return evalstr

	def eval_operation(self,op,arg1,arg2):
		result=""
		#print("OP: ",op,arg1,arg2)
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
			return ("NUMBER",result)
		elif type(result)==bool:
			return ("BOOLEAN",result)
		else:
			return ("STRING",result)

	def eval_call(self):
		pass

	def eval_assignment(self,obj,args1,args2):
		#print(obj,args1)
		if args1!=None:
			if obj[0:1]=="_":
				env.env_objects[obj]={"body" : args2,"params" : args1}
				env.env_global[obj]={"type" : "function"}
			else:
				varobj=args1
				
				if args1[0]=="NUMBER":
					varvalue=args1[1]

					if args2 in ["+=","-=","*=","/="]:
						origvalue=env.env_local[obj][1]

						if args2=="+=":
							varvalue=origvalue+varvalue
						elif args2=="-=":
							varvalue=origvalue-varvalue
						elif args2=="*=":
							varvalue=origvalue*varvalue
						elif args2=="/=":
							varvalue=origvalue/varvalue
							
					varobj=("NUMBER",float(varvalue))
					
				env.env_local[obj]=varobj

	def eval_codebody(self,codebody):
		if codebody!=None:
			for line in range(0,len(codebody)):
				rtnstate=self.eval_code(codebody[line])
			
				if rtnstate is not None: 
					return rtnstate
		return None

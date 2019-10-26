#------------------------------------------------------------
# Parses Tokens into format:- 
# (Line No,Method Action, Method Type,Action 1, Action 2,Action 3)
#------------------------------------------------------------
# Method Actions:-
#	Operation
#	Assignment
#	Logical
#	Call
#------------------------------------------------------------

import bard_lex
import bard_env as env
import pprint

class bard_parser:
	def __init__(self,tokens):
		self.tokens=tokens
		self.isfunc=False
		self.currenttoken=""
		
	def parsetoken(self,tok_prev):
		spos=0
		indent="\t"
		codebody1=""
		codebody2=""
		currline=env.currentline
		action="Call"
					
		while env.prog[env.currentline][spos:spos+1]=="\t":
			indent+="\t"
			spos+=1

		try:
			tok_type,tok_value=next(self.tokens)
			#print(tok_type,tok_value)
			self.currenttoken=(tok_type,tok_value)
			
			if tok_type in ("NUMBER","IDENTIFIER","STRING") and tok_prev is None:
				return self.parsetoken((tok_type, tok_value))
			elif tok_type=="OPERATOR":
				if tok_prev[1][0:1]=="_":
					return self.parsetoken(("FUNCTION",tok_prev[1]))
				else:
					tok_next=self.parsetoken(None)

					if tok_value in ["=","+=","-=","*=","/="]:
						return ((env.currentline+1, "Assignment", tok_prev,tok_next,tok_value,None))
					elif tok_value in "+-*/^%==!==><=":
						return ((env.currentline+1, "Operation", (tok_type,tok_value),tok_prev,tok_next,None))
					elif tok_value in "&&||":
						return ((env.currentline+1,"Logical", (tok_type,tok_value),tok_prev,tok_next,None))
			elif tok_value in ",])":
				return tok_prev
			elif tok_value in "(":
				params=self.function_params()

				if tok_prev is None:
					return self.function_params(tok_value)
				elif tok_prev[0] in "KEYWORD,IDENTIFIER,FUNCTION":
					if tok_prev[1] in ["IF","ELSE","LOOP","FUNCTION"]:
						#print(len(indent))
						codebody1=self.code_block(indent)

						if env.prog[env.currentline+1].strip()[0:4].upper()=="ELSE":
							#print("ELSE")
							codebody2=self.code_block(indent[0:len(indent)-1])
							
					if tok_prev[0]=="FUNCTION": action="Assignment"
					#pprint.pprint((currline,action,tok_prev,params,codebody1,codebody2))
					return ((env.currentline+1,action,tok_prev,params,codebody1,codebody2))
				return self.function_params(tok_value)
			else:
				if tok_type in "KEYWORD,IDENTIFIER,FUNCTION":
					return self.parsetoken((tok_type,tok_value))
				else:
					return tok_prev[1]
		except:
			if tok_prev==None:
				pass
			elif tok_prev[1]=="ELSE":
				return ((env.currentline+1,"Call",tok_prev,("BOOLEAN",True),self.code_block(),None))

			return tok_prev

	def function_params(self):
		tok_params=[]
		curr_param=""
		prev_param=""
		
		while self.currenttoken[1] not in "])":
			if self.currenttoken[1] in "(,":
				curr_param=self.parsetoken(None)
			else:
				curr_param=self.parsetoken(curr_param)

			if self.currenttoken[1] in ",)":
				tok_params.append(curr_param)
							
		self.currenttoken=("End","End")

		return(tok_params)

	def code_block(self,indent):
		codebody=[]

		#print(env.prog[env.currentline])
		#print(env.currentline ,env.prog[env.currentline])

		try:
			while True:
				env.currentline+=1
				#print(env.currentline ,env.prog[env.currentline])
				if env.prog[env.currentline].strip()=="":		#Check whether current is a blank line
					pass
				elif env.prog[env.currentline][0:len(indent)]==indent: #or "ELSE" in env.prog[env.currentline][0:len(indent)+3].upper():
					lex=bard_lex.bard_lex(env.prog[env.currentline])
					p=bard_parser(lex.tokenize())

					funbody=p.parsetoken(None)
					
					if funbody is not None:
						codebody.append(funbody)
						#env.currentline-=1
						#print(env.currentline)
				else:
					#print(env.currentline,env.prog[env.currentline-1])
					env.currentline-=1
					#print(env.currentline,env.prog[env.currentline-1])
					break

		except:
			pass
		#print(len(codebody),codebody) 
		if len(codebody)==0: 
			return None
		#elif len(codebody)==1:
			#print(codebody)
		#	return codebody[0]
		else:
			#print("1: ",codebody[0]) 
			#print("2: ",codebody[1]) 
			return(codebody)


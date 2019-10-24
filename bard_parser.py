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
		
		while env.prog[env.currentline-1][spos:spos+1]=="\t":
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
						return ((env.currentline, "Assignment", tok_prev,tok_next,tok_value,None))
					elif tok_value in "+-*/^%==!==><=":
						return ((env.currentline, "Operation", (tok_type,tok_value),tok_prev,tok_next,None))
					elif tok_value in "&&||":
						return ((env.currentline,"Logical", (tok_type,tok_value),tok_prev,tok_next,None))
			elif tok_value in ",])":
				return tok_prev
			elif tok_value in "(":
				params=self.function_params()

				if tok_prev is None:
					return self.function_params(tok_value)
				elif tok_prev[0] in "KEYWORD,IDENTIFIER,FUNCTION":
					action="Call"

					codebody1=self.code_block(indent)
					
					if env.prog[env.currentline].strip()[0:4].upper()=="ELSE":
						codebody2=self.code_block(indent)
					
					if tok_prev[0]=="FUNCTION": action="Assignment"

					return ((env.currentline,action,tok_prev,params,codebody1,codebody2))
				return self.function_params(tok_value)
			else:
				if tok_type in "KEYWORD,IDENTIFIER,FUNCTION":
					return self.parsetoken((tok_type,tok_value))
				else:
					return tok_prev
		except:
			if tok_prev==None:
				pass
			elif tok_prev[1]=="ELSE":
				return ((env.currentline,"Call",tok_prev,("BOOLEAN",True),self.code_block(),None))

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

		try:
			while True:
				env.currentline+=1
				#print(env.prog[env.currentline])
				if env.prog[env.currentline-1].strip()=="":		#Check whether current is a blank line
					pass
				elif env.prog[env.currentline-1][0:len(indent)]==indent:
					#print("CurrLineA: ",env.currentline,len(indent),env.prog[env.currentline-1])
					lex=bard_lex.bard_lex(env.prog[env.currentline-1])
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
		
		if len(codebody)==0: codebody=None
		
		#pprint.pprint(codebody)
		return(codebody)


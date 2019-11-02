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
					elif tok_value in "+-*/^%==!==><=|":
						return ((env.currentline+1, "Operation", (tok_type,tok_value),tok_prev,tok_next,None))
					elif tok_value in ["&&","||"]:
						return ((env.currentline+1,"Logical", (tok_type,tok_value),tok_prev,tok_next,None))
			elif tok_value in ",])":
				return tok_prev
			elif tok_value in "(":
				params=self.function_params()

				if tok_prev is None:
					return self.function_params(tok_value)
				elif tok_prev[0] in "KEYWORD,IDENTIFIER,FUNCTION":
					if tok_prev[1] in ["IF","ELSE","LOOP"] or tok_prev[0]=="FUNCTION":
						codebody1=self.code_block(indent)

						if env.prog[env.currentline+1].strip()[0:4].upper()=="ELSE":
							codebody2=self.code_block(indent[0:len(indent)-1])
							
					if tok_prev[0]=="FUNCTION": action="Assignment"
					#print()
					#print("Code: ")
					#pprint.pprint((currline,action,tok_prev,params,codebody1,codebody2))
					return ((currline+1,action,tok_prev,params,codebody1,codebody2))
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
				return ((currline+1,"Call",tok_prev,("BOOLEAN",True),self.code_block(indent),None))

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
		temp=""
		elsekywd=False
		
		try:
			while True:
				env.currentline+=1
				#temp=env.prog[env.currentline].strip()
				
				if env.prog[env.currentline].strip()=="" or env.prog[env.currentline].strip()[0:1]=="#":	#Check whether current is a blank line
					#print("Blank: ",env.currentline)
					pass
				elif env.prog[env.currentline][0:len(indent)]==indent and elsekywd==False: 
					#print("1")
					
					if (env.prog[env.currentline].strip()[0:4]).upper()=="ELSE": elsekywd=True
					
					lex=bard_lex.bard_lex(env.prog[env.currentline])
					p=bard_parser(lex.tokenize())

					funbody=p.parsetoken(None)
					
					if funbody is not None:
						#print(funbody)
						codebody.append(funbody)
				else:
					#print("Break: ",env.currentline)
					env.currentline-=1

					break

		except:
			pass
		#pprint.pprint(codebody)
		if len(codebody)==0: 
			return None
		else:
			return(codebody)


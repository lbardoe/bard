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
				if tok_prev is None:
					return self.function_params(tok_value)
				elif tok_prev[0] in "KEYWORD,IDENTIFIER,FUNCTION":
					params=self.function_params()
					
					if tok_prev[0]=="FUNCTION":
						return ((env.currentline,"Assignment",tok_prev,params,self.function_body(),None))
					elif tok_prev[1]=="LOOP":
						return ((env.currentline,"Call",tok_prev,params,self.function_body(),None))
					elif tok_prev[1] in ["IF","ELSE"]:
						return ((env.currentline,"Call",tok_prev,params,self.function_body(),self.function_body(True)))
					else:
						return ((env.currentline,"Call",tok_prev,params,None,None))

				return self.function_params(tok_value)
			else:
				if tok_type in "KEYWORD,IDENTIFIER,FUNCTION":
					#if tok_value=="ELSE":
					#	return ((env.currentline,"Call",(tok_type,tok_value),None,self.function_body(),None))
					#else:
						return self.parsetoken((tok_type,tok_value))
				else:
					return tok_prev
		except:
			#if tok_value=="ELSE":
			#	return ((env.currentline,"Call",(tok_type,tok_value),None,self.function_body(),None))
			#print("Test2")
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

	def function_body(self,elsestatement=False):
		spos=0
		indent="\t"
		codebody=[]

		while env.prog[env.currentline-1][spos:spos+1]=="\t":
			indent+="\t"
			spos+=1
			
		if (env.prog[env.currentline-1][0:len(indent)+3]).upper()=="ELSE" and elsestatement==True:
			print("Code: ",env.prog[env.currentline-1])
			lex=bard_lex.bard_lex(env.prog[env.currentline-1])
			p=bard_parser(lex.tokenize())

			return p.parsetoken(None)
						
			
		try:
			while True:
				env.currentline+=1
				print("CurrLine: ",env.currentline)

				if env.prog[env.currentline-1].strip()=="":		#Check whether current is a blank line
					pass
				elif env.prog[env.currentline-1][0:len(indent)]==indent:
					lex=bard_lex.bard_lex(env.prog[env.currentline-1])
					p=bard_parser(lex.tokenize())

					funbody=p.parsetoken(None)
					
					if funbody is not None:
						codebody.append(funbody)
				else:
					#print(env.currentline)
					#env.currentline+=-2
					break

		except:
			pass
		
		if len(codebody)==0: codebody=None
		
		print("End: ",env.currentline)
		return(codebody)


#------------------------------------------------------------
#Parses Tokens into format:- 
#(Method Action, Line Number, Method Type,Action 1, Action 2)
#------------------------------------------------------------
#Method Actions:-
#	Operation
#	Assignment
#	Logical
#	Call
#------------------------------------------------------------

import bard_lex
import bard_env as env

class bard_parser:
	def __init__(self,tokens):
		self.tokens=tokens
		self.isfunc=False
		self.currenttoken=""
		
	def parsetoken(self,tok_prev):
		try:
			#print("Prev: ",tok_prev)
			#Read Next Token into token variables.
			tok_type,tok_value=next(self.tokens)
			#print("Token:",tok_type,tok_value)
			self.currenttoken=(tok_type,tok_value)
			
			#if tok_prev is None:
			#	self.isfunc=False

			if tok_type in ("NUMBER","IDENTIFIER","STRING") and tok_prev is None:
				return self.parsetoken((tok_type, tok_value))
			elif tok_type=="OPERATOR":
				if tok_prev[1][0:1]=="_":
					return self.parsetoken(("FUNCTION",tok_prev[1]))
				else:
					tok_next=self.parsetoken(None)

					if tok_value in ["=","+=","-=","*=","/="]:
						return ((env.currentline+1, "Assignment", tok_prev,tok_next,tok_value))
					elif tok_value in "+-*/^%==!==><=":
						return ((env.currentline+1, "Operation", (tok_type,tok_value),tok_prev,tok_next))
					elif tok_value in "&&||":
						return ((env.currentline+1,"Logical", (tok_type,tok_value),tok_prev,tok_next))
			elif tok_value in ",])":
				return tok_prev
			elif tok_value in "(":
				if tok_prev is None:
					return self.function_params(tok_value)
				elif tok_prev[0] in "KEYWORD,IDENTIFIER,FUNCTION":
					params=self.function_params()
					
					if tok_prev[0]=="FUNCTION":
						return ((env.currentline+1,"Assignment",tok_prev,params,self.function_body()))
					elif tok_prev[1]=="LOOP":
						return ((env.currentline+1,"Call",tok_prev,params,self.function_body()))
					else:
						return ((env.currentline+1,"Call",tok_prev,params,None))

				return self.function_params(tok_value)
			else:
				#if tok_value.upper()=="FN":
				#	self.isfunc=True
					
				if tok_type in "KEYWORD,IDENTIFIER,FUNCTION":
					return self.parsetoken((tok_type,tok_value))
				else:
					return tok_prev
		except:
			return tok_prev

	def function_params(self):
		tok_params=[]
		curr_param=""
		prev_param=""
		
		while self.currenttoken[1] not in "])":
			#print(1,self.currenttoken[1])
			if self.currenttoken[1] in "(,":
				#print(2,self.currenttoken[1])
				curr_param=self.parsetoken(None)
			else:
				#print(3,self.currenttoken[1])
				curr_param=self.parsetoken(curr_param)

			#print(4,self.currenttoken[1])
			if self.currenttoken[1] in ",)":
				#print(5,curr_param)
				tok_params.append(curr_param)
				
			#print(6,self.currenttoken[1])
			
		#print(7,self.currenttoken[1])
		self.currenttoken=("End","End")
		#print(self.currenttoken)
		return(tok_params)

	def function_body(self):
		spos=0
		indent="\t"
		codebody=[]

		while env.prog[env.currentline][spos:spos+1]=="\t":
			indent+="\t"
			
		try:
			while True:
				if env.prog[env.currentline+1].strip()=="":
					pass
				elif env.prog[env.currentline+1][0:len(indent)]==indent:
					lex=bard_lex.bard_lex(env.prog[env.currentline+1])
					p=bard_parser(lex.tokenize())
					
					funbody=p.parsetoken(None)
					
					if funbody is not None:
						codebody.append(funbody)
				else:
					break

				env.currentline+=1
		except:
			print("Body EOF")
			
		#print(codebody[1])
		return(codebody)


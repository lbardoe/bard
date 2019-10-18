import bard_env as env

class bard_lex():
	def __init__(self,text): 
		self.text=text

	def tokenize(self):
		self.tok_pos=0
		self.tok_end=len(self.text)
		self.tok_digits="-.0123456789"
		self.tok_chars="$_abcdefghijklmnopqrstuvwxyz0123456789"
		
		while self.tok_pos<self.tok_end:
			txt = self.text[self.tok_pos:self.tok_end]
			
			tok_type=""
			tok_value=txt[0:1]
			
			if txt[0:1] in ';\n\t ':	#New Line or Semi Colon - Denotes End of Line
				self.tok_pos += 1
			elif txt[0:1] in "=&|!+-*/^%<>":
				if txt[0:1]=="-" and txt[1:2] in "0123456789":
					yield (self.get_more(self.tok_digits))
				else:
					if txt[0:2] in ["+=","-=","*=","/=","<=",">=","&&","!=","=="]:
						tok_value += txt[1:2]
					
					yield ("OPERATOR", tok_value)
					self.tok_pos += len(tok_value)
			elif txt[0:1] in "()[],":
				yield ('PUNCTUATION',tok_value)
				self.tok_pos += 1
			elif txt[0:1]=="#":	#Comments
				self.tok_pos+=len(txt)
			elif txt[0:1] in "\"'":	#Strings
				yield (self.get_more("\"'"))
				self.tok_pos += 0
			elif txt[0:1] in self.tok_digits:	#Digits
				yield (self.get_more(self.tok_digits))
			elif txt[0:1] in self.tok_chars:
				yield (self.get_more(self.tok_chars))
			else:
				self.tok_pos += 1
				
	def get_more(self,tok_chars):
		rtn_value=""
		rtn_type=""
		endstr="\n"
		
		if self.text[self.tok_pos:self.tok_pos+1] in "\"'": 
			endstr=self.text[self.tok_pos:self.tok_pos+1]

			rtn_type="STRING"

			self.tok_pos+=1

			while self.text[self.tok_pos:self.tok_pos+1]!=endstr:
				rtn_value+=self.text[self.tok_pos:self.tok_pos+1]

				self.tok_pos += 1  
			self.tok_pos += 1  
		else:
			while (self.text[self.tok_pos:self.tok_pos+1]).lower() in tok_chars:
				rtn_value+=self.text[self.tok_pos:self.tok_pos+1]

				self.tok_pos += 1  

			if rtn_value.upper() in env.token_kywd:
				rtn_type="KEYWORD"
				rtn_value=rtn_value.upper()
			else:
				try:
					if float(rtn_value):
						pass
					rtn_type="NUMBER"
				except:
					#if rtn_value[0:1]=="_":
					#	rtn_type="FUNCTION"
					#else:
					rtn_type="IDENTIFIER"

		return (rtn_type, rtn_value)

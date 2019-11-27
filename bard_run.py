#Import additional Python Objects.
import os
import sys
import datetime
import pprint

#Import the Elements of the Bard Interpreter.
import bard_lex
import bard_parser
import bard_env as env
import bard_eval
import bard_ide

def run():
	if env.env_debug==True:
		print("-->Program Start: {}".format(datetime.datetime.now()) + "\n")

	while env.currentline < len(env.prog):
		lexer = bard_lex.bard_lex(env.prog[env.currentline])
		parser=bard_parser.bard_parser(lexer.tokenize())

		a=parser.parsetoken(None)

		if type(a)==tuple:
			codeev=bard_eval.bard_eval()
			codeev.eval_code(a) 

		env.currentline+=1

	if env.env_debug==True:
		print("\n")
		print("-->Keywords  : ",len(env.token_kywd))
		print("-->Objects   : ",env.env_global)
		print("-->Variables : ",env.env_local)
		print("-->Filename  : ",sys.argv[len(sys.argv)-1])	
		print("-->Lines     : ",len(env.prog))
		print("\n-->Program End: {}".format(datetime.datetime.now()))


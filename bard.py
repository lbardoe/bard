#----------------------------------------------------------------------------
#Bard Programming Interpreter written by Lee Bardoe (2019)
#----------------------------------------------------------------------------
#	B	Basic
#	A	and
#	R	Reduced
#	D	Definition
#----------------------------------------------------------------------------

#Import additional Python Objects.
import re
import os
import sys

import pprint

#Import the Elements of the Bard Interpreter.
import bard_lex
import bard_parser
import bard_env as env
import bard_eval
import datetime

def run(filename):
	"""This function is used to run 2b files for the BARD Interpreter."""
	with open(filename,"r") as fn:
		for line in fn:
			env.prog.append(line)
	
def interpreter():
	pass

def ide():
	pass

def err(e):
	print(e)

#run("example1.2b")
#run("example2.2b")
run("example3.2b")
#run("example4.2b")

env.env_debug=True

if env.env_debug==True:
	print("-->Program Start: {}".format(datetime.datetime.now()) + "\n")

lineno=0

while env.currentline < len(env.prog):
	lexer = bard_lex.bard_lex(env.prog[env.currentline])
	parser=bard_parser.bard_parser(lexer.tokenize())

	a=parser.parsetoken(None)
	#print(env.currentline)
	if type(a)==tuple:
		#print("Code Line: " + env.prog[env.currentline-1])
		#pprint.pprint(a)

		codeev=bard_eval.bard_eval()
		
		#print(codeev.eval_code(a)) #[1])
		codeev.eval_code(a) #[1]

	env.currentline+=1

if env.env_debug==True:
	print("\n")
	print("Globals: ",env.env_global)
	print("Locals: ",env.env_local)
	#print("Objects: ",env.env_objects)
	print("\n-->Program End: {}".format(datetime.datetime.now()))


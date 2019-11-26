#----------------------------------------------------------------------------
# BARD Programming Interpreter written by Lee Bardoe (2019)
#----------------------------------------------------------------------------
# B		Basic
# A		and
# R		Reduced
# D		Definition
#----------------------------------------------------------------------------

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

#Import additional Python Objects.
import os
import sys

import pprint

#Import the Elements of the Bard Interpreter.
import bard_lex
import bard_parser
import bard_env as env
import bard_eval
import bard_ide
import datetime

def run(filename):
	"""This function is used to run 2b files for the BARD Interpreter."""
	with open(filename,"r") as fn:
		for line in fn:
			env.prog.append(line)
	
def interpreter():
	print("This feature is currently under developement.")
	print()
	#pass

def ide():
	bard_ide.open_ide()
	#print("This feature is currently under developement.")
	#print()
	
def err(e):
	print(e)

if len(sys.argv)==1:
	interpreter()
else:
	if sys.argv[1]=="/d": 
		env.env_debug=True
		run(sys.argv[len(sys.argv)-1])
	elif sys.argv[1]=="/l":
		print("This feature is currently under developement.")
		print()
	elif sys.argv[1]=="/i":
		ide()
	else:
		run(sys.argv[len(sys.argv)-1])
	
#run("example1.2b")
#run("example2.2b")
#run("example3.2b")
#run("example4.2b")


if env.env_debug==True:
	print("-->Program Start: {}".format(datetime.datetime.now()) + "\n")

while env.currentline < len(env.prog):
	lexer = bard_lex.bard_lex(env.prog[env.currentline])
	parser=bard_parser.bard_parser(lexer.tokenize())

	a=parser.parsetoken(None)

	if type(a)==tuple:
		codeev=bard_eval.bard_eval()
		codeev.eval_code(a) #[1]

	env.currentline+=1

if env.env_debug==True:
	print("\n")
	print("-->Number of Keywords: ",len(env.token_kywd))
	print("-->Globals: ",env.env_global)
	print("-->Locals : ",env.env_local)
	#print("Objects: ",env.env_objects)
	print("\n-->Program End: {}".format(datetime.datetime.now()))


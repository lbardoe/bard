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
import os, fnmatch
import sys
import datetime
import pprint

#Import the Elements of the Bard Interpreter.
import bard_lex
import bard_parser
import bard_env as env
import bard_eval
import bard_ide
import bard_run

def loadfile(filename):
	"""This function is used to run 2b files for the BARD Interpreter."""
	with open(filename,"r") as fn:
		for line in fn:
			env.prog.append(line)

	bard_run.run()
	
def interpreter():
	print("BARD Programming Language. (Basic And Reduced Definition).\nVersion : " + env.version + " on " + sys.platform + "\n\nType Help or ? for Assistance or Quit/Exit/Q or E to exit.")
	print()
	
	intvalue=""
	
	while intvalue not in ["q","Q","Quit","quit","Exit","exit"]:
		intvalue=input("-->")

		if intvalue.upper()[0:4]=="LIST":
			print("Num. : Code")
			
			for x in range(len(env.prog)):
				print("{: 4}".format(x+1) + " : " +env.prog[x].rstrip())
		elif intvalue.upper()[0:3]=="RUN":
			env.currentline=0
			bard_run.run()
		elif intvalue.upper()[0:4]=="HELP" or intvalue[0]=="?":
			print("Interpreter Keywords:")
			print("-------------------------------------")
			
			for x in range(len(env.inter_kywd)):
				print(">> " + env.inter_kywd[x])
				
			print("\n")
			print("Language Keywords:")
			print("-------------------------------------")
			
			for x in range(len(env.token_kywd)):
				print(">> " + env.token_kywd[x])
			
			print("\n")
		elif intvalue.upper()[0:3]=="DEL":
			env.prog=[]
		elif intvalue.upper()[0:4]=="LOAD":
			vfile=intvalue[4:len(intvalue)].strip()
			vfiles=fnmatch.filter(os.listdir("."),vfile + "*.2b")
			
			for x in range(len(vfiles)):
				print(">> " + vfiles[x])
				
			if len(vfiles)==1:
				loadfile(vfiles[x])
		else:
			env.prog.append(intvalue + "\n")
			env.currentline=len(env.prog)-1
		
			bard_run.run()

def ide():
	bard_ide.open_ide()
	
def err(e):
	print(e)

if len(sys.argv)==1:
	interpreter()
else:
	if sys.argv[1]=="/d": 	#Debugging
		env.env_debug=True
		loadfile(sys.argv[len(sys.argv)-1])
	elif sys.argv[1]=="/l":	#Logging
		print("This feature is currently under developement.")
		print()
	elif sys.argv[1]=="/i":	#IDE
		ide()
	else:					#Load File Only
		loadfile(sys.argv[len(sys.argv)-1])
	

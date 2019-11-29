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
import sys

#Import the Elements of the Bard Interpreter.
import bard_env as env
import bard_ide
import bard_interpreter as inter
import bard_ops as ops
	
if len(sys.argv)==1:
	inter.interpreter()
else:
	if sys.argv[1]=="/d": 	#Debugging
		env.env_debug=True
		ops.loadfile(sys.argv[len(sys.argv)-1])
	elif sys.argv[1]=="/l":	#Logging
		print("This feature is currently under developement.")
		print()
		pass
		
	elif sys.argv[1]=="/i":	#IDE
		bard_ide.open_ide()
	else:					#Load File Only
		ops.loadfile(sys.argv[len(sys.argv)-1])
	

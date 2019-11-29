#Import the Elements of the Bard Interpreter.
import bard_env as env
import bard_run
import datetime

def loadfile(filename):
	"""This function is used to run 2b files for the BARD Interpreter."""
	reset()
	
	with open(filename,"r") as fn:
		for line in fn:
			env.prog.append(line)

	bard_run.run()

def savefile(filename):
	if len(filename)>0:
		if ".2b" not in filename:
			filename+=".2b"
	else:
		filename=datetime.datetime.now()
		filename=filename.strftime("%Y%m%d%H%M%S") + ".2b"
		
	if len(env.prog)>0:
		print("Saving : " + filename + ".....")
		
		with open(filename,"w") as file:
			for x in env.prog:
				file.write(str(x))

		print("File Saved.")
def reset():
	env.prog=[]
	env.currentline=len(env.prog)
		

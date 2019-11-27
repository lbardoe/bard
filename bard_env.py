#Declare the Enviroments for storing Global and Local Objects.
env_global={}
env_local={}
env_objects={}
env_debug=False

prog=[]
currentline=0

version="20190901.1 (Lee Bardoe)"

#Store a list of BARD Keywords.
token_kywd=["IF","ELSE","PUT","LOOP","FILE","DATE","RTN","CAST","CASE","GET","IMP","TYPE","WAIT","ASCII","TRUE","FALSE"]
inter_kywd=["LIST","SAVE","LOAD","EXIT","E","QUIT","Q","HELP","?","DEL","RUN"]

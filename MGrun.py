#!/usr/bin/env python
import os, sys
from setup import processes, HTbins, MGcmd, QCUT
from subprocess import call, check_output

username=None
process=None
MGDIR=None

#=======================================================================
# Read config file
if not os.path.isfile("config") :
	print "Could not locate config file, aborting..."
	sys.exit()
configFile="config"
f = open(configFile,'r')
lines = f.readlines()
f.close()
for line in lines:
	if line.startswith("#") : continue
	l = line.partition('#')[0]
	l = l.split('=')
	if not l : continue
	tag = l[0].strip()
	if tag == "username" : username = l[1].strip()
	elif tag == "process" : process = l[1].strip()
	elif tag == "MGpath" : MGDIR = (l[1].strip()).rstrip(str(os.sep))

# Check if config parameters are valid 
if not username :
	print "Invalid username, aborting..."
	sys.exit()
if (not process) or (process not in processes) :
	print "Invalid process name, aborting..."
	sys.exit()
if (not MGDIR) or (not os.path.exists(MGDIR)):
	print "Could not locate Madgraph directory, aborting..."
	sys.exit()
	
#======================================================================
# Setup data directory 
OutDIR = os.path.join("/users", username, 
						"data", username, "100TeV", process)
MGoutDIR = os.path.join(OutDIR, "MG")
if not os.path.exists(OutDIR):
	os.makedirs(OutDIR)
if not os.path.exists(MGoutDIR):
	os.makedirs(MGoutDIR)
for HTbin in HTbins :
	HTbinDIR = os.path.join(OutDIR, HTbin)
	if not os.path.exists(HTbinDIR):
		os.makedirs(HTbinDIR)
	

#======================================================================
# Compile madgraph
if not os.path.exists( os.path.join(MGoutDIR, "bin") ):
	print "Compiling Madgraph for the process "+process
	MGrun = os.path.join(MGDIR, "bin", "mg5_aMC")
	cmdFile = "MGrun.cmd"
	f=open(cmdFile, 'w')  
	f.write("import model sm-no_b_mass\n")
	f.write(MGcmd[process])
	f.write("\noutput "+MGoutDIR)
	f.close()
	call([MGrun, cmdFile])
else :
	print "Madgraph already compiled for the process "+process


#======================================================================
# Set madgraph cards
call("cp "+os.path.join("Cards","*.dat")+" "+ 
				os.path.join(MGoutDIR, "Cards")+os.sep, shell=True)
qcut = QCUT[process]
MGrun = os.path.join(MGoutDIR, "bin", "madevent")
cmdFile = "MGrun.cmd"
f=open(cmdFile, 'w')
f.write("generate_events\n")
#f.write("  set nevents 100\n") #debug 
f.write("  set ptj "+str(qcut)+"\n")
f.write("  set ptb "+str(qcut)+"\n")
f.write("  set mmjj "+str(qcut)+"\n")
f.write("  set mmbb "+str(qcut)+"\n")
f.write("  set xqcut "+str(qcut)+"\n")
f.close()
PythiaCard = os.path.join(MGoutDIR,"Cards","pythia_card.dat")
with open(PythiaCard,'a') as f:
	f.write("      QCUT = "+str(qcut)+"\n")


#======================================================================
# Run madgraph -- generate events
def RunMG() :
	call("rm -r "+os.path.join(MGoutDIR, "Events", "run_*"),shell=True)
	call("rm -r "+os.path.join(MGoutDIR, "RunWeb"),shell=True)
	MGrun = os.path.join(MGoutDIR, "bin", "madevent")
	for HTbin in HTbins :
		DIR=os.path.join(OutDIR, HTbin)
		for i in range(6):
			tag=str(i+1).zfill(3)
			rootfile=os.path.join(DIR, tag+'.root')
			txtfile=os.path.join(DIR, tag+'.txt')
			if os.path.isfile(rootfile) :
				continue
			STmin, STmax = HTbin.split("-")
			with open(cmdFile, 'a') as f:
				f.write("  set STmin "+STmin)
				f.write("  set STmax "+STmax)
			call([MGrun, cmdFile])
			RunDIR=os.path.join(MGoutDIR, "Events", "run_01")
			PythiaLogFile=os.path.join(RunDIR,"tag_1_pythia.log")
			RootFile=os.path.join(RunDIR,"tag_1_delphes_events.root")
			PythiaLog=check_output(["tail","-24",PythiaLogFile])
			call(["mv", RootFile, rootfile])
			f=open(txtfile,'w')
			f.write(PythiaLog)
			f.close()
			call(["rm", "-r", RunDIR])

RunMG()


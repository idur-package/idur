#!/usr/bin/python3
import os
import sys
from sys import exit
import glob
import subprocess

def main():
	arch = Arch64()
	help()
	start()
	Narg=len(sys.argv) #number of args
	if Narg > 1:
		for i in range(Narg):
			if sys.argv[i] == "in":
				print("install")
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							print(sys.argv[y])
							d_install(sys.argv[y])
					else:
						y = i
			if sys.argv[i] == "show":
				print("show details")
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							print(sys.argv[y])
							d_showdetails(sys.argv[y])
					else:
						y = i
			elif sys.argv[i] == "rm":
				print("remove")
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							print(sys.argv[y])
							d_remove(sys.argv[y])
					else:
						y = i
			elif sys.argv[i] == "up":
				print("update")
				d_updater()
				if Narg < 3:
					d_update_all()
				else:
					for y in range(Narg):
						if y > i:
							if "--" not in sys.argv[y]:
								print(sys.argv[y])
								d_update(sys.argv[y])
						else:
							y = i
			elif sys.argv[i] == "upr":
				print("update repos")
				d_updater()
			elif sys.argv[i] == "addr":
				print("add repo")
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							print(sys.argv[y])
							d_addr(sys.argv[y])
					else:
						y = i
			elif sys.argv[i] == "rmr":
				print("remove repo")
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							d_rmr(sys.argv[y])
					else:
						y = i
			elif sys.argv[i] == "lr":
				d_lr()
			elif sys.argv[i] == "l":
				d_list_all()
	exit()

def Arch64():
	if "x86_64" not in str(subprocess.check_output(["uname", "-m"])):
		return True
	else:
		return False
	

def help():
	if len(sys.argv) > 1:
		if sys.argv[1] == "--help":
			print("""
idur <command> <package>
Use:
    in <package>      Install package
    rm <package>      Remove package
    up <package>      Update package
    up                Update all package
    upr               Update just repos
    addr <repo link>  Add a new repo
    rmr <repo name>   Remove a repo
    lr                list all repo
			""")
			exit()
		if sys.argv[1] == "--version":
			print("v0.0.1")
			exit()
	else:
		print("""
idur <command> <package>
Use:
    in <package>      Install package
    rm <package>      Remove package
    up <package>      Update package
    up                Update all package
    l                 list all apps
    upr               Update just repos
    addr <repo link>  Add a new repo
    rmr <repo name>   Remove a repo
    lr                list all repo
		""")
def detect_root():
	if os.name == "posix":
		if "root" not in str(subprocess.check_output(["whoami"])):
			return False
		else:
			return True
	else:
		return True
def start():
	if detect_root() == False:
		print("need root")
		exit()
	os.system("mkdir -p /etc/idur/")
	os.system("mkdir -p /etc/idur/repos")
	os.system("mkdir -p /etc/idur/apps")


def d_install(packagename):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	sys.path.insert(1, os.path.dirname(result[0]))
	
	
	package = __import__(packagename)
	if packagename == "standard":
		exit()
	
	os.system("cp " + path + " /etc/idur/apps/" + packagename + "-v.py")
	
	for i in range(len(package.Depends)):
		os.system("apt install -y " + package.Depends[i])
	
	if Arch64():
		if package.Arch == "all":
			os.system(package.Install)
		elif package.Arch == "x86_64":
			os.system(package.Install64)
		elif package.Arch == "i386":
			print("just i386")
		elif package.Arch == "both":
			os.system(package.Install64)
	else:
		if package.Arch == "all":
			os.system(package.Install)
		elif package.Arch == "x86_64":
			print("just x86_64")
		elif package.Arch == "i386":
			os.system(package.Install32)
		elif package.Arch == "both":
			os.system(package.Install32)
def d_showdetails(packagename):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	sys.path.insert(1, os.path.dirname(result[0]))
	
	
	package = __import__(packagename)
	if packagename == "standard":
		exit()
	
	print("Name: " + package.Name)
	print("Version: " + package.Version)
	print("Maintainer: " + package.Maintainer)
	print("Contact: " + package.Contact)
	
	print("Depends: ")
	for i in range(len(package.Depends)):
		print(package.Depends[i])
	print("Architecture:")
	if package.Arch == "x86_64" or package.Arch == "all" or package.Arch == "both":
		print(" - x86_64")
	if package.Arch == "i386" or package.Arch == "all" or package.Arch == "both":
		print(" - i386")
	
	
		

def d_remove(packagename):
	sys.path.insert(1, "/etc/idur/apps")
	
	package = __import__(packagename + "-v")
	if packagename == "standard":
		exit()
	os.system(package.Remove)
	os.system("rm -vrf /etc/idur/apps/" + packagename + "-v.py")


def d_update(packagename):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	print(result[0])
	sys.path.insert(1, "/etc/idur/apps")
	
	package = __import__(packagename + "-v")
	if packagename == "standard":
		exit()
	
	if os.path.exists("/etc/idur/apps/" + packagename + "-v.py"):
		sys.path.insert(2, os.path.dirname(result[0]))
		newpackage = __import__(packagename)
		if packagename == "standard":
			exit()
		if package.Version < newpackage.Version:
			print("update")
			d_remove(packagename)
			d_install(packagename)
	else:
		print("you don't have installed " + packagename)
	
def d_update_all():
	path='/etc/idur/apps/*-v.py'
	result=glob.glob(path, recursive=True)
	for i in range(len(result)):
		name=os.path.basename(result[i])
		size = len(name)
		name = name[:size - 5]
		d_update(name)
def d_list_all():
	path='/etc/idur/apps/*-v.py'
	result=glob.glob(path, recursive=True)
	for i in range(len(result)):
		name=os.path.basename(result[i])
		size = len(name)
		name = name[:size - 5]
		print(name)
	
def d_rmr(name):
	path='/etc/idur/repos/' + name + '/standard.py'
	if os.path.exists(path):
		size=len(path)
		path = path[:size - 11]
		os.system("rm -vrf " + path)
	
def d_lr():
	path='/etc/idur/repos/*/standard.py'
	result=glob.glob(path, recursive=True)
	for i in range(len(result)):
		if os.path.exists(result[i]):
			
			npath = result[i][16:]
			size=len(npath)
			npath = npath[:size - 12]
			print(npath)
	

def d_addr(link):
	os.system("""
	cd /etc/idur/repos/
	git clone """ + link + """
	""")
def d_updater():
	result=glob.glob('/etc/idur/repos/*/standard.py', recursive=True)
	for i in range(len(result)):
		os.system("cd " + os.path.dirname(result[i]) + "&& git pull")
	



if __name__ == "__main__":
	main()

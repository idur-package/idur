#!/usr/bin/python3
import os
import sys
from sys import exit
import glob
import subprocess
import requests

def main():
	arch = Arch64()
	help()
	start()
	Narg=len(sys.argv) #number of args
	if Narg > 1:
		for i in range(Narg):
			if sys.argv[i] == "install" or sys.argv[i] == "in":
				is_root()
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							tryinternet()
							d_install(sys.argv[y])
					else:
						y = i
						
		for i in range(Narg):
			if sys.argv[i] == "reinstall" or sys.argv[i] == "rein":
				is_root()
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							tryinternet()
							d_reinstall(sys.argv[y])
					else:
						y = i
						
			if sys.argv[i] == "search" or sys.argv[i] == "se":
				
				if Narg < 3:
					d_search("", sa=False)
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							d_search(sys.argv[y])
					else:
						y = i
						
			if sys.argv[i] == "show" or sys.argv[i] == "sh":
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							d_showdetails(sys.argv[y])
					else:
						y = i
			elif sys.argv[i] == "remove" or sys.argv[i] == "rm":
				is_root()
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							d_remove(sys.argv[y])
					else:
						y = i
			elif sys.argv[i] == "update" or sys.argv[i] == "up":
				is_root()
				tryinternet()
				d_updater()
				if Narg < 3:
					d_update_all()
				else:
					for y in range(Narg):
						if y > i:
							if "--" not in sys.argv[y]:
								tryinternet()
								d_update(sys.argv[y])
						else:
							y = i
			elif sys.argv[i] == "update-repos" or sys.argv[i] == "upr":
				is_root()
				tryinternet()
				d_updater()
			elif sys.argv[i] == "add-repo" or sys.argv[i] == "addr":
				is_root()
				tryinternet()
				if len(sys.argv) > i+2:
					d_addr(sys.argv[i+1], sys.argv[i+2])
				else:
					print("add-repo <repo-name> <repo-link>")
			elif sys.argv[i] == "remove-repo" or sys.argv[i] == "rmr":
				is_root()
				for y in range(Narg):
					if y > i:
						if "--" not in sys.argv[y]:
							d_rmr(sys.argv[y])
					else:
						y = i
			elif sys.argv[i] == "list-repos" or sys.argv[i] == "lr":
				d_lr()
			elif sys.argv[i] == "l" or sys.argv[i] == "list":
				d_list_all()
			elif sys.argv[i] == "la" or sys.argv[i] == "list-all":
				all_package()
	exit()

def Arch64():
	if "x86_64" not in str(subprocess.check_output(["uname", "-m"])):
		return True
	else:
		return False
	

def help():
	helpvar="""
idur <command> <package>
Use:
    install        <package>                Install package
    remove         <package>                Remove package
    show           <package>                Show details of package
    search         <name>                   Search packages
    list                                    list all installed packages
    list-all                                list all packages
    reinstall      <package>                Reinstall package
    update         <package>                Update package
    update                                  Update all package
    update-repos                            Update just repos
    add-repo       <repo-name> <repo-link>  Add a new repo
    remove-repo    <repo name>              Remove a repo
    list-repos                              list all repo
			"""
	if len(sys.argv) > 1:
		if sys.argv[1] == "--help" or sys.argv[1] == "-h":
			print(helpvar)
			exit()
		if sys.argv[1] == "--version" or sys.argv[1] == "-v":
			print("v0.1.0")
			exit()
	else:
		print(helpvar)
def detect_root():
	if os.name == "posix":
		if "root" not in str(subprocess.check_output(["whoami"])):
			return False
		else:
			return True
	else:
		return True
def is_root():
	if detect_root() == False:
		print("need root")
		exit()
def start():
	if os.path.exists("/etc/idur/") == False:
		if detect_root():
			os.system("mkdir -p /etc/idur/")
			os.system("mkdir -p /etc/idur/repos")
			os.system("mkdir -p /etc/idur/apps")
		else:
			print("You need root")

def d_reinstall(packagename):
	d_remove(packagename)
	d_install(packagename)
	
	
def d_install(packagename):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	if len(result) == 0:
		print("Package not found")
		exit()
	sys.path.insert(1, os.path.dirname(result[0]))
	
	package = __import__(packagename)
	if packagename == "standard":
		exit()
		
	if hasattr(package, 'Conflict'):
		for i in range(len(package.Conflict)):
			if package.Conflict[i] in str(subprocess.check_output(["apt", "list", "--installed", package.Conflict[i]])):
				print(package.Conflict[i] + " is in conflict with " + packagename)
				exit()
			elif os.path.exists("/usr/bin/idur"):
				if package.Conflict[i] in str(subprocess.check_output(["idur", "l"])):
					print(package.Conflict[i] + " is in conflict with " + packagename)
					exit()
	
	os.system("cp " + path + " /etc/idur/apps/" + packagename + "-v.py")
	
	if hasattr(package, 'Depends'):
		for i in range(len(package.Depends)):
			os.system("apt install -y " + package.Depends[i])
	if hasattr(package, 'idurDepends'):
		for i in range(len(package.idurDepends)):
			os.system("idur install " + package.idurDepends[i])
	
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
	if len(result) == 0:
		print("Package not found")
		exit()
	sys.path.insert(1, os.path.dirname(result[0]))
	
	
	package = __import__(packagename)
	if packagename == "standard":
		exit()
	
	print("Name: " + package.Name)
	if hasattr(package, 'Version'):
		print("Version: " + str(package.Version))
	print("Maintainer: " + package.Maintainer)
	if hasattr(package, 'Contact'):
		print("Contact: " + package.Contact)
	if hasattr(package, 'License'):
		print("License: " + package.License)
	
	if hasattr(package, 'Depends'):
		print("Depends: ")
		for i in range(len(package.Depends)):
			print(" - " + package.Depends[i])
	if hasattr(package, 'idurDepends'):
		print("idurDepends: ")
		for i in range(len(package.idurDepends)):
			print(" - " + package.idurDepends[i])
	print("Architecture:")
	if package.Arch == "x86_64" or package.Arch == "all" or package.Arch == "both":
		print(" - x86_64")
	if package.Arch == "i386" or package.Arch == "all" or package.Arch == "both":
		print(" - i386")
	
	print("Description: ")
	print(package.Description)
	
	
		

def d_remove(packagename):
	sys.path.insert(1, "/etc/idur/apps")
	
	if os.path.exists("/etc/idur/apps/" + packagename + "-v.py") == False:
		print("you don't have installed " + packagename)
		exit()
	
	package = __import__(packagename + "-v")
	if packagename == "standard":
		exit()
	os.system(package.Remove)
	os.system("rm -vrf /etc/idur/apps/" + packagename + "-v.py")


def d_update(packagename):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	if len(result) == 0:
		print("Package not found")
		exit()
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
	else:
		print("you don't have this repository")
	
def d_lr():
	path='/etc/idur/repos/*/standard.py'
	result=glob.glob(path, recursive=True)
	for i in range(len(result)):
		if os.path.exists(result[i]):
			
			npath = result[i][16:]
			size=len(npath)
			npath = npath[:size - 12]
			print(npath)
	

def d_addr(name, link):
	if os.path.exists("/etc/idur/repos/" + name) == False:
		os.system("""
		cd /etc/idur/repos/
		git clone """ + link + " " + name)
def d_updater():
	result=glob.glob('/etc/idur/repos/*/standard.py', recursive=True)
	for i in range(len(result)):
		os.system("cd " + os.path.dirname(result[i]) + "&& git pull")
	
def _read_desc(pathd):
	sys.path.insert(1, os.path.dirname(pathd))
	packagename = os.path.basename(pathd)
	packagename = packagename[:len(packagename) - 3]
	package = __import__(packagename)
	
	prithis= package.Description.replace('\n', ' ')
	
	print("- " + prithis[0:50] + "...")
def d_search(packagename, sa=False):
	if sa:
		path="/etc/idur/repos/*/*"
	else:
		path='/etc/idur/repos/*/*' + packagename + '*.py'
	result=glob.glob(path, recursive=True)
	for i in range(len(result)):
		pit=os.path.basename(result[i])
		pit = pit[:len(pit) - 3]
		if pit != "standard":
			print(pit)
			_read_desc(result[i])

def internet():
	url = "https://github.com/idur-package"
	timeout = 5
	try:
		request = requests.get(url, timeout=timeout)
		return True
		
	except (requests.ConnectionError, requests.Timeout) as exception:
		return False
def tryinternet():
	result=internet()
	if result:
		print("Connected to the Internet")
	else:
		print("No internet connection.")
		exit()
def all_package():
	path="/etc/idur/repos/*/*"
	result=glob.glob(path, recursive=True)
	for i in range(len(result)):
		pit=os.path.basename(result[i])
		pit = pit[:len(pit) - 3]
		if pit != "standard" and pit != "__pycach":
			print(pit)

if __name__ == "__main__":
	main()

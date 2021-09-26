#!/usr/bin/python3
import os
import sys
from sys import exit
import glob
import subprocess
import requests
import importlib
from colorama import Fore as COLOR

# Main Function
def main():
	arch = Arch64()
	check_help()
	create_initial_folders()
	arg_amount=len(sys.argv) #number of args
	
	recommends=False
	suggests=False
	ignore=False
	check=True
	always_yes=False
	
	if arg_amount > 1:
		for i in range(arg_amount):
			if sys.argv[i] == "install" or sys.argv[i] == "in":
				check_root()
				for y in range(arg_amount):
					if y > i:
						if sys.argv[y] == "-r" or sys.argv[y] == "--recommends":
							recommends=True
						elif sys.argv[y] == "-s" or sys.argv[y] == "--suggests":
							suggests=True
						elif sys.argv[y] == "-i" or sys.argv[y] == "--ignore":
							ignore=True
						elif sys.argv[y] == "-y" or sys.argv[y] == "--yes":
							always_yes=True
						elif "--" not in sys.argv[y]:
							check_internet()
							install_package(sys.argv[y], rec=recommends, sug=suggests, ignore=ignore, yes=always_yes)
					else:
						y = i
			if sys.argv[i] == "show-install" or sys.argv[i] == "showin":
				for y in range(arg_amount):
					if y > i:
						if "--" not in sys.argv[y]:
							show_install_instructions(sys.argv[y])
					else:
						y = i
			if sys.argv[i] == "show-remove" or sys.argv[i] == "showrm":
				for y in range(arg_amount):
					if y > i:
						if "--" not in sys.argv[y]:
							show_remove_instructions(sys.argv[y])
					else:
						y = i
						
						
		for i in range(arg_amount):
			if sys.argv[i] == "reinstall" or sys.argv[i] == "rein":
				check_root()
				for y in range(arg_amount):
					if y > i:
						if sys.argv[y] == "-i" or sys.argv[y] == "--ignore":
							ignore=True
						elif sys.argv[y] == "-y" or sys.argv[y] == "--yes":
							always_yes=True
						elif "--" not in sys.argv[y]:
							check_internet()
							reinstall_packages(sys.argv[y], ignore=ignore, yes=always_yes)
					else:
						y = i
						
			if sys.argv[i] == "search" or sys.argv[i] == "se":
				if arg_amount < 3:
					search_packages("", search_all=False)
				for y in range(arg_amount):
					if y > i:
						if "--" not in sys.argv[y]:
							search_packages(sys.argv[y])
					else:
						y = i
						
			if sys.argv[i] == "show" or sys.argv[i] == "sh":
				for y in range(arg_amount):
					if y > i:
						if "--" not in sys.argv[y]:
							show_package_details(sys.argv[y])
					else:
						y = i

			elif sys.argv[i] == "remove" or sys.argv[i] == "rm":
				check_root()
				for y in range(arg_amount):
					if y > i:
						if sys.argv[y] == "-i" or sys.argv[y] == "--ignore":
							check=False
						elif sys.argv[y] == "-y" or sys.argv[y] == "--yes":
							always_yes=True
						elif "--" not in sys.argv[y]:
							remove_package(sys.argv[y],check=check, yes=always_yes)
					else:
						y = i
			elif sys.argv[i] == "is-installed" or sys.argv[i] == "ii":
				if len(sys.argv) > 2:
					print(package_is_installed(sys.argv[2]))
			elif sys.argv[i] == "update" or sys.argv[i] == "up":
				check_root()
				check_internet()
				update_repos()
				if arg_amount < 3:
					update_all()
				else:
					if sys.argv[i-1] == "-i" or sys.argv[i-1] == "--ignore":
						if arg_amount < 4:
							update_all(ignore=True)
					elif sys.argv[i-1] == "-y" or sys.argv[i-1] == "--yes":
						if arg_amount < 4:
							update_all(yes=True)
					else:
						for y in range(arg_amount):
							if y > i:
								if sys.argv[y] == "-i" or sys.argv[y] == "--ignore":
									ignore = True
								elif sys.argv[y] == "-y" or sys.argv[y] == "--yes":
									always_yes=True
								elif "--" not in sys.argv[y]:
									check_internet()
									update_package(sys.argv[y], ignore=ignore, yes=always_yes)
							else:
								y = i

			elif sys.argv[i] == "update-repos" or sys.argv[i] == "upr":
				check_root()
				check_internet()
				update_repos()

			elif sys.argv[i] == "add-repo" or sys.argv[i] == "addr":
				check_root()
				check_internet()
				if len(sys.argv) > i+2:
					if sys.argv[i-1] == "-y" or sys.argv[i-1] == "--yes":
						always_yes=True
					add_repo(sys.argv[i+1], sys.argv[i+2],yes=always_yes)
				else:
					print("add-repo <repo-name> <repo-link>")
			elif sys.argv[i] == "remove-repo" or sys.argv[i] == "rmr":
				check_root()
				for y in range(arg_amount):
					if y > i:
						if sys.argv[y] == "-y" or sys.argv[y] == "--yes":
							always_yes=True
						elif "--" not in sys.argv[y]:
							remove_repo(sys.argv[y], yes=always_yes)
					else:
						y = i
			elif sys.argv[i] == "list-repos" or sys.argv[i] == "lr":
				list_repos()
			elif sys.argv[i] == "l" or sys.argv[i] == "list":
				list_installed()
			elif sys.argv[i] == "la" or sys.argv[i] == "list-all":
				list_all()
	exit()

# Return True if 'uname -m' == x86_64
def Arch64():
	if "x86_64" in str(subprocess.check_output(["uname", "-m"])):
		return True
	else:
		return False

# Help and version commands
def check_help():
	helptext="""
idur <command> <package>
Use:
    install        <package>                Install package
    remove         <package>                Remove package
    show           <package>                Show details of package
    show-install   <package>                Show install instructions of package
    show-remove    <package>                Show remove instructions of package
    is-installed   <package>                Show True if the package is installed
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
    help                                    see expert help
			"""
	if len(sys.argv) > 1:
		if sys.argv[1] == "--help" or sys.argv[1] == "-h":
			print(helptext)
			exit()
		if sys.argv[1] == "help" or sys.argv[1] == "h":
			print("""
idur <command> <package>
Use:
    install or in          <package>                Install package
      -r --recommends                               install also recommends
                                                    packages
      -s --suggests                                 install also suggests
                                                    packages
      -i --ignore                                   Ignore Conflicts,
                                                    Architecture, everything.
      -y --yes                                      no ask to continue

    remove or rm           <package>                Remove package
      -i --ignore                                   no check if other packages
                                                    depends on the package
                                                    that you want remove
      -y --yes                                      no ask to continue

    show or sh             <package>                Show details of package

    show-install or showin <package>                Show install instructions of package

    show-remove or showrm  <package>                Show remove instructions of package

    is-installed or ii     <package>                Show True if the package is
                                                    installed

    search or se           <name>                   Search packages

    list or l                                       list all installed packages

    list-all or la                                  list all packages

    reinstall or rein      <package>                Reinstall package
      -i --ignore                                   Ignore Conflicts,
                                                    Architecture, everything.
      -y --yes                                      no ask to continue

    update or up           <package>                Update package
      -i --ignore                                   Ignore Conflicts,
                                                    Architecture, everything.
      -y --yes                                      no ask to continue

    update or up                                    Update all package
      -i --ignore                                   Ignore Conflicts,
                                                    Architecture, everything.
                                                    (sudo idur -i update)
      -y --yes                                      no ask to continue
                                                    (sudo idur -y update)


    update-repos or upr                             Update just repos

    add-repo or addr       <repo-name> <repo-link>  Add a new repo
      -y --yes                                      no ask to continue
                        (sudo idur -y add-repo <repo-name> <repo-link>)

    remove-repo or rmr     <repo name>              Remove a repo
      -y --yes                                      no ask to continue

    list-repos or lr                                list all repo

    help or h                                       see expert help

	
    --help or -h                                    see basic help

    --version or -v                                 see version
	
	""")
			exit()
		if sys.argv[1] == "--version" or sys.argv[1] == "-v":
			print("v0.2.3")
			exit()
	else:
		print(helptext)

# Return True if the user has root power
def root():
	if os.name == "posix":
		if "root" not in str(subprocess.check_output(["whoami"])):
			return False
		else:
			return True
	else:
		return True

# Print if the user has root power
def check_root():
	if root() == False:
		print(COLOR.RED + """You're not root, you need use idur with root or an admin user
You can try:
------------
""" + COLOR.RESET + "sudo idur" + COLOR.RED + """
------------
""" + COLOR.RESET + """su root
idur""" + COLOR.RED + """
------------""" + COLOR.RESET)
		exit()

# Create the /etc/idur/
def create_initial_folders():
	if root():
		if os.path.exists("/etc/idur/") == False:
			os.system("mkdir -p /etc/idur/")
		if os.path.exists("/etc/idur/repos/") == False:
			os.system("mkdir -p /etc/idur/repos/")
		if os.path.exists("/etc/idur/apps/") == False:
			os.system("mkdir -p /etc/idur/apps/")
		if os.path.exists("/opt/idur/") == False:
			os.system("mkdir -p /opt/idur/")
		if os.path.exists("/opt/idur/bin/") == False:
			os.system("mkdir -p /opt/idur/bin/")
		if os.path.exists("/opt/idur/bin/readme.txt") == False:
			os.system('echo "exec idur-exec program to execute /opt/idur/bin/program" > /opt/idur/bin/readme.txt')
	else:
		if os.path.exists("/etc/idur/") == False or os.path.exists("/opt/idur/") == False:
			print("You need root")

# Function that remove the package, and then install the package again
def reinstall_packages(packagename, ignore=False, yes=False):
	if ignore:
		warning_ignore()
		

	if yes==False:
		print(packagename + " " + show_package_time_install(packagename))
		if print_continue() == False:
			exit()

	remove_package(packagename, check=False, ignore_check=True, yes=True)
	install_package(packagename, ignore=ignore, ignoreignore=True, yes=True)

def warning_ignore():
	print("\n\n\nWarning!!\n\n\n")
	print("-i or --ignore ignores all Depends, Conflicts and Architectures")
	ask=input("Are You Sure that you want to use the -i or --ignore parameter? (Y/n)")
	if ask.lower() == "y":
		print("Continue...")
	else:
		print("Aborting")
		exit()

# install package
def install_package(packagename, sug=False, rec=False, ignore=False, ignoreignore=False, yes=False):

	if ignore and ignoreignore==False:

		print("\n\n\nWarning!!\n\n\n")

		print("-i or --ignore ignores all Conflicts and Architectures")
		ask=input("Are You Sure that you want to use the -i or --ignore parameter? (Y/n)")
		if ask.lower() == "y":
			print("Continue...")
		else:
			print("Aborting")
			exit()

	package = load_package_from_repos(packagename)
	path = load_package_from_repos(packagename, returnpath=True)

	if Arch64():
		if package.Arch == "all" or package.Arch == "x86_64" or package.Arch == "both":
			pass
		elif package.Arch == "i386":
			print("Just x86_64")
			if ignore == False:
				exit()
	else:
		if package.Arch == "all" or package.Arch == "i386" or package.Arch == "both":
			pass
		elif package.Arch == "x86_64":
			print("Just i386")
			if ignore == False:
				exit()

	if hasattr(package, 'Conflict'):
		for i in range(len(package.Conflict)):
			if package.Conflict[i] in str(subprocess.check_output(["apt", "list", "--installed", package.Conflict[i]])):
				print(package.Conflict[i] + " is in conflict with " + packagename)
				if ignore == False:
					exit()
			elif os.path.exists("/usr/bin/idur"):
				if package_is_installed(package.Conflict[i]):
					print(package.Conflict[i] + " is in conflict with " + packagename)
					if ignore == False:
						exit()
	
	if yes==False:
		print(package.Name + " " + show_package_time_install(packagename))
		if print_continue() == False:
			exit()

	os.system("cp " + path + " /etc/idur/apps/" + packagename + "-v.py")
	
	if hasattr(package, 'Depends'):

		times=2
		while times != 0:
			print(times)
			times-=1
			#Detect Dependencies
			for i in range(len(package.Depends)):
				to_install=True
				if package.Depends[i][0:4] == "rec/":
					if rec:
						package.Depends[i] = package.Depends[i][4:len(package.Depends[i])]
					else:
						to_install=False
				elif package.Depends[i][0:4] == "sug/":
					if sug:
						package.Depends[i] = package.Depends[i][4:len(package.Depends[i])]
					else:
						to_install=False
						
				if to_install:
					
					if " " in package.Depends[i]:
						deps = package.Depends[i].split()
						to_install=True
						for j in range(len(deps)):
							if deps[j] in str(subprocess.check_output(["apt", "list", "--installed", deps[j]])):
								print(deps[j] + " is installed")
								to_install=False
						if to_install:
							os.system("apt install -y " + deps[0])
					else:
						to_install=True
						if package.Depends[i] in str(subprocess.check_output(["apt", "list", "--installed", package.Depends[i]])):
								print(package.Depends[i] + " is installed")
								to_install=False
						if to_install:
							os.system("apt install -y " + package.Depends[i])
	if hasattr(package, 'idurDepends'):
		times=2
		while times != 0:
			print(times)
			times-=1
			for i in range(len(package.idurDepends)):
				to_install=True
				if package.idurDepends[i][0:4] == "rec/":
					if rec:
						package.idurDepends[i] = package.idurDepends[i][4:len(package.idurDepends[i])]
					else:
						to_install=False
				elif package.idurDepends[i][0:4] == "sug/":
					if sug:
						package.idurDepends[i] = package.idurDepends[i][4:len(package.idurDepends[i])]
					else:
						to_install=False
						
				if to_install:
					
					if " " in package.idurDepends[i]:
						deps = package.idurDepends[i].split()
						print(deps)
						to_install=True
						for j in range(len(deps)):
							deps[j]
							if package_is_installed(deps[j]):
								print(deps[j] + " is installed")
								to_install=False
						if to_install:
							os.system("idur install -y " + deps[0])
					else:
						to_install=True
						if package_is_installed(package.idurDepends[i]):
								print(package.idurDepends[i] + " is installed")
								to_install=False
						if to_install:
							os.system("idur install -y " + package.idurDepends[i])
	


	if Arch64():
		if package.Arch == "all":
			os.system(package.Install)
		elif package.Arch == "x86_64":
			os.system(package.Install64)
		elif package.Arch == "i386":
			print("just i386")
			if ignore:
				os.system(package.Install32)
		elif package.Arch == "both":
			os.system(package.Install64)
	else:
		if package.Arch == "all":
			os.system(package.Install)
		elif package.Arch == "x86_64":
			print("just x86_64")
			if ignore:
				os.system(package.Install64)
		elif package.Arch == "i386":
			os.system(package.Install32)
		elif package.Arch == "both":
			os.system(package.Install32)

# Print the remove instructions
def show_remove_instructions(packagename):
	package = load_package_from_repos(packagename)
	if hasattr(package, 'Remove'):
		print(str(package.Remove))
	else:
		print("Error")
		
# Print the install instructions
def show_install_instructions(packagename):
	
	package = load_package_from_repos(packagename)

	if Arch64():
		if package.Arch == "all":
			if hasattr(package, 'Install'):
				print(str(package.Install))
		elif package.Arch == "x86_64":
			if hasattr(package, 'Install64'):
				print(str(package.Install64))
		elif package.Arch == "i386":
			print("just i386")
		elif package.Arch == "both":
			if hasattr(package, 'Install64'):
				print(str(package.Install64))
	else:
		if package.Arch == "all":
			if hasattr(package, 'Install'):
				print(str(package.Install))
		elif package.Arch == "x86_64":
			print("just x86_64")
		elif package.Arch == "i386":
			if hasattr(package, 'Install32'):
				print(str(package.Install32))
		elif package.Arch == "both":
			if hasattr(package, 'Install32'):
				print(str(package.Install32))
	
def show_package_time_install(packagename):
	package = load_package_from_repos(packagename)
	path = load_package_from_repos(packagename, returnpath=True)

	#print("Repo: " + path[16:len(path)][:-1*(len(packagename)+4)])
	
	if hasattr(package, 'Time'):
		return "(" + str(package.Time) + ")"
	else:
		return ""
	

# Function that print the principal features of the package, like Name, Version, Description, Architecture, etc.
def show_package_details(packagename):
	package = load_package_from_repos(packagename)
	path = load_package_from_repos(packagename, returnpath=True)
	
	print("Repo: " + path[16:len(path)][:-1*(len(packagename)+4)])
	
	
	print("Name: " + package.Name)
	if hasattr(package, 'Version'):
		print("Version: " + str(package.Version))
	print("Maintainer: " + package.Maintainer)
	if hasattr(package, 'Time'):
		print("Time (Install duration): " + package.Time)
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

# Return True if the package that you want remove, it's a depends of another package
def is_idurDepends_of_installed_packages(idurDepend):
	finded=False
	path='/etc/idur/apps/*-v.py'
	result=glob.glob(path, recursive=True)
	for i in range(len(result)):
		sys.path.insert(1, "/etc/idur/apps")
		name=os.path.basename(result[i])
		size = len(name)
		name = name[:size - 5]
		package = load_package_installed(name)
		if hasattr(package, 'idurDepends'):
			for j in range (len(package.idurDepends)):
				if package.idurDepends[j] == idurDepend:
					print(package.Name + " depends on " + idurDepend)
					finded=True
				elif " " in package.idurDepends[j]:
					package_with_options = package.idurDepends[j].split()
					for k in range (len(package_with_options)):
						if package_with_options[k] == idurDepend:
							print(package.Name + " depends on " + idurDepend)
							finded=True
	if finded:
		return True
	else:
		return False

# Function that execute the remove instructions and remove the package from /etc/idur/apps/
# idur remove <name>
def remove_package(packagename, check=True, ignore_check=False, yes=False):

	package = load_package_installed(packagename)
	
	if check:
		if is_idurDepends_of_installed_packages(packagename):
			exit()
	else:
		if ignore_check==False:
			warning_ignore()

	

	if yes==False:
		print("Remove " + package.Name)
		if print_continue() == False:
			exit()

	os.system("bash -c \"" + package.Remove + "\"")
	os.system("rm -vrf /etc/idur/apps/" + packagename + "-v.py")

# Return True if the package is in /etc/idur/apps/
def package_is_installed(packagename):
	
	if os.path.exists("/etc/idur/apps/" + packagename + "-v.py"):
		return True
	else:
		return False

def to_update(packagename):

	package = load_package_installed(packagename)

	if os.path.exists("/etc/idur/apps/" + packagename + "-v.py"):
		newpackage = load_package_from_repos(packagename)
		if package.Version < newpackage.Version:
			return True
	else:
		print("you don't have installed " + packagename)
	return False

# Function to update the package specified
# idur update <name>
def update_package(packagename, ignore=False, ignoreignore=False, yes=False):
	package = load_package_installed(packagename)

	if ignore and ignoreignore==False:
		warning_ignore()
	
	if os.path.exists("/etc/idur/apps/" + packagename + "-v.py"):
		newpackage = load_package_from_repos(packagename)
		if package.Version < newpackage.Version:
			if yes==False:
				if print_continue() == False:
					exit()
			remove_package(packagename, check=False, ignore_check=True, yes=True)
			install_package(packagename, ignore=ignore, ignoreignore=True, yes=True)
	else:
		print("you don't have installed " + packagename)
	
# Function that update all the packages (if it need update) and repositories that you have
def update_all(ignore=False, yes=False):
	path='/etc/idur/apps/*-v.py'
	result=glob.glob(path, recursive=True)

	is_updates = False

	if ignore:
		warning_ignore()


	for i in range(len(result)):
		name=os.path.basename(result[i])
		size = len(name)
		name = name[:size - 5]
		if to_update(name):
			is_updates = True
			print("- " + str(name) + " " + show_package_time_install(name))
	if is_updates:
		if yes==False:
			if print_continue() == False:
				exit()
	else:
		print("No updates")

	for i in range(len(result)):
		name=os.path.basename(result[i])
		size = len(name)
		name = name[:size - 5]
		if ignore:
			update_package(name, ignore=ignore, ignoreignore=True, yes=True)
		else:
			update_package(name, yes=True)

# Function that list all the packages that you have installed
# the installed apps are saved in /etc/idur/apps/, with -v.py
def list_installed():
	path='/etc/idur/apps/*-v.py'
	result=glob.glob(path, recursive=True)
	result=order_array(result)
	for i in range(len(result)):
		name=os.path.basename(result[i])
		size = len(name)
		name = name[:size - 5]
		print(name)
	
# Function that remove the repository specified
# idur remove-repo <name>
def remove_repo(name, yes=False):
	
	path='/etc/idur/repos/' + name + '/standard.py'
	if os.path.exists(path):
		size=len(path)
		path = path[:size - 11]

		if yes==False:
			if print_continue() == False:
				exit()

		os.system("rm -vrf " + path)
	else:
		print("you don't have this repository")
	
# Function that list all the repositories that you have cloned in /etc/idur/repos/
def list_repos():
	path='/etc/idur/repos/*/standard.py'
	result=glob.glob(path, recursive=True)
	result=order_array(result)
	for i in range(len(result)):
		if os.path.exists(result[i]):
			
			package_name = result[i][16:]
			size=len(package_name)
			package_name = package_name[:size - 12]
			print(package_name)

# Function that clone the git repo, and it save in /etc/idur/repos/
# idur add-repo <name> <link>
def add_repo(name, link, yes=False):
	if yes==False:
		if print_continue() == False:
			exit()
	if os.path.exists("/etc/idur/repos/" + name) == False:
		os.system("""
		cd /etc/idur/repos/
		git clone """ + link + " " + name)

# Function that update the repositories
# git pull in /etc/idur/repos/*/
#
# idur update-repos
def update_repos():
	print(COLOR.GREEN)
	result=glob.glob('/etc/idur/repos/*/standard.py', recursive=True)
	for i in range(len(result)):
		os.system("cd " + os.path.dirname(result[i]) + " && git pull")
	print(COLOR.RESET)

# Print the Description of the path_input
def print_description_of_path(path_input):
	package = load_package_from_path(path_input)
	
	description = package.Description.replace('\n', ' ')
	
	print("- " + description[0:50] + "...")

# Return True if the searchword is in the Description of path_input
def search_on_description(path_input, searchword):
	packagename = os.path.basename(path_input)
	packagename = packagename[:len(packagename) - 3]
	if packagename != "__pycach" and packagename != "standard":
		package = load_package_from_repos(packagename)
	
		if searchword.lower() in package.Description.lower():
			return True
		else:
			return False
	else:
		return False

# Search available packages
# The "Search Engine" is based on if the input is in the Name or Description
def search_packages(packagename, search_all=False):
	if search_all:
		path="/etc/idur/repos/*/*"
	else:
		path='/etc/idur/repos/*/*' + packagename + '*.py'
	result=glob.glob(path, recursive=True)
	result=order_array(result)
	if search_all==False and packagename != "":

		# Description Search
		print("\nDescription Search")
		dpath="/etc/idur/repos/*/*"
		dresult=glob.glob(dpath, recursive=True)
		dresult=order_array(dresult)
		for j in range(len(dresult)):
			result_out = os.path.basename(dresult[j])
			result_out = result_out[:len(result_out) - 3]
			if result_out != "standard" or result_out != "__pycach":
				if search_on_description(dresult[j], packagename):
					print()
					if package_is_installed(result_out):
						print(result_out + COLOR.GREEN + " (is installed)" + COLOR.RESET)
					else:
						print(result_out)
					print_description_of_path(dresult[j])
	
	# Name Search
	print("\nName Search")
	for i in range(len(result)):
		result_out=os.path.basename(result[i])
		result_out = result_out[:len(result_out) - 3]
		if result_out != "standard":
			print()
			if package_is_installed(result_out):
				print(result_out + COLOR.GREEN + " (is installed)" + COLOR.RESET)
			else:
				print(result_out)
			print_description_of_path(result[i])

# Return True if there is internet
def internet():
	url = "https://github.com/idur-package"
	timeout = 5
	try:
		request = requests.get(url, timeout=timeout)
		return True
		
	except (requests.ConnectionError, requests.Timeout) as exception:
		return False

# Print if there is internet
def check_internet():
	result=internet()
	if result:
		print(COLOR.GREEN + "Connected to the Internet" + COLOR.RESET)
	else:
		print(COLOR.RED + "No internet connection." + COLOR.RESET)
		exit()

# list all available packages
def list_all():
	path="/etc/idur/repos/*/*"
	result=glob.glob(path, recursive=True)
	result=order_array(result)
	for i in range(len(result)):
		result_out = os.path.basename(result[i])
		result_out = result_out[:len(result_out) - 3]
		if result_out != "standard" and result_out != "__pycach":
			if package_is_installed(result_out):
				print(result_out + COLOR.GREEN + " (installed)" + COLOR.RESET)
			else:
				print(result_out)
def print_continue():
	while True:
		ask = input("Continue? (Y/n)")
		if ask.lower() == "y":
			return True
		elif ask.lower() == "n":
			return False
# alphabetical order
def order_array(output):
	output_amount = len(output)
	with_problem = True

	while with_problem:
		with_problem = False
		for i in range(output_amount):
			if i != 0:
				if output[i] < output[i-1]:
					number_temp = output[i-1]
					output[i-1] = output[i]
					output[i] = number_temp
					with_problem = True
	
	return output
def load_package_from_path(pathvar):
	result=glob.glob(pathvar, recursive=True)
	if len(result) == 0:
		print("Package not found")
		exit()
	packagename = os.path.basename(pathvar)
	packagename = packagename[:-3]
	if packagename == "standard":
		exit()
	spec=importlib.util.spec_from_file_location(packagename,pathvar)
	package = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(package)
	return package

def load_package_installed(packagename):
	path="/etc/idur/apps/" + packagename + "-v.py"
	result=glob.glob(path, recursive=True)
	if len(result) == 0:
		print(COLOR.RED + "Package not installed" + COLOR.RESET)
		exit()
	package = load_package_from_path(result[0])
	return package
	
def load_package_from_repos(packagename, returnpath=False, returnrepo=False):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	if len(result) == 0:
		print(COLOR.RED + "Package not found" + COLOR.RESET)
		exit()
	result=order_array(result)
	package = []
	#package = load_package_from_path(result[0])
	for i in range(len(result)):
		package.append(load_package_from_path(result[i]))
	
	with_problem = True
	while with_problem:
		with_problem = False
		for i in range(len(result)):
			if i != 0:
				if package[i].Version > package[i-1].Version:
					number_temp = package[i-1]
					package[i-1] = package[i]
					package[i] = number_temp

					result_temp = result[i-1]
					result[i-1] = result[i]
					result[i] = result_temp
					with_problem = True

	if returnpath:
		return result[0]
	if returnrepo:
		return os.path.dirname(result[0])

	return package[0]

if __name__ == "__main__":
	main()

#!/usr/bin/python3
import os
import sys
from sys import exit, path
import glob
import subprocess
import requests

# Main Function
def main():
	arch = Arch64()
	check_help()
	create_initial_folders()
	arg_amount=len(sys.argv) #number of args
	
	recommends=False
	suggests=False
	check=True
	
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
						elif "--" not in sys.argv[y]:
							check_internet()
							install_package(sys.argv[y], rec=recommends, sug=suggests)
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
						if "--" not in sys.argv[y]:
							check_internet()
							reinstall_packages(sys.argv[y])
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
						if sys.argv[y] == "-n" or sys.argv[y] == "--no-check":
							check=False
						elif "--" not in sys.argv[y]:
							remove_package(sys.argv[y],check=check)
					else:
						y = i

			elif sys.argv[i] == "update" or sys.argv[i] == "up":
				check_root()
				check_internet()
				update_repos()
				if arg_amount < 3:
					update_all()
				else:
					for y in range(arg_amount):
						if y > i:
							if "--" not in sys.argv[y]:
								check_internet()
								update_package(sys.argv[y])
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
					add_repo(sys.argv[i+1], sys.argv[i+2])
				else:
					print("add-repo <repo-name> <repo-link>")
			elif sys.argv[i] == "remove-repo" or sys.argv[i] == "rmr":
				check_root()
				for y in range(arg_amount):
					if y > i:
						if "--" not in sys.argv[y]:
							remove_repo(sys.argv[y])
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
			print(helptext)
			exit()
		if sys.argv[1] == "--version" or sys.argv[1] == "-v":
			print("v0.1.6")
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
		print("need root")
		exit()

# Create the /etc/idur/
def create_initial_folders():
	if os.path.exists("/etc/idur/") == False:
		if root():
			os.system("mkdir -p /etc/idur/")
			os.system("mkdir -p /etc/idur/repos")
			os.system("mkdir -p /etc/idur/apps")
		else:
			print("You need root")

# Function that remove the package, and then install the package again
def reinstall_packages(packagename):
	remove_package(packagename, check=False)
	install_package(packagename)
	
# install package
def install_package(packagename, sug=False, rec=False):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	if len(result) == 0:
		print("Package not found")
		exit()
	result=order_array(result)
	sys.path.insert(1, os.path.dirname(result[0]))
	
	package = __import__(packagename)
	if packagename == "standard":
		exit()
	
	if Arch64():
		if package.Arch == "all" or package.Arch == "x86_64" or package.Arch == "both":
			pass
		elif package.Arch == "i386":
			exit()
	else:
		if package.Arch == "all" or package.Arch == "i386" or package.Arch == "both":
			pass
		elif package.Arch == "x86_64":
			exit()

	if hasattr(package, 'Conflict'):
		for i in range(len(package.Conflict)):
			if package.Conflict[i] in str(subprocess.check_output(["apt", "list", "--installed", package.Conflict[i]])):
				print(package.Conflict[i] + " is in conflict with " + packagename)
				exit()
			elif os.path.exists("/usr/bin/idur"):
				if package_is_installed(package.Conflict[i]):
					print(package.Conflict[i] + " is in conflict with " + packagename)
					exit()
	
	os.system("cp " + path + " /etc/idur/apps/" + packagename + "-v.py")
	
	if hasattr(package, 'Depends'):
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
						os.system("idur install " + deps[0])
				else:
					to_install=True
					if package_is_installed(package.idurDepends[i]):
							print(package.idurDepends[i] + " is installed")
							to_install=False
					if to_install:
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

# Print the remove instructions
def show_remove_instructions(packagename):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	if len(result) == 0:
		print("Package not found")
		exit()
	sys.path.insert(1, os.path.dirname(result[0]))
	
	package = __import__(packagename)
	if packagename == "standard":
		exit()
	
	if hasattr(package, 'Remove'):
		print(str(package.Remove))
	else:
		print("Error")
		
# Print the install instructions
def show_install_instructions(packagename):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	if len(result) == 0:
		print("Package not found")
		exit()
	sys.path.insert(1, os.path.dirname(result[0]))
	
	package = __import__(packagename)
	if packagename == "standard":
		exit()
		
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
	
# Function that print the principal features of the package, like Name, Version, Description, Architecture, etc.
def show_package_details(packagename):
	path='/etc/idur/repos/*/' + packagename + '.py'
	result=glob.glob(path, recursive=True)
	if len(result) == 0:
		print("Package not found")
		exit()
	
	print("Repo: " + result[0][16:len(result[0])][:-1*(len(packagename)+4)])
	
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

# Return True if the package that you want remove, it's a depends of another package
def is_idurDepends_of_installed_packages(idurDepend):
	finded=False
	path='/etc/idur/apps/*-v.py'
	result=glob.glob(path, recursive=True)
	for i in range(len(result)):
		sys.path.insert(1, "/etc/idur/apps")
		name=os.path.basename(result[i])
		size = len(name)
		name = name[:size - 3]
		package = __import__(name)
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
def remove_package(packagename, check=True):
	sys.path.insert(1, "/etc/idur/apps")
	
	if os.path.exists("/etc/idur/apps/" + packagename + "-v.py") == False:
		print("you don't have installed " + packagename)
		exit()
	
	if check:
		if is_idurDepends_of_installed_packages(packagename):
			exit()

	package = __import__(packagename + "-v")
	if packagename == "standard":
		exit()
	os.system("bash -c \"" + package.Remove + "\"")
	os.system("rm -vrf /etc/idur/apps/" + packagename + "-v.py")

# Return True if the package is in /etc/idur/apps/
def package_is_installed(packagename):
	
	if os.path.exists("/etc/idur/apps/" + packagename + "-v.py"):
		return True
	else:
		return False

# Function to update the package specified
# idur update <name>
def update_package(packagename):
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
			remove_package(packagename, check=False)
			install_package(packagename)
	else:
		print("you don't have installed " + packagename)
	
# Function that update all the packages (if it need update) and repositories that you have
def update_all():
	path='/etc/idur/apps/*-v.py'
	result=glob.glob(path, recursive=True)
	for i in range(len(result)):
		name=os.path.basename(result[i])
		size = len(name)
		name = name[:size - 5]
		update_package(name)

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
def remove_repo(name):
	path='/etc/idur/repos/' + name + '/standard.py'
	if os.path.exists(path):
		size=len(path)
		path = path[:size - 11]
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
def add_repo(name, link):
	if os.path.exists("/etc/idur/repos/" + name) == False:
		os.system("""
		cd /etc/idur/repos/
		git clone """ + link + " " + name)

# Function that update the repositories
# git pull in /etc/idur/repos/*/
#
# idur update-repos
def update_repos():
	result=glob.glob('/etc/idur/repos/*/standard.py', recursive=True)
	for i in range(len(result)):
		os.system("cd " + os.path.dirname(result[i]) + " && git pull")

# Print the Description of the path_input
def print_description_of_path(path_input):
	sys.path.insert(1, os.path.dirname(path_input))
	packagename = os.path.basename(path_input)
	packagename = packagename[:len(packagename) - 3]
	package = __import__(packagename)
	
	description = package.Description.replace('\n', ' ')
	
	print("- " + description[0:50] + "...")

# Return True if the searchword is in the Description of path_input
def search_on_description(path_input, searchword):
	sys.path.insert(1, os.path.dirname(path_input))
	packagename = os.path.basename(path_input)
	packagename = packagename[:len(packagename) - 3]
	if packagename != "__pycach" and packagename != "standard":
		package = __import__(packagename)
	
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
		print("\nDescription Search\n")
		dpath="/etc/idur/repos/*/*"
		dresult=glob.glob(dpath, recursive=True)
		dresult=order_array(dresult)
		for j in range(len(dresult)):
			result_out = os.path.basename(dresult[j])
			result_out = result_out[:len(result_out) - 3]
			if result_out != "standard" or result_out != "__pycach":
				if search_on_description(dresult[j], packagename):
					print(result_out)
					print_description_of_path(dresult[j])
	
	# Name Search
	print("\nName Search\n")
	for i in range(len(result)):
		result_out=os.path.basename(result[i])
		result_out = result_out[:len(result_out) - 3]
		if result_out != "standard":
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
		print("Connected to the Internet")
	else:
		print("No internet connection.")
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
			print(result_out)

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

if __name__ == "__main__":
	main()

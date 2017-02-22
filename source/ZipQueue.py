import os
while True:
	if not os.path.isfile("7za.exe"):
	    input("7za.exe not found in working directory")
	else:
		break
from subprocess import call
from timeit import default_timer as timer
import ctypes

def cmdtitle(strIn):
    ctypes.windll.kernel32.SetConsoleTitleW(strIn)

def echolist(message, listIn):
    print("\n%s:\n----------------\n" % message)
    for i in range(len(listIn)):
        print("{0} - {1}".format(i+1, listIn[i]))

def get_intrang(prompt, rang):
    while True:
        try:
            num = int(input(prompt))
            if num in range(1, rang + 1):
            	return num
        except ValueError:
            pass

def pathsize(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

version = "1.0.0"
builddate = "2/22/2017"
cmdtitle("Zip Queue %s" % version)
print(
	"      ___                       ___                                ___           ___           ___           ___ ",
	"     /\__\                     /\  \                              /\  \         /\__\         /\  \         /\__\ ",
	"    /::|  |       ___         /::\  \                ___          \:\  \       /:/ _/_        \:\  \       /:/ _/_ ",
	"   /:/:|  |      /\__\       /:/\:\__\              /\  \          \:\  \     /:/ /\__\        \:\  \     /:/ /\__\ ",
	"  /:/|:|  |__   /:/__/      /:/ /:/  /             /::\  \     ___  \:\  \   /:/ /:/ _/_   ___  \:\  \   /:/ /:/ _/_ ",
	" /:/ |:| /\__\ /::\  \     /:/_/:/  /             /:/\:\  \   /\  \  \:\__\ /:/_/:/ /\__\ /\  \  \:\__\ /:/_/:/ /\__\ ",
	" \/__|:|/:/  / \/\:\  \__  \:\/:/  /             /:/ /::\  \  \:\  \ /:/  / \:\/:/ /:/  / \:\  \ /:/  / \:\/:/ /:/  / ",
	"     |:/:/  /     \:\/\__\  \::/__/             /:/_/:/\:\__\  \:\  /:/  /   \::/_/:/  /   \:\  /:/  /   \::/_/:/  / ",
	"     |::/  /       \::/  /   \:\  \             \:\/:/  \/__/   \:\/:/  /     \:\/:/  /     \:\/:/  /     \:\/:/  / ",
	"     |:/  /        /:/  /     \:\__\             \::/  /         \::/  /       \::/  /       \::/  /       \::/  / ",
	"     |/__/         \/__/       \/__/              \/__/           \/__/         \/__/         \/__/         \/__/ ",
    "verison %s     %s" % (version, builddate), "written by pixelpython", sep="\n")

while True:
	pathlist = []
	namelist = []
	ratiolist = []
	echolist("7-Zip Action", ["Archive", "Extract"])
	actIn = get_intrang("Action?  ", 2)
	if actIn == 1:
		# archive
		while True:
			if len(pathlist) == 0:
				pathapp = input("Directory to compress:  ")
			else:
				pathapp = input("Directory to compress [q] quit [v] view [r] remove:  ")
			if pathapp in ["q", "v", "r"] and len(pathlist) != 0:
				if pathapp.lower() == "q":
					break
				elif pathapp.lower() == "v" or pathapp.lower() == "r":
					for i in range(len(pathlist)):
						print("{0} - {1}".format(i+1, pathlist[i]))
						if pathapp.lower() == "r":
								remove = get_intrang("Path to remove:  ", len(pathlist)) - 1
								del pathlist[remove]
								del namelist[remove]
			elif os.path.isdir(pathapp):
				pathlist.append(pathapp)
				namelist.append(input("Output file name: "))
			else:
				print("Path not found.")
		start = timer()
		for i in range(len(pathlist)):
			filetime = timer()
			call('7za a -mx9 "{0}" "{1}"'.format(namelist[i], pathlist[i]))
			print("File compressed in %ss" % round((timer() - filetime), 3))
			ratiolist.append("{:.0%}".format(os.path.getsize("%s.7z" % namelist[i])/pathsize(pathlist[i])))
		for i in range(len(namelist)):
			print("{0}.7z ratio is {1}".format(namelist[i], ratiolist[i]))
		print("Queue completed in %ss" % round((timer() - start), 3))
	elif actIn == 2:
		# extract
		while True:
			if len(pathlist) == 0:
				pathapp = input("Files to decompress:  ")
			else:
				pathapp = input("Files to decompress (q to quit):  ")
			if pathapp.lower() == "q" and len(pathlist) != 0:
				break
			elif os.path.isfile(pathapp):
				pathlist.append(pathapp)
			else:
				print("File not found.")
		start = timer()
		for zpath in pathlist:
			filetime = timer()
			call('7za x "%s"' % zpath)
			print("Completed in %s s" % round((timer() - filetime), 3))
		print("Queue completed in %ss" % round((timer() - start), 3))
	else:
		pass
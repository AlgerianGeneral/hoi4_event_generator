#!/usr/bin/python
#import configparser as conf
from termcolor import colored
import os

#Detect OS
if os.name == "nt":
	OS = "Win"
else:
	OS = "Unix"

class event:
	def __init__(self, eType, eid, options, t = "Unnamed Event", desc = "Placeholder", pic = "GFX_placeholder", optionText = [], optionEffects = [], otherProperties = ""):
		self.eType = eType
		self.eid = eid 
		self.t = t
		self.desc = desc
		self.pic = pic
		if pic == "": self.pic = "GFX_report_event_german_speech"
		self.options = options
		self.optionText = optionText
		if type(optionEffects) is list:
			self.optionEffects = optionEffects
		else: self.optionEffects = ""
		if self.eType == 1:
			self.eType = "country_event"
			self.otherProperties = otherProperties
		else:
			self.eType = "news_event"
			self.otherProperties = "\nmajor = yes\n" + otherProperties


	def generateLocalisation(self):
		numOpt = len(self.optionText)
		localisation = []
		
		localisation.append(self.t)
		self.t = (self.eid + ".t")

		localisation.append(self.desc)
		self.desc = (self.eid + ".d")

		num = 0
		while(num < numOpt):
			localisation.append(self.optionText[num])
			alpha = ["a", "b", "c", "d", "e", "f"]
			self.optionText[num] = self.eid + "." + alpha[num]
			num += 1

		localisation[0] = self.t + ":0 \"" + localisation[0] + "\""
		localisation[1] = self.desc + ":0 \"" + localisation[1] + "\""
		x = 0
		while(x < numOpt):
			localisation[2 + x] = self.optionText[x] + ":0 \"" + localisation[ 2 + x] + "\""
			x += 1

		return localisation

	def generateCode(self):
		

		code1 = """{} = {{ #Generated by HOI4 event generator written by Murphy
	id = {}
   	title = {}
   	desc = {}
   	picture = {}

   	{}

	""".format(self.eType, self.eid, self.t, self.desc, self.pic, self.otherProperties)
		code2 = ""
		a = 0
		for x in self.optionText:
			code2 += """option = {{
	name = {}

	{}

	}}\n""".format(x, self.optionEffects[a])
			a += 1

		return code1 + code2 + "\n}"


#class settings():
	#def load_settings:
		#conf.RawConfigParser()
######
def clear():
	if OS == "Win":
		os.system("cls")
	else:
		os.system("clear")

def invalidOpt():
	print colored("[-] Invalid option. try again.\n", "red")


validatePathErrCodes = {-1: "Potential Error: dot in path but maybe not a file extension.", -2: "Missing file extension."}
def validatePath(path, localisation = False):
	if path == "": return 1
	if "/" in path or "\\" in path: #Windows paths as well
		if ".txt" in path or ".yml" in path: return 0 #definetly has a file extension
		if "." in path: return -1 #might have a file extension
		if not "." in path: return -2
	elif not "/" in path:
		if ".txt" in path or ".yml" in path: return 0
		if "." in path: return -1
		if not "." in path: return -2

def validateField(text, func, wordlist = None, obligatory = False, blacklist = None):
	result = None
 	while True:
		try:
			result = raw_input(text)
			if not blacklist == None:
				if result in blacklist:
					print "Not allowed the following: ", blacklist
					continue
			if obligatory == True and result == "":
				print "Cannot leave this field empty."
				continue
			if not wordlist == None:
				if not result in wordlist:
					print "Invalid entry. Try again."
					continue
			result = func(result)
		except ValueError:
			print "Invalid entry. Try again."
			continue
		break
	return result

def createEvent():
	clear()
	print "All fields with an * are required. Leave others empty at will.\n"
	eType = validateField("Enter event type (1 for normal and 0 for news)*: ", int, obligatory = True, wordlist = ["0", "1"])
	eid = validateField("Enter event ID (Be careful! Anything in the form of 'xyz.1' requires 'add_namespace = xyz' at the top the file)*: ", str, obligatory = True)
	t = validateField("Enter event title: ", str)
	desc = validateField("Enter event description:\n", str)
	pic = validateField("Enter picture path (example: GFX_example_pic): ", str)
	options = validateField("Enter options (at least one required)*: ", int, obligatory = True, blacklist = "0")

	x = 0
	optionText = None
	optionEffects = None

	while (x < options):
		if x == 0:
		 	opt = []
		 	optEff = []
		opt.append(validateField("Enter option {} title(leave empty for default):".format(x + 1), str))
		if eType == 1: optEff.append(validateField("Enter option {} effects(leave empty for no effects):".format(x + 1), str))
		optionText = opt
		if not optEff == "": optionEffects = optEff
		x += 1


	addProp = validateField("Would you like to add any additional properties [y/n]?", str, wordlist = ["y", "Y", "n", "N"])
	otherProperties = ""

	if addProp == "y" or addProp == "Y":
		print "Enter each property one at a time. To finish, enter ", colored("0", "red"),"or", colored("q", "red")
		while True:
			i = raw_input("Enter property: ")
			if i == "0" or i == "q": break
			otherProperties += (i + "\n")

	return event(eType, eid, options, t = t, desc = desc, pic = pic, optionText = optionText, optionEffects = optionEffects, otherProperties = otherProperties)

###############################Here comes the meat###############################

clear()
with open("logo.txt") as file:
	logo = file.read(1024) #1024 is to avoid someone addding loads of shit and thus causing the program to run out of memory
	print colored(logo, "green") , "\n\n\n"

print "Welcome to Event Generator for Hearts of Iron IV written by Murphy\n"

while True:
	try:
		print "Select an option from below:\n\n    [", colored("1", "red"), "] Create an event\n    [", colored("2", "red"), "] Exit"
		opt = input("\nOption: ")

		if opt == 2: break

		if opt == 1:
			clear()
			while True:
				print "Select where you would like to output the code:\n\n    [", colored("1", "red"), "] Output to file\n    [", colored("2", "red"), "] Print to screen\n    [", colored("c", "red"), "] Cancel"
				opt = input("\nOption: ")

				if opt == 1:
					while True:
						path = raw_input("\nEnter event file path (leave emtpy for default): ")
						isValid = validatePath(path)
						if isValid == 0 or isValid == 1: break
						if isValid == -1:
							print validatePathErrCodes[-1]
							print "Path you entered: ", path
							a = raw_input("Is this path correct [y/n]?")
							if a == "y" or a == "Y": break
						if isValid == -2: print validatePathErrCodes[-2]
					
					while True:
						localPath = raw_input("\nEnter localisation file path (leave emtpy for default): ")
						isValid = validatePath(localPath)
						if isValid == 0 or isValid == 1: break
						if isValid == -1:
							print validatePathErrCodes[-1]
							print "Path you entered: ", localPath
							a = raw_input("Is this path correct [y/n]?")
							if a == "y" or a == "Y": break
						if isValid == -2: print validatePathErrCodes[-2]
						#ErrCode 1 is default path
					
					#TODO: Need to create a proper system for default files
					clear()

					e = createEvent()
					localisation = e.generateLocalisation() #it's important that localisation gets called first
					code = e.generateCode()

					with open(path, "a") as eCode:
						eCode.write(code)
						print "Wrote to event file"

					with open(localPath, "a") as local:
						for i in localisation:
							local.write(i + "\n")
						print "Wrote to localisation file"

					Placeholder = input("\nEnter anything to continue: ")
					continue

				elif opt == 2:
					#do something
					e = createEvent()
					localisation = e.generateLocalisation() #it's important that localisation gets called first
					code = e.generateCode()

					clear()
					print "Printing Event Code: \n"
					print code
					print "\nPrinting localisation: \n"
					print localisation
					Placeholder = input("\nEnter anything to continue: ")
					continue
				else:
					invalidOpt()
		else:
			clear()
			invalidOpt()

	except SyntaxError:
		invalidOpt()
		continue

#Exit message
print "Quitting...."
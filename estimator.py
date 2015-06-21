#!/usr/bin/python

import re
import sys

# Estimate the length of filament required for a given gcode file
def estimateFilament (filename):
	total_mm = 0
	running_total = 0

	absolute = True

	#Try to open the file
	try:
		gcode_file = open(filename, 'r')
	except: #Handle the error nicely if the file cannot be opened.
		return "File Not Found"
	
	# read the gcode file line by line
	for line in gcode_file:
		if ("G92 " in line): 
			#The E value will be reset here so add the running total
			#length to the total length and reset the running length.
			total_mm += float(running_total)
			running_total = 0
		
		elif ("G91 " in line):
			#E values will now be relative and not absolute
			absolute = False	
			total_mm += float(running_total) # add the running length and then reset it to 0
			running_total = 0
		
		elif ("G90 " in line):
			#E values will now be absolute
			absolute = True
		
		elif ("G1 " in line):
			#get the E values. Examples: E-1, E25, E0.535 will all be matched
			results = re.search("E(-?\d+(\.\d+)?)", line) # This will find E values that are negative and optionally have decimals
			if (results != None):
				if (absolute):
					#If the E values are absolute, we just want to find the last one
					#so update the running total
					running_total = results.group(1)
				else:
					#If the E values are relative, then their values should be added or 
					#subtracted from the total length so far.
					total_mm += float(results.group(1))

	#add and lengths that haven't already been added
	total_mm += float(running_total)

	gcode_file.close()
	return round(total_mm, 1) # return the length in mm to one decimal point

def main(args):
	
	toString = "----------\nEstimated length of filament for: \n"
	
	#find the length of each file individually and make its output nice.
	for filename in args:
		length = estimateFilament(filename)
		toString = toString + filename +  " --> " + str(length) + " mm\n"
	
	toString = toString + "----------"
	return toString

if (len(sys.argv) == 1):
	print "Please provide at least one gcode file as an argument."
	print "Multiple gcode files can be processed at once. Provide each file as a separate argument"
	print "\n\tExample: python estimator.py Sample1.gcode Sample2.gcode"
	print "\nThis will process both Sample1.gcode and Sample2.gcode"
else:
	#We assume that all arguments are gcode files. 
	#The first arg in the argv array will always be the script name, so we
	#don't want it to be parsed.
	print main(sys.argv[1:])


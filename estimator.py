#!/usr/bin/python

import re
import sys

def estimateFilament (filename):
	#filename = '3mmBox.gcode'

	gcode_file = open(filename, 'r')

	total_mm = 0
	running_total = 0

	for line in gcode_file:
		#line = gcode_file.readline()
		if ("G92 " in line):
			total_mm += float(running_total)
			
		elif ("G1 " in line):
			results = re.search("E(\d+\.\d+)", line)
			if (results != None):
				running_total = results.group(1)

	total_mm += float(running_total)

	gcode_file.close()
	return round(total_mm)

def main(args):
	toString = "----------\nEstimated length of filament for: \n"
	for filename in args:
		length = estimateFilament(filename)
		toString = toString + filename +  " --> " + str(length) + " mm\n"
	toString = toString + "----------"
	return toString

print main(sys.argv[1:])

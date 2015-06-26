#!/usr/bin/python

import re
import sys

def estimateFilament (filename):
	gcode_file = open(filename, 'r')

	total_mm = 0
	running_total = 0

	absolute = True

	for line in gcode_file:
		#line = gcode_file.readline()
		if ("G92 " in line):
			total_mm += float(running_total)
			#print "total",total_mm
			running_total = 0
		
		elif ("G91 " in line):
			absolute = False	
			total_mm += float(running_total)
			running_total = 0
		
		elif ("G90 " in line):
			absolute = True
		
		elif ("G1 " in line):
			results = re.search("E(-?\d+(\.\d+)?)", line)
			#results = re.search("E(\d+\.\d+)", line)
			if (results != None):
				if (absolute):
					running_total = results.group(1)
					#print running_total
				else:
					total_mm += float(results.group(1))

	#print running_total
	total_mm += float(running_total)

	gcode_file.close()
	return round(total_mm, 1)

def main(args):
	toString = "----------\nEstimated length of filament for: \n"
	for filename in args:
		length = estimateFilament(filename)
		volume = 3.14*0.0875*0.0875*(length/10)
		weight = volume * 1.3
		cost = (3*weight)/100
		cost = round(cost, 2)
		print volume, weight, cost
		toString = toString + filename +  " --> " + str(length) + " mm, cost: $" + str(cost) + "\n"
	toString = toString + "----------"
	return toString

print main(sys.argv[1:])

#!/usr/bin/python

import optparse
import re
import os

# argument exon inutile car featurecount peut choisir la feature qui l interresse mais bon on va pas modifier proqseq plus que ca

def main():
	parser=optparse.OptionParser()
	parser.add_option("-i", "--input", type="string", dest="file")
	parser.add_option("-o", "--output", type="string", dest="dest")
	(options, args)= parser.parse_args()
	run(options.file, options.dest)
	
	
def run(inpfile, dest):
	with open(inpfile, "r") as infile:
		with open(dest, "w") as outfile:
			listt=[]
			for li in infile:
				li=li.rstrip()
				nwli=""
				listt=li.split("\t")
				for i in range(0, len(listt)-1):
					nwli+=listt[i]+"\t"
				idfeat=listt[i+1].split(";")[0].split('"')[1]
				#exit(idfeat)
				nwli+="ID="+idfeat+"\n"
				outfile.write(nwli)
	print("coucou")

if __name__ == '__main__':
		  main()

#!/usr/bin/python

import optparse
import re
import os

# argument exon inutile car featurecount peut choisir la feature qui l interresse mais bon on va pas modifier proqseq plus que ca

def main():
	parser=optparse.OptionParser()
	parser.add_option("-i", "--input", type="string", dest="file")
	parser.add_option("-o", "--output", type="string", dest="dest")
	parser.add_option("-f","--format", type="string", dest="format", help="format of output: GO, gtf, bed")
	parser.add_option("-e", "--exon", action="store_true", dest="exon", default=False)
	(options, args)= parser.parse_args()
	run(options.file, options.dest, options.format, options.exon)
	
def run(inpfile, dest, Fformat, exon=False):
	#print("\n\n\n",Fformat,"\n")
	if Fformat=="GO":
		directory=os.path.dirname(dest)
		regirock=re.compile(r"ID=(?P<id>[^;]*)")
		regice=re.compile(r"GO:\d{7}")
		registeel=re.compile(r"Name=(?P<name>[^;]*)")
		gofile2=open(directory+"TERM2GENE.csv","w")
		gofile2.write("TERM,GENE\n")
	#print(dest)
	with open(inpfile, "r") as infile:
		with open(dest, "w") as outfile:
			
			listt=[]
			for li in infile:
				#print(len(li))
				
				if li[0]==">" or li[0]=="\n":
					break
				if li[0]!="#":
					li=li.rstrip()
					nwli=""
					listt=li.split("\t")
					if exon:
						listt[2]="exon"
					if Fformat=="GO":
						ice=regice.findall(listt[-1])
						rock=regirock.match(listt[-1])
						name=registeel.search(listt[-1]).group("name")
						if rock is not None:
							id=rock.group("id")
						elif listt[6]=="-":
							id= listt[0].split("_")[0] + "_" + listt[3] + "_" + listt[4] + "negaStrd"
#							print(id)
						else:
							id= listt[0].split("_")[0] + "_" + listt[3] + "_" + listt[4] + "posiStrd"
						
						if ice!=[]:
							for i in ice:
								gofile2.write(i+","+id+"\n")
								outfile.write(i+","+name+"\n")
							
					elif Fformat=="gtf":
						for i in range(0,len(listt)-1):
							nwli+=listt[i]+"\t"
						if listt[i+1].split(';')[0].split('=')[0] =="ID":
							id=listt[i+1].split(';')[0].split('=')[1]
						elif listt[6]=="-":
							id= listt[0].split("_")[0] + "_" + listt[3] + "_" + listt[4] + "negaStrd"
						else:
							id= listt[0].split("_")[0] + "_" + listt[3] + "_" + listt[4] + "posiStrd"
						nwli+="gene_id \"" + id + "\"; transcript_id \"TR:" + id + "\"\n"
						outfile.write(nwli)
						
						
					elif Fformat=="bed":
						if listt[8].split(';')[0].split('=')[0] =="ID":
							id=listt[8].split(';')[0].split('=')[1]
						elif listt[6]=="-":
							id= listt[0].split("_")[0] + "_" + listt[3] + "_" + listt[4] + "negaStrd"
						else:
							id= listt[0].split("_")[0] + "_" + listt[3] + "_" + listt[4] + "posiStrd"
						nwli= listt[0] +"\t"+ listt[3] +"\t"+ listt[4] +"\t"+ id +"\t0\t"+ listt[6] +"\t"+ listt[3] +"\t"+ listt[4] +"\t0,255,0\t1\t"+ str(int(listt[4])-int(listt[3])) + ",\t0,\n"
						outfile.write(nwli)
						
	if Fformat=="GO":	
		gofile2.close()
		return dest, directory+"TERM2GENE.csv"
	return dest

if __name__ == '__main__':
		  main()

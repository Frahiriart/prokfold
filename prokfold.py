#!/usr/bin/python

import os
import argparse
import sys
import yaml
import re
import pickle as pic
import pandas as pd
from copy import deepcopy as dcp
from script import reads as fqc
from script import execute as exe
from script import bowtie as bwt
from script import biotools as bt
from script import gff2gtf as fc
from script import edge as edg


def run():

	parser = argparse.ArgumentParser(description="",
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-c', '--config', dest="config",
					help="Enter the path to the file which contain the configuration of all program.\n\n")
	parser.add_argument('-o', '--output', dest="repResult", default='./',
					help="Enter the name of the file where the result will be store."
					"\nDefault: -o ./\n\n")
	parser.add_argument('-p', '--processor', dest="cpu", default=4, type=int,
					help="""Enter the number of CPU that the pipeline will use.\nDefault: -p 4\n\n""")
	parser.add_argument('-a', '--account', dest="count", default="f",
					help="Choose the method to count feature between feature count (fc) or fadu (f)."
					"\nDefault: -a f\n\n")
	parser.add_argument('-f', '--freeload', dest="free", default=1, type=int,
					help="Level of storage of data produce by intermediate programm.\n"
					"You can choose between [0,1,2], default: -f 1\n"
					"\tLevel 0: data from afterqc and SAM file from bowtie2 are delete\n"
					"\tLevel 1: SAM file from bowtie2 are delete but can be recover with bam file\n"
					"\tLevel 2: No intermediate data are delete\n\n")
	
	#Verification of arguments
	args=parser.parse_args()
	if not os.path.exists(args.config):
		sys.exit("Your path of configuation file don't exists or we haven't the permission.\n")
	
	
	selfDir = os.path.dirname(os.path.abspath(__file__))
	result=args.repResult.split("/")
	if os.path.exists(args.repResult) is False:
		os.makedirs(args.repResult)
	if os.path.exists(args.repResult+"/fastqc/beforeTrim") is False:
		os.makedirs(args.repResult+"/fastqc/beforeTrim")
	if os.path.exists(args.repResult+"/fastqc/afterTrim") is False:
		os.makedirs(args.repResult+"/fastqc/afterTrim")
	if os.path.exists(args.repResult+"/afterqc") is False:
		os.makedirs(args.repResult+"/afterqc")
	if os.path.exists(args.repResult+"/genome/index") is False:
		os.makedirs(args.repResult+"/genome/index")
	if os.path.exists(args.repResult+"/BowAlignement") is False:
		os.makedirs(args.repResult+"/BowAlignement")
	if os.path.exists(args.repResult+"/coverage") is False:
		os.makedirs(args.repResult+"/coverage")
	if os.path.exists(args.repResult+"/featureCounts") is False and args.count=="fc":
		os.makedirs(args.repResult+"/featureCounts")
	if os.path.exists(args.repResult+"/edgeResult/js") is False:
		os.makedirs(args.repResult+"/edgeResult/js")
	if os.path.exists(args.repResult+"/fadu") is False and args.count=="f":
		os.makedirs(args.repResult+"/fadu/joinCounts")
	args.repResult=os.path.abspath(args.repResult)
	
	args.config=os.path.abspath(args.config)
	bivar=selfDir+"/script/bivar.bin"


	data=extract_param2(args.config, bivar)
	if data["reads"]["cp"][-1] != "/":
		data["reads"]["cp"]+="/"
	for i in data["reads"]["sa"]:
		for j in data["reads"]["sa"][i].values():
			for k in j:
				k=data["reads"]["cp"]+k
				if os.path.exists(k) is False:
					print("We didn't found the file:", k)
					exit()



	chrSizeFile, genomeFile=bt.chromosome_sizes(data["genome"]["fna"], args.repResult+"/genome")
	if genomeFile:
		data["genome"]["fna"]=genomeFile
	
	Fgff2=os.path.splitext(os.path.basename(data["genome"]["gff"]))[0]
	data["genome"]["gtf"]=fc.run(data["genome"]["gff"],
		args.repResult+"/genome/"+Fgff2+".gtf", "gtf", )
	
	run_fastqc(data["reads"]["sa"], data["reads"]["cp"], selfDir+"/depend/FastQC/fastqc",
		args.repResult+"/fastqc/beforeTrim", args.cpu)
	
	transcript = run_afterqc(data["reads"]["sa"], data["reads"]["cp"],
		selfDir+"/depend/pypy2.7-v7.3.5-linux64/bin/pypy",
		selfDir+"/depend/AfterQC-master/after.py", args.repResult+"/afterqc",
		args.cpu, data["afterqc"])
		
	run_fastqc(dcp(transcript), "", selfDir+"/depend/FastQC/fastqc",
		args.repResult+"/fastqc/afterTrim", args.cpu)

	Findex=run_bowtie_index(data["genome"]["fna"], args.repResult+"/genome/index",
		selfDir+"/depend/bowtie2-2.4.4-linux-x86_64/bowtie2-build")
	
	transcript=run_bowtie(Findex, dcp(transcript),
		selfDir+"/depend/bowtie2-2.4.4-linux-x86_64/bowtie2",
		args.repResult+"/BowAlignement", data["bowtie"], args.cpu, args.free)
	
	transcript=sam2indexbam(dcp(transcript), selfDir+"/depend/samtools-1.12/samtools", args.cpu, args.free)
	
	deeptools(dcp(transcript), chrSizeFile, data["deeptools"],
		selfDir+"/depend/deepTools-3.5.1/bin",	args.repResult+"/coverage", args.cpu)
	
	#Choose Count method
	if args.count=='fc':
		rawCount = featureCounts(dcp(transcript), data["genome"]["gtf"],
			selfDir+"/depend/subread-2.0.2-Linux-x86_64/bin",
			args.repResult+"/featureCounts", data["reads"]["se"], data["featCount"], cpu=args.cpu)
	elif args.count=="f":
		rawCount = fadu(selfDir+"/depend/FADU/", args.repResult+"/fadu",
			dcp(transcript), data["genome"]["gff"], data["fadu"], cpu=args.cpu)
	
	Nsample=0
	for i in transcript:
		Nsample+=len(transcript[i])

	edger(selfDir+"/script/edgeR.R", selfDir+"/script/js",
		rawCount, Nsample, args.repResult+"/edgeResult", data["edger"])
	
	if genomeFile:
		genomeFile="rm "+ genomeFile
		#os.system(genomeFile)




def extract_param2(conf, bivar):

#################	Extract parameter from the config file		#################

	print("\n\n"+"-"*20+" EXTRACTION OF PARAMATER IN THE CONFIGURATION FILE: "+"-"*20+"\n")

	param={}
	binfile=open(bivar,"rb")
	dicreg=pic.load(binfile)
	emptyli=re.compile("^\s*$")
	commentli=re.compile("^\s*#")
	splinter=re.compile(",\s*")
	
	for i in dicreg["LparamGroup"]:
		param[i]={}
	param["reads"]["sa"]={}
	
	dicreg=dicreg["Dregex"]
	
	compt=0
	with open(conf) as f:
		for lifull in f:
			li=lifull.rstrip()
			li=li.split("#")[0]
			compt+=1
			
			if emptyli.match(li) is not None:
				continue
			
			for i in dicreg:
				for j in dicreg[i]:
					for k in dicreg[i][j]:
						match=dicreg[i][j][k].match(li)
						if match is not None:
							if i=="num":
								param[j][k]=int(match.group(1))
							
							elif i=="path":
								param[j][k]=match.group(1)
								if not os.path.exists(param[j][k]):
									print("The path", param[j][k], "do not exist or we have not the permission (type preferably the path from the root to your file)")
									exit()
							
							elif i=="list":
								param[j][k]=splinter.split(match.group(1))
							
							elif i=="troolean":
								if match.group(1).lower()=="true":
									param[j][k]=1
								elif match.group(1).lower()=="false":
									param[j][k]=0
								else:
									param[j][k]=2
							
							elif i=="boolean":
								if match.group(1).lower()=="true":
									param[j][k]=True
								elif match.group(1).lower()=="false":
									param[j][k]=False
							
							elif i=="sample":
								if match.group(2) not in param[j][k]:
									param[j][k][match.group(2)]={}
								if match.group(4)=="":
									param[j][k][match.group(2)][match.gbowtie_broup(1)]=[match.group(3)]
								else:
									param[j][k][match.group(2)][match.group(1)]=[match.group(3), match.group(4)]
							elif i=="Bnum":
								if match.group(1).lower()=="none":
									param[j][k]=None
								else:
									param[j][k]=int(match.group(1))
									
							else:
								param[j][k]=match.group(1)
							break
					else:
						continue
					break
				else:
					continue
				break
			else:
				print("Error in the file", conf,":\n\tline",str(compt)+":"+lifull)
				exit()
	return param




def run_fastqc(transcript, commonPath, repFastqc, repResult="result/fastqc", cpu=4):

###########################	Running fastqc for all sample		###########################
	
	print("\n\n"+"-"*20+" READS QUALITY CONTROL WITH FASTQC "+"-"*20+"\n")	
	
	cmds=[]
	for i in transcript:
		for j in transcript[i]:
			cmd=fqc.fastqc(commonPath+transcript[i][j][0], repResult, repFastqc)
			if len(transcript[i][j])==2:
				cmds.append(cmd)
				cmd=fqc.fastqc(commonPath+transcript[i][j][1], repResult, repFastqc)
			cmds.append(cmd)
	exe.threading_run(cmds, "fastqc", cpu)




def run_afterqc(transcript, commonPath, repPypy, repAfterqc, repResult="result/afterqc", cpu=4,
	p={'-f': '-1', '-t': '-1', '-q': '15', '-p': '35', '-a': '2', '-n': '3', '-s': '35'}):

###########################	Running afterqc		###########################

	print("\n\n"+"-"*20+" READS FILTERING WITH AFTERQC "+"-"*20+"\n")
	
	cmds = []
	for i in transcript:
		for j in transcript[i]:
			cmd=''
			pe=False
			if len(transcript[i][j])==1:
				cmd = fqc.afterqc(repResult, commonPath+transcript[i][j][0], fq2=None,
					f=p["-f"], t=p["-t"], q=p["-q"], p=p["-p"], a=p["-a"], n=p["-n"], s=p["-s"],
					pypy_bin=repPypy, afterqc_bin=repAfterqc)
				# Update fastq file for downstream analysis
				transcript[i][j] = [os.path.join(repResult, 'good_reads',
					os.path.splitext(os.path.basename(transcript[i][j][0]))[0]+'.good.fq')]
			else:
				cmd = fqc.afterqc(repResult, commonPath+transcript[i][j][0],
					commonPath+transcript[i][j][1],
					f=p["-f"], t=p["-t"], q=p["-q"], p=p["-p"], a=p["-a"], n=p["-n"], s=p["-s"],
					pypy_bin=repPypy, afterqc_bin=repAfterqc)
				# Update fastq file for downstream analysis
				transcript[i][j] = [os.path.join(repResult, 'good_reads',
					os.path.splitext(os.path.basename(transcript[i][j][0]))[0]+'.good.fq'),
					os.path.join(repResult, 'good_reads',
					os.path.splitext(os.path.basename(transcript[i][j][1]))[0]+'.good.fq')]				
				#print(cmd)
			cmds.append(cmd)


	exe.threading_run(cmds, 'afterqc', cpu)
	return transcript




def run_bowtie_index(genome, output, repBwtBuild, index=None):

###########################	Indexing the reference genome		###########################
	
	print("\n\n"+"-"*20+" INDEXING THE REFERENCE GENOME "+"-"*20+"\n")
	
	name=genome.split("/")[-1].split(".fna")
	if len(name)==1:
		output+="/"+"".join(name)
	else:
		output+="/"+"".join(name[:-1])

	cmd=bwt.index(genome, output, repBwtBuild)
	print(cmd,"\n")
	os.system(cmd)
	return output
	


	
def run_bowtie(index, transcript, repbwt, repResult="result/BowAlignement", p={}, cpu=4, free=1):

###########################	Alignement with Bowtie2		###########################
	
	print("\n\n"+"-"*20+" ALIGNEMENT WITH BOWTIE2 "+"-"*20+"\n")
	
	cpu=int(cpu/p["-p"])
	cmds=[]
	for i in transcript:
#		print(i)
		for j in transcript[i]:
#			print("\t",j,transcript[i][j])
			output=repResult+"/"+j+".sam"
			if len(transcript[i][j])==1:
				cmd=bwt.bowtie2(output, index, transcript[i][j][0], bowbin=repbwt,
					k=p["-k"], p=p["-p"], free=free)
			else:
				cmd=bwt.bowtie2(output, index, transcript[i][j][0], transcript[i][j][1],
					bowbin=repbwt, k=p["-k"], p=p["-p"], free=free)
			cmds.append(cmd)
			transcript[i][j]=output
	exe.threading_run(cmds, 'bowtie', cpu)
	return transcript



def sam2indexbam(transcript, repsam, cpu=4, free=1):

#################    Sorting and indexing of alignements with Samtools    #################

	print("\n\n"+"-"*20+" SORTING AND INDEXING OF ALIGNEMENT WITH SAMTOOLS "+"-"*20+"\n")

	cmds=[]
	for i in transcript:
		for j in transcript[i]:
			bam_file= os.path.splitext(transcript[i][j])[0] + '.bam'
			cmd=bt.sam2bam(transcript[i][j], bam_file, repsam, free)
			transcript[i][j]= os.path.splitext(transcript[i][j])[0] + '_sorted.bam'
			cmd+=" ; \n" + bt.sort_bam(bam_file, transcript[i][j], repsam, free)
			cmd+=" ; \n" + bt.index_bam(transcript[i][j], repsam)
			#print(cmd)
			cmds.append(cmd)
	exe.threading_run(cmds, 'samtools', cpu)
	return transcript



def deeptools(transcript, genomeSize, param, repDeep, repResult="result/coverage", cpu=4):

#################    BigWig creation and visualisation with deeptools    #################

	print("\n\n"+"-"*20+" BigWig CREATION AND VISUALISATION WITH DEEPTOOLS "+"-"*20+"\n")
	
	if cpu>4:
		cpu =4
	
	with open(genomeSize) as fi:
		for li in fi:
			li=li.rstrip()
			chrSize=int(li.split("\t")[1])
	
	if param["normal"].lower=="none":
		param["normal"]=None
	else:
		param["normal"]=param["normal"].upper()
			
	print("Creation of BigWig:")
	cmds=[]
	bigwigList=[]
	bamList=[]
	for i in transcript:
		for j in transcript[i]:
			bigwigFile=os.path.basename(transcript[i][j])
			bigwigFile=repResult+"/"+os.path.splitext(bigwigFile)[0]+".bw"
			cmd=bt.bam2bw(transcript[i][j], bigwigFile, repDeep+"/bamCoverage", chrSize, param["normal"])
			bamList.append(transcript[i][j])
			transcript[i][j]=bigwigFile
			cmds.append(cmd)
			bigwigList.append(bigwigFile)
	exe.threading_run(cmds,"bamCoverage", cpu)
	
	print("\n\nPlot creation:\n")
	cmd=bt.bw2plot(bigwigList, repResult, repDeep+"/multiBigwigSummary",
		repDeep+"/plotCorrelation", repDeep+"/plotPCA", param["--binSize"], cpu)
	print(cmd,"\n")
	os.system(cmd)
	
	print("\n\nGenome Coverage:\n")
	numSample=len(bamList)
	cmd=bt.plot_coverage(bamList, repResult, numSample, repDeep+"/plotCoverage", param["--minMappingQuality"])
	print(cmd,"\n")
	os.system(cmd)




def featureCounts(transcript, annotGenome, FC_bin, output, se,
	p={"-t":['CDS','ncRNA','tRNA','regulatory_region','tmRNA','rRNA']}, cpu=4):
	
#################   Count the number of reads per features with featureCounts   #################

	print("\n\n"+"-"*20+" Count the number of reads for each selected features "+"-"*20,
		"\n"+"-"*37+" with featureCounts "+"-"*37+"\n")
	
	Lbam=[]
	for i in transcript:
		for j in transcript[i]:
			Lbam.append(transcript[i][j])	

	Fcount=output+"/rawCount"
	p["-t"]=",".join(p["-t"])
	
	cmd="{} -T {} -a {} -o {}.tsv ".format(FC_bin+"/featureCounts", cpu,  annotGenome, Fcount)
	cmd+= "-t {} ".format(p["-t"])
	if se == 0:
		cmd+="-p "

	cmd+=" ".join(Lbam)
	print(cmd+"\n")
	os.system(cmd)
	
	
	group=[]
	with open(Fcount+".tsv", "r") as fir:
		with open(Fcount+"a.tsv", "w") as fiw:
			li=next(fir)
			fiw.write(li)
			li=next(fir)
			li=li.rstrip()
			li=li.split("\t")
			for i in range(6,len(li)):
				for keyi in transcript:
					for keyj in transcript[keyi]:
						print(transcript[keyi][keyj],"\t", li[i])
						if transcript[keyi][keyj]==li[i]:
							li[i]=keyj
							group.append(keyi)
			fiw.write("\t".join(group)+"\n")
			li="\t".join(li)+"\n"
			fiw.write(li)
							
			for li in fir:
				fiw.write(li)
	cmd="rm {}.tsv; mv {}a.tsv {}.tsv".format(Fcount, Fcount, Fcount)
	os.system(cmd)
	return Fcount+".tsv"		
		


def fadu(fadu_bin, output, transcript, gff,
	p={"-f":['CDS','ncRNA','tRNA','regulatory_region','tmRNA','rRNA']}, cpu=4):
	
#################   Count the number of reads per features with Fadu  #################

	print("\n\n"+"-"*20+" Count the number of reads for each selected features "+"-"*20,
		"\n"+"-"*41+" with Fadu "+"-"*42+"\n")
	
	param=""
	for i in p:
		if type(p[i])==type(True):
			if p[i]:
				param+= " " + i
		elif type(p[i])==type(1):
			param+= " {} {}".format(i, p[i])
		elif i=="-f":
			param+= ' -f "{}"'.format(",".join(p[i]))
	cmds=[]
	
	
	for i in transcript:
		#print(i)
		for j in transcript[i]:
			#print(j)
			cmd= 'julia {}faduMod.jl -g "{}" -b "{}" -o "{}"'.format(fadu_bin, gff,
				transcript[i][j], output)
			cmd+=param
			cmds.append(cmd)
	exe.threading_run(cmds,"FADU", cpu)
	

	groupe=""
	for i in transcript:
		groupe += "{}\t".format(i)*len(transcript[i])
		print(i)
	groupe = groupe.rstrip()
	groupe += "\n"
	
	group1 = list(transcript.keys())[0]
	print(group1)
	sample1 = list(transcript[group1].keys())[0]
	print(sample1)
	firstSample = os.path.basename(transcript[group1][sample1]).split(".")[0]
	path = "{}/{}.counts.txt".format(output,firstSample)
	print(path)
	countJoin = pd.read_csv(path, sep='\t', header=0)
	countJoin = countJoin.iloc[: , :-2]
	countJoin = countJoin.rename(columns={"num_alignments" : sample1})
	print(countJoin.info())

	
	pathResult='{}/joinCounts/rawCount.tsv'.format(output)
	with open(pathResult,"w") as fiw:
		fiw.write("# Data produce by modified Fadu script\n")
		fiw.write(groupe)
	
	first=True
	for i in transcript:
		if first:
			lsample = list(transcript[i].keys())[1:]
			first=False
		else:
			lsample = list(transcript[i].keys())
		for j in lsample:
			sampleName = os.path.basename(transcript[i][j]).split(".")[0]
			path = "{}/{}.counts.txt".format(output,sampleName)
			mergingSamp = pd.read_csv(path, sep='\t', header=0)
			mergingSamp = mergingSamp.iloc[: , :-2]
			mergingSamp = mergingSamp.rename(columns={"num_alignments" : sampleName})
			#print(mergingSamp.info())
			colName=["featureID", "Chr","Start", "End", "Strand", "uniq_len"]
			countJoin = pd.merge(countJoin, mergingSamp, how="outer", on=colName)
			
	print(countJoin.info())
	#print(countJoin.head())
	countJoin.to_csv(pathResult, mode='a', sep="\t", header=True)
	return pathResult



def edger(edger_bin, scr_bin, inpCount, Nsample, output, p={'-n': 'TMM', '-c': 4, '-s': '0.375', '-t':'30'}):
	
#################   Normalization of the counts with EdgeR   #################
	
	print("\n\n"+"-"*20+" Count the number of reads for each selected features "+"-"*20)
	
	print(p)
	
	print(float(p["-s"]))
	if p["-s"][1]==".":
		p["-s"]=int(Nsample*float(p["-s"]))+1
	p["-n"]=p["-n"].upper()
	print(p)
	print(inpCount, "\n\n\n")
	cmd="Rscript {} -i {} -o {}".format(edger_bin, inpCount, output)
	for i in p:
		cmd+=" {} {}".format(i, p[i])
		
	print(cmd)
	os.system(cmd)
	edg.mdsPlot(output+"/MultiDimScaling.csv",output+"/js/")
	
	cmd="cp {}/plotly-2.3.0.min.js {}/mds.js {}/js/".format(scr_bin, scr_bin, output)
	os.system(cmd)
	cmd="cp {}/edgeMDS.html {}/".format(scr_bin, output)
	os.system(cmd)
	




if __name__ == '__main__':
	run()

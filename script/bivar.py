#!/usr/bin/python

from pickle import *
import re

def var_writer():

	f=open("bivar.bin", "wb")
	LparamGroup=["afterqc", "reads", "genome", "bowtie", "deeptools", "featCount", "fadu", "edger"]
	Dregex={"num":{}, "path":{}, "troolean":{}, "string":{}, "list":{}, "float":{}, "boolean":{}}
	Dregex["num"]={"afterqc":{}, "bowtie":{}, "deeptools":{}, "edger":{}, "fadu":{}}
	Dregex["path"]={"reads":{}, "genome":{}}
	Dregex["troolean"]={"reads":{}}
	Dregex["boolean"]={"fadu":{}}
	Dregex["sample"]={"reads":{}}
	Dregex["Bnum"]={"bowtie":{}}
	Dregex["string"]={"deeptools":{}, "edger":{}}
	Dregex["list"]={"featCount":{}, "fadu":{}}
	Dregex["float"]={"edger":{}}
	
	
	Dregex["path"]["genome"]["fna"]=re.compile("^genome fna:\s*(?P<genommefna>\S*)\s*$")
	Dregex["path"]["genome"]["gff"]=re.compile("^genome gff3:\s*(?P<genommegff3>\S*)\s*$")

	Dregex["path"]["reads"]["cp"]=re.compile("^reads commonPath:\s*(?P<commonPath>\S*)\s*$")
	Dregex["troolean"]["reads"]["se"]=re.compile("^reads singleEnd:\s*(?i:(true|false|maybe))\s*$")
	Dregex["sample"]["reads"]["sa"]=re.compile("^reads sample:\s*(?P<name>\S*)\s*(?P<group>\S*)\s*(?P<r1>\S*)\s*(?P<r2>\S*)\s*$")
	
	Dregex["num"]["afterqc"]["-f"]=re.compile("^afterqc trimming front \(-f\):\s*(-1|\d{1,2})\s*$")
	Dregex["num"]["afterqc"]["-t"]=re.compile("^afterqc trimming tail \(-t\):\s*(-1|\d{1,2})\s*$")
	Dregex["num"]["afterqc"]["-q"]=re.compile("^afterqc quality base \(-q\):\s*(\d+)\s*$")
	Dregex["num"]["afterqc"]["-p"]=re.compile("^afterqc poly size limit \(-p\):\s*(\d+)\s*$")
	Dregex["num"]["afterqc"]["-a"]=re.compile("^afterqc poly mismatch \(-a\):\s*(\d+)\s*$")
	Dregex["num"]["afterqc"]["-n"]=re.compile("^afterqc N base limit \(-n\):\s*(\d+)\s*$")
	Dregex["num"]["afterqc"]["-s"]=re.compile("^afterqc seq length \(-s\):\s*(\d+)\s*$")
		
	Dregex["num"]["bowtie"]["-p"]=re.compile("^bowtie number cpu \(-p\):\s*(\d+)\s*$")
	Dregex["Bnum"]["bowtie"]["-k"]=re.compile("^bowtie num of align \(-k\):\s*(?i:(None|\d+))\s*$")

	Dregex["num"]["deeptools"]["-n"]=re.compile("^plotCoverage num sample \(-n\):\s*(\d+)\s*$")
	Dregex["num"]["deeptools"]["--minMappingQuality"]=re.compile("^plotCoverage min mapping quality \(--minMappingQuality\):\s*(\d+)\s*$")
	Dregex["num"]["deeptools"]["--binSize"]=re.compile("^multiBigwigSummary binSize \(-bs\):\s*(\d+)\s*$")
	Dregex["string"]["deeptools"]["normal"]=re.compile("^bamCoverage normalize:\s*(?i:(none|rpkm|cpm|tpm|bpm))\s*$")	

	Dregex["list"]["featCount"]["-t"]=re.compile("featCount feature type \(-t\):\s*(?P<all>\w+(,\s*\w+)*)\s*$")
	
	Dregex["list"]["fadu"]["-f"]=re.compile("fadu feature type \(-f\):\s*(?P<all>\w+(,\s*\w+)*)\s*$")
	Dregex["boolean"]["fadu"]["-M"]=re.compile("^remove multi-mapped \(-M\):\s*(?i:(true|false))\s*$")
	Dregex["boolean"]["fadu"]["-p"]=re.compile("^proper pairs \(-p\):\s*(?i:(true|false))\s*$")
	Dregex["num"]["fadu"]["-m"]=re.compile("^max fragment size \(-m\):\s*(\d+)\s*$")
	
	
	Dregex["float"]["edger"]["-s"]=re.compile("^minimum number of sample \(-s\):\s*(?i:(\d+|[01]\.\d+))\s*$")
	Dregex["num"]["edger"]["-c"]=re.compile("^minimum count per sample \(-c\):\s*(?i:(\d+))\s*$")
	Dregex["string"]["edger"]["-n"]=re.compile("^normalization method \(-n\):\s*(?i:(upperquartile|none|rle|tmm))\s*$")
	Dregex["num"]["edger"]["-t"]=re.compile("^top count heatmap\(-t\):\s*(?i:(\d+))\s*$")
	
	
	binary={"Dregex":Dregex, "LparamGroup":LparamGroup}
	dump(binary, f)
	f.close()



if __name__ == '__main__':
	var_writer()
#	var_Twriter()


"""
def var_Twriter():
	f=open("lbivar.bin", "wb")
	LparamGroup=["afterqc", "reads"]
	Tregex=[]
	
	Tregex.append((re.compile("^afterqc trimming front \(-f\):\s*(-1|\d{1,2})\s*$"), "num", "afterqc", "f"))
	Tregex.append((re.compile("^afterqc trimming tail \(-t\):\s*(-1|\d{1,2})\s*$"), "num", "afterqc", "t"))
	Tregex.append((re.compile("^afterqc quality base \(-q\):\s*(\d+)\s*$"), "num", "afterqc", "q"))
	Tregex.append((re.compile("^afterqc poly size limit \(-p\):\s*(\d+)\s*$"), "num", "afterqc", "p"))
	Tregex.append((re.compile("^afterqc poly mismatch \(-a\):\s*(\d+)\s*$"), "num", "afterqc", "a"))
	Tregex.append((re.compile("^afterqc N base limit \(-n\):\s*(\d+)\s*$"), "num", "afterqc", "n"))
	Tregex.append((re.compile("^afterqc seq length \(-s\):\s*(\d+)\s*$"), "num", "afterqc", "s"))
	
	Tregex.append((re.compile("^reads commonPath:\s*(?P<commonPath>\S*)\s*$"), "path", "reads", "cp"))
	Tregex.append((re.compile("^reads singleEnd:\s*(?i:true|false|maybe)\s*$"), "troolean", "reads", "se"))
	Tregex.append((re.compile("^reads sample:\s*(?P<name>\S*)\s*(?P<group>\S*)\s*(?P<r1>\S*)\s*(?P<r2>\S*)\s*$"), "sample", "reads","sa"))
	
	Tregex=tuple(Tregex)
	binary={"Tregex":Tregex, "LparamGroup":LparamGroup}
	dump(binary, f)
	f.close()
"""

"""
	confData={"genome":{}, "reads":{}, "afterqc":{}}
	
	confData["afterqc"]["f"]=re.compile("^trimming front \(-f\):\s*(-+\S+)\s*$")
	confData["afterqc"]["t"]=re.compile("^trimming tail \(-t\):\s*(-+\S+)\s*$")
	confData["afterqc"]["q"]=re.compile("^quality base \(-q\):\s*(\S+)\s*$")
	confData["afterqc"]["p"]=re.compile("^poly size limit \(-p\):\s*(\S+)\s*$")
	confData["afterqc"]["a"]=re.compile("^poly mismatch \(-a\):\s*(\S+)\s*$")
	confData["afterqc"]["n"]=re.compile("^N base limit \(-n\):\s*(\S+)\s*$")
	confData["afterqc"]["s"]=re.compile("^seq length \(-s\):\s*(\S+)\s*$")
	
	confData["reads"]["commonPath"]=re.compile("^commonPath:\s*(?P<commonPath>\S*)\s*$")
	confData["reads"]["singleEnd"]=confSingleEnd=re.compile("^singleEnd:\s*(?P<singEnd>\S*)\s*$")
	confData["reads"]["sample"]=re.compile("^sample:\s*(?P<name>\S*)\s*(?P<group>\S*)\s*(?P<r1>\S*)\s*(?P<r2>\S*)\s*$")
"""
"""
	startli=["genome fn", "genome bed", "reads commonPath:", "reads sample:", "afterqc trimming front", "afterqc trimming tail", "afterqc quality base", "afterqc poly size limit", "afterqc poly mismatch", "afterqc N base limit", "afterqc seq length"]
	
	confData={"genome":{}, "reads":{}, "afterqc":{}}
	
	confData["num"]["afterqc trimming front"]=re.compile("^afterqc trimming front \(-f\):\s*(-?\S+)\s*$")
	confData["num"]["afterqc trimming tail"]=re.compile("^afterqc trimming tail \(-t\):\s*(-?\S+)\s*$")
	confData["num"]["afterqc quality base"]=re.compile("^afterqc quality base \(-q\):\s*(\S+)\s*$")
	confData["num"]["afterqc poly size limit"]=re.compile("^afterqc poly size limit \(-p\):\s*(\S+)\s*$")
	confData["num"]["afterqc poly mismatch"]=re.compile("^afterqc poly mismatch \(-a\):\s*(\S+)\s*$")
	confData["num"]["afterqc N base limit"]=re.compile("^afterqc N base limit \(-n\):\s*(\S+)\s*$")
	confData["num"]["afterqc seq length"]=re.compile("^afterqc seq length \(-s\):\s*(\S+)\s*$")
	
	confData["path"]["reads commonPath"]=re.compile("^reads commonPath:\s*(?P<commonPath>\S*)\s*$")
	confData["inst"]["reads singleEnd"]=confSingleEnd=re.compile("^reads singleEnd:\s*(?P<singEnd>\S*)\s*$")
	confData["sample"]["reads sample"]=re.compile("^reads sample:\s*(?P<name>\S*)\s*(?P<group>\S*)\s*(?P<r1>\S*)\s*(?P<r2>\S*)\s*$")

	binary={"regex":confData, "start":startli}
"""

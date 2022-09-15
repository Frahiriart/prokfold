

def index(genome, output, bowtie2Build_bin):
	
	'''Generate index of genome with bowtie2_build'''
	cmd='{} {} {}'.format(bowtie2Build_bin, genome, output)
	return cmd


def bowtie2(output, index, fq1, fq2=None, bowbin="bowtie2", k=None, p=1, free=1):

	'''Alignement of reads on the indexed genome with bowtie2'''
	if fq2:
		cmd= "{} -x {} -1 {} -2 {}".format(bowbin, index, fq1, fq2)
	else:
		cmd= "{} -x {} -U {}".format(bowbin, index, fq1)
	if k or k=="None":
		cmd+=" -k {}".format(k)
	cmd+= " -p {} -S {} 2> {}.alignSummary".format(p, output, output)
	if free==2:
		cmd+= " ; rm {} {}".format(fq1, fq2)
	return cmd


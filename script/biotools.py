import os
import pandas as pd
#from execute import run
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from BCBio import GFF


def sam2bam(sam_file, bam_file=None, samtools_bin="samtools", free=1):
    '''Convert sam file to bam file'''
    if bam_file is None:
        bam_file = os.path.splitext(sam_file)[0] + '.bam'
    cmd = "{} view -bS {} > {}".format(samtools_bin, sam_file, bam_file)
    if free:
    	cmd+= " ; rm {}".format(sam_file) 
    return cmd



def sort_bam(bam_file, sorted_bam_file=None, samtools_bin="samtools", free=1):
    '''Sort bam file'''
    if sorted_bam_file is None:
        sorted_bam_file=os.path.splitext(bam_file)[0] +'_sorted.bam'
    cmd = "{} sort {} -o {}".format(samtools_bin, bam_file, sorted_bam_file)
    if free:
    	cmd+= " ; rm {}".format(bam_file)
    # cmd = "samtools sort {} -o {}; rm {}; echo {}".format(bam_file, sorted_bam_file, bam_file, sorted_bam_file)
    return cmd



def index_bam(sorted_bam_file, samtools_bin="samtools"):
    '''Index bam file'''
    cmd = "{} index {}".format(samtools_bin, sorted_bam_file)
    return cmd



def chromosome_sizes(genome_fasta_file, output):
    '''Extract the size of chromosome'''
    # Uncompress genome zip file
    resultName=os.path.basename(genome_fasta_file)
    resultName=resultName.split(".")[0]
    genome=False
    if genome_fasta_file.endswith('.gz'):
        genome = output + "/" + resultName + '.fasta'
        cmd = "gunzip -c {} > {}".format(genome_fasta_file, genome)
        print(cmd)
        os.system(cmd)
        genome_fasta_file = genome
    # Generate chromosome size file
    chr_size_file = output + "/" + resultName + '_size.tsv'
    with open(chr_size_file, 'w') as sz:
        for rec in SeqIO.parse(genome_fasta_file, "fasta"):
            print(rec)
            sz.write("{}\t{}\n".format(rec.id, len(rec.seq)))
    return chr_size_file, genome
    

   
def bam2bw(sorted_bam_file, bigwig_file, bamCoverage_bin='bamCoverage', genomeSize=None, normalize=None):
    '''Convert bam file as normalized bigwig file '''
    cmd = "{} -b {} -o {} ".format(bamCoverage_bin, sorted_bam_file, bigwig_file)
    if normalize in ['BPM', 'TPM']:
        cmd = cmd + "--normalizeUsing BPM"
    elif normalize == 'RPKM':
        cmd = cmd + "--normalizeUsing RPKM"
    elif normalize == 'CPM':
        cmd = cmd + "--normalizeUsing CPM"
    cmd+=" --effectiveGenomeSize {} ".format(genomeSize)
    return cmd



def bw2plot(bigwig_files, outdir, bamMBWS_bin='multiBigwigSummary', plotC_bin="plotCorrelation", plotPCA_bin="plotPCA",  binSize=1000, cpu=4):
    '''Summarize bigwig files as table, correlation and PCA plots'''
    # Summary
    bigwig_files.sort()
    summary_array_file = os.path.join(outdir, 'summary_bigwigs.npz')
    summary_tab_file = os.path.join(outdir, 'summary_bigwigs.tsv')
    cmd1 = "{} bins --smartLabels --binSize {} -b {} -o {} --outRawCounts {} -p {}".format(bamMBWS_bin, binSize, ' '.join(bigwig_files), summary_array_file, summary_tab_file, cpu)
    # Spearman's correlation
    correlation_plot_file = os.path.join(outdir, 'correlation_bigwigs.png')
    correlation_tab_file = os.path.join(outdir, 'correlation_bigwigs.tsv')   
    cmd2 = "{} --plotNumbers --skipZeros --corData {} --corMethod spearman --whatToPlot heatmap -o {} --plotFileFormat png --outFileCorMatrix {}".format(plotC_bin ,summary_array_file, correlation_plot_file, correlation_tab_file) 
    # PCA
    pca_plot_file = os.path.join(outdir, 'pca_bigwigs.png')
    pca_tab_file = os.path.join(outdir, 'pca_bigwigs.tsv')     
    cmd3 = "{} --transpose --corData {} --plotFile {} --outFileNameData {} ".format(plotPCA_bin, summary_array_file, pca_plot_file, pca_tab_file)
    cmd = "{};{};{}".format(cmd1, cmd2, cmd3)
    return cmd



def plot_coverage(sorted_bam_files, outdir, n, plotCoverage_bin='plotCoverage', minMappingQuality=0):
    '''genome coverage from bam'''
    plot_file = os.path.join(outdir, 'plot_coverage.png')
    tab_file = os.path.join(outdir, 'plot_coverage.tsv')
    cmd = "{} --ignoreDuplicates --smartLabels --skipZeros --plotFileFormat png -b {} -o {} --outRawCounts {} -n {} --minMappingQuality {} ".format(plotCoverage_bin, ' '.join(sorted_bam_files), plot_file, tab_file, n, minMappingQuality)
    return cmd








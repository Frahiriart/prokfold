import os


#def fastqc(fq, fastqc_dir, fastqc_bin="fastqc"):
def fastqc(fq, fastqc_dir, fastqc_bin="fastqc"):

    '''Generate reads QC with FastQC'''
    cmd = '{} {} --outdir {}'.format(fastqc_bin, fq, fastqc_dir)
    return cmd


def afterqc(afterqc_dir, fq1, fq2=None, f="-1", t="-1", q="20", p="35", a="5", n="5", s="35",
    pypy_bin="pypy.py", afterqc_bin="after.py"):

    '''Filtering & Trimming of reads with afterQC'''
    # Set filtered reads directories
    if os.path.exists(afterqc_dir)==False:
        os.mkdir(afterqc_dir)
    good_reads_dir = os.path.join(afterqc_dir, "good_reads")
    if os.path.exists(good_reads_dir)==False:
        os.mkdir(good_reads_dir)

    bad_reads_dir = os.path.join(afterqc_dir, "bad_reads")
    if os.path.exists(bad_reads_dir)==False:
        os.mkdir(bad_reads_dir)

    # Filtering with afterqc
    if fq2:
        cmd = "{} {} -1 {} -2 {} ".format(pypy_bin, afterqc_bin, fq1, fq2)
    else:
        cmd = "{} {} -1 {} ".format(pypy_bin, afterqc_bin, fq1)
    cmd = cmd + "-g {} -b {} ".format(good_reads_dir, bad_reads_dir)
    cmd = cmd + "-f {} -t {} -q {} -p {} -a {} -n {} -s {}".format(f, t, q, p, a, n, s)
    return cmd

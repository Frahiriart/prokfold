import subprocess
import re
import threading


def threading_run(cmds, mod, np):
    '''Multithreading to run commands in parallel'''
    jobs = list()
    #print(cmds)
    for i in range(0, len(cmds), int(np)):
        for k in range(i, i + int(np), 1):
            try:
                cmds[k]
            except IndexError:
                print("")
            else:
                print("Running {} as {}\n".format(mod, cmds[k]))
                th = threading.Thread(target=run, args=(cmds[k], mod))
                jobs.append(th)
                print(" -> starting thread {}".format(th))
                th.start()
        for j, job in enumerate(jobs):
            print(j,"---------------------", job)
            job.join()
            print(job)

def run(cmd, mod):
    '''Run commands from shell and generate error messages'''
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        if(re.search("fastqc", mod)): fastqcErrMsg()
        elif(re.search("afterqc", mod)): afterqcErrMsg()
        elif(re.search("salmon", mod)): salmonErrMsg()
        elif (re.search("samtools", mod)): samtoolsErrMsg()
        elif (re.search("wigtobw", mod)): wigtobwErrMsg()
        elif (re.search("geneBody_coverage", mod)): geneBody_covErrMsg()
        elif (re.search("bmToBigWig", mod)): bmToBigWigErrMsg()
        elif (re.search("subread-buildindex", mod)): subreadErrMsg(mod)
        elif (re.search("subread-align", mod)): subreadErrMsg(mod)
        elif (re.search("featureCounts", mod)): subreadErrMsg(mod)
#        if(re.search("featcnt",mod)): errMsg.featCntErrMsg()
#        if(re.search("DESeq",mod)): errMsg.DESeqErrMsg()
#        if(re.search("edgeR",mod)): errMsg.EdgeRErrMsg()
#        if(re.search("noiseq",mod)): errMsg.DESeqErrMsg()
#        if(re.search("limma",mod)): errMsg.limmaErrMsg()
        exit(1)
    else:
        print("Output from {}:\n{}Success.\n".format(mod, output))
        return output


def fastqcErrMsg():
    fastqcErrorMsg = """
                     IN CASE OF ERROR
                     Suggestions for most common errors:
                     Error: Status : FAIL 127 /bin/sh: ... ... ... fastqc: No such file or directory
                     Fix: Please check the path of the fastqc executables.
                     """
    print(fastqcErrorMsg)
    return 1


def afterqcErrMsg():
    afterqcErrorMsg = """
                      IN CASE OF ERROR
                      Suggestions for most common errors:
                      Error: Status : FAIL 127 /bin/sh: ... ... ...pypy: No such file or directory
                      Fix: Please check the path of the pypy executables.
                      pypy: error while loading shared libraries: libbz2.so.1.0: cannot open shared object file: No such file or directory
                      Fix:         ln -s /usr/lib64/libbz2.so.1.0.6 /usr/lib64/libbz2.so.1.0
                      pypy: error while loading shared libraries: libtinfo.so.5: cannot open shared object file: No such file or directory
                      Fix:         ln -s libtinfo.so.6.1 libtinfo.so.5
                      """
    print(afterqcErrorMsg)
    return 1


def salmonErrMsg():
    salmonErrorMsg = """
                     IN CASE OF ERROR
                     Suggestions for most common errors:
                     Error: Status : FAIL 127 /bin/sh: ... ... ...salmon / build / quant: No such file or directory
                     Fix: Please check the path of the salmon executables.
                     Error: Permission denied.
                     Fix: Check the permission of the directory and give permission.
                     """
    print(salmonErrorMsg)
    return 1


def samtoolsErrMsg():
    samtoolsErrorMsg = """
                      IN CASE OF ERROR
                      Suggestions for most common errors:
                      Error: Status : FAIL 127 /bin/sh: ... ... ...samtools: No such file or directory
                      Fix: Please check the path of the samtools executables.
                      Error: Permission denied.
                      Fix: Check the permission of the directory and give permission.
                      """
    print(samtoolsErrorMsg)
    return 1


def bmToBigWigErrMsg():
    bmToBigWigErrMsg = """
                    IN CASE OF ERROR
                    Suggestions for most common errors:
                    Error: Status : FAIL 127 /bin/sh: ... ... ...samtools/wigToBigWig: No such file or directory
                    Fix: Please check the path of the samtools/wigToBigWig executables.
                    Error: Permission denied.
                    Fix: Check the permission of the directory and give permission.
                    """
    print(bmToBigWigErrMsg)
    return 1


def geneBody_covErrMsg():
    geneBody_covErrMsg = """
                         IN CASE OF ERROR
                         Suggestions for most common errors:
                         Error: Status : FAIL 127 /bin/sh: ... ... ...geneBody_coverage.py: No such file or directory
                         Fix: Please check the path of the geneBody_coverage executables.
                         Error: Permission denied.
                         Fix: Check the permission of the directory and give permission.
                         """
    print(geneBody_covErrMsg)
    return 1


def subreadErrMsg(mod):
    subreadErrMsg = """
                    IN CASE OF ERROR
                    Suggestions for most common errors:
                    Error: Status : FAIL 127 /bin/sh: ... ... ...{}: No such file or directory
                    Fix: Please check the path of the subread executables.
                    Error: Permission denied.
                    Fix: Check the permission of the directory and give permission.
                    """.format(mod)
    print(subreadErrMsg)
    return 1

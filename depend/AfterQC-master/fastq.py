 #!/usr/bin/env python
  
import gzip
import bz2
import os,sys

def isFastq(f):
    fqext = (".fq", ".fastq", ".fq.gz", ".fastq.gz", ".fq.bz2", ".fastq.bz2")
    for ext in fqext:
        if f.endswith(ext):
            return True
    return False

################################
#fastq.reader

class Reader:

    def __init__(self, fname):
        self.__file = None
        self.__eof = False
        self.filename = fname
        if self.filename.endswith(".gz"):
            self.__file = gzip.open(self.filename, "r")
        elif self.filename.endswith(".bz2"):
            self.__file = bz2.BZ2File(self.filename)
        else:
            self.__file = open(self.filename, "r")
        if self.__file == None:
            print("Failed to open file " + self.filename)
            sys.exit(1)
            
    def __del__(self):
        if self.__file != None:
            self.__file.close()
            
    def nextRead(self):
        if self.__eof == True or self.__file == None:
            return None

        lines = []
        #read 4 (lines, name, sequence, strand, quality)
        for i in xrange(0,4):
            line = self.__file.readline().rstrip()
            if len(line) == 0:
                self.__eof = True
                return None
            lines.append(line)
        return lines

    def isEOF(self):
        return False

################################
#fastq.writer

class Writer:
    
    filename = ""
    
    __file = None
    
    def __init__(self, fname, force_gzip = False, gzip_compression = 2):
        self.filename = fname
        if not self.filename.endswith(".gz") and force_gzip:
            self.filename = self.filename + ".gz"
        if self.filename.endswith(".gz"):
            self.__file = gzip.open(self.filename, "w", compresslevel = gzip_compression)
        elif self.filename.endswith(".bz2"):
            print("ERROR: Write bzip2 stream is not supported")
            sys.exit(1)
        else:
            self.__file = open(self.filename, "w")
        if self.__file == None:
            print("Failed to open file " + self.filename + " to write")
            sys.exit(1)

    def flush(self):
        if self.__file !=None:
            self.__file.flush()

    def close(self):
        if self.__file !=None:
            self.__file.flush()
            self.__file.close()
 
    def writeLines(self, lines):
        if self.__file == None:
            return False
            
        for line in lines:
            self.__file.write(line+"\n")
        return True
            
    def writeRead(self, name, seqence, strand, quality):
        if self.__file == None:
            return False
            
        self.__file.write(name+"\n")
        self.__file.write(seqence+"\n")
        self.__file.write(strand+"\n")
        self.__file.write(quality+"\n")
        
        return True

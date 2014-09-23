import os,sys
import time
import hashlib


baseline_dir_dict = r"baseline_dict.txt"
working_dir_dict = r"working_dir_dict.txt"
patch_dir =r"patch"


omit_dir = {'.svn':1,'.git':1,'out':1,'ccache':1}
omit_file = {'.gitignore':1,'.gitattributes':1,'v8.log':1}
#omit_fileExt = {'.bin':1,'.img':1,'.bak':1}
omit_fileExt = {'.bak':1,'.o':1,'.obj':1,'.class':1,'.cmd':1,'.builtin':1,'.order':1}

size_limit = 50000000 # 50M. files over size_limit will be omited. set to 0 if don't want to limit

TRUNK_DIR = 'Trunk'
TAGS_DIR = 'Tag'

ADD_DIR= 'add'
REMOVE_DIR = 'remove'



TRUNK_DIR = 'Trunk'
TAGS_DIR = 'Tags'

ADD_DIR = 'add'
REMOVE_DIR = 'remove'


def md5Checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    fh.close()
    return m.hexdigest()

class Exporter:
    def __init__(self):
        pass
    def close(self):
        pass
    def export(self,strInfo):
        pass

class ConsoleExporter( Exporter ):
    def __init__(self):
        pass
    def close(self):
        pass        
    def export(self,strInfo):
        print strInfo
        pass

#todo: add teardown to close file    
class FileExporter ( Exporter ):
    
    def __init__(self,output_file_name):
        self.output_file_name = output_file_name
        self.output_file = open(output_file_name,'w')
    
    def close(self):
        self.output_file.flush()
        self.output_file.close()
        pass
    
    def export(self,strInfo):
        self.output_file.write(strInfo)
        self.output_file.write('\n')
      

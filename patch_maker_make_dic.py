#!/usr/bin/python 
import DirBrowser
import os,sys
import time
import hashlib
from util import *
from sanity_check import *

#add current dir to sys path
sys.path.append(os.getcwd())
try:
    from patch_maker_config import *
except Exception as err:  
    print "Error: Can't load [patch_maker_config.py]."
    exit(1)    
#import patch_maker_config



cur_script_name = ""
cur_path = os.getcwd()



      
#todo: don't add file .gitignore
class myDirBrowser(DirBrowser.DirBrowser):
    
    def __init__(self , exporter , strInitDir="",):
        DirBrowser.DirBrowser.__init__(self,strInitDir)
        self.exporter = exporter
        self.quickCheckDic = {}
        
    def SetQuickCheckDic(self, quickCheckDic):
        self.quickCheckDic = quickCheckDic
        self.quickCheckDicUse = 0
        pass    
    def ProcessFile(self, strFilename,strDir):     
        fullName = os.path.join(strDir,strFilename)
        #relativeName = fullName.replace(self.m_strInitDir,'')
        relativeName = os.path.relpath(fullName ,self.m_strInitDir)   
        #print relativeName 
        
        #dirty solution. redo it later
        if(fullName.rfind('/uboot/build/') != -1): # omit /uboot/build
        	return 0
        
        lastUpdateTime = str(os.path.getmtime(fullName))
        fsize =  os.path.getsize(fullName)
        fileSize = str(fsize )
        
        if size_limit != 0 and fsize > size_limit: # omit big file
            return 0
        
        if self.quickCheckDic.has_key(relativeName ):
            #print "has key"
            info = self.quickCheckDic[relativeName ]
            if info[0] == 'File':
                time = info[2]
                size = info[3]
                if time == lastUpdateTime and size == fileSize:
                    file_md5 = info[4]
                    self.quickCheckDicUse += 1
                    #print "bingo"
                else:
                    file_md5 = md5Checksum(fullName)    
                    
        else:                
            file_md5 = md5Checksum(fullName)
        
        
        
        strInfo = "File;%s;%s;%s;%s"%(relativeName,lastUpdateTime ,fileSize ,file_md5 )
        self.exporter.export(strInfo)
        
        
        #print "FILE:"+fullName + ","+ "timestemp:"+str(os.path.getmtime(fullName))+","+"filesize:"+str(os.path.getsize(fullName))
        pass
    def ProcessDir(self,strCurrentdir,strParentdir):
        
        if(strParentdir == None): # first level. do nothing
            pass
        else:
            fullDir = os.path.join(strParentdir,strCurrentdir)
            #relativeDir = fullDir.replace(self.m_strInitDir,'')
            relativeDir = os.path.relpath(fullDir ,self.m_strInitDir)    
            #dirty solution. redo it later    
            if(relativeDir.rfind('uboot/build/') != -1): # omit /uboot/build
                return 0
                
            #print "DIR:"+strCurrentdir+","
            #print "DIR:"+fullDir + ","+ "timestemp:"+str(os.path.getmtime(fullDir))
            #print "DIR;%s;%s"%(relativeDir ,str(os.path.getmtime(fullDir)))
            strInfo = "DIR;%s;%s"%(relativeDir ,str(os.path.getmtime(fullDir)))
            self.exporter.export(strInfo)
            pass
            

def read_baseline_dict_file():
    baseline_dict_file = open(os.path.join(cur_path,baseline_dir_dict),'r')
    lines2 = baseline_dict_file.readlines()
    baseline_dict = {}
    for line2 in lines2:
        try:
            filename2 = line2.strip('\n').split(';')[1]
        except Exception as err:  
            print filename2 
        if(baseline_dict.has_key(filename2 ) == True): # should not be here. todo: raise exception
            print filename2
            print "woo2"
        else:
            baseline_dict[filename2] = line2.strip('\n').split(';')

    print "Current baseline_dic has ", len(baseline_dict), " items"
    return baseline_dict 

def read_working_dict_file():
    working_dict_file = open(os.path.join(cur_path,working_dir_dict),'r')
    lines2 = working_dict_file.readlines()
    working_dict = {}
    for line2 in lines2:
        try:
            filename2 = line2.strip('\n').split(';')[1]
        except Exception as err:  
            print filename2 
        if(working_dict.has_key(filename2 ) == True): # should not be here. todo: raise exception
            print filename2
            print "woo2"
        else:
            working_dict[filename2] = line2.strip('\n').split(';')

    print "Current working_dic has ", len(working_dict), " items"
    return working_dict
               
'''
Format:
DIR;name;timestamp
File;name;timestamp;size;md5
--
sample:
DIR;/home/OTT/AmlogicMX_SDK_work/abi/cpp/src;1398758161.48
File;/home/OTT/AmlogicMX_SDK_work/abi/cpp/src/new.cc;1398758161.48;1810;19d457206ae85045171540394d65f7bf
'''
def make_working_dir_dict():
    #make working dir dict
    print "make working_dir_dict"
    startTime = time.time()
    
    quickCheckDic = {}
    if os.path.exists(os.path.join(cur_path,working_dir_dict)):
        quickCheckDic  = read_working_dict_file()
    
    os.chdir(cur_path)
    exporter2 =  FileExporter(working_dir_dict)
    
    working_dir_Brower = myDirBrowser(exporter2 )
    
    working_dir_Brower.SetOmitDir( omit_dir )  # only one level dir name. if want more, do in derived class
    working_dir_Brower.SetOmitFile( omit_file ) # file full name
    working_dir_Brower.SetOmitFileExt( omit_fileExt ) # file extend name
    
    working_dir_Brower.SetQuickCheckDic(quickCheckDic)
    
    if(working_dir_Brower.SetInitDir(working_dir)==0):
        print ("false")
    else:
        working_dir_Brower.BeginBrowse()        
        pass
    
    print working_dir_Brower.quickCheckDicUse
    exporter2.close()
    endTime = time.time()
    print "     done. Use time " , str(endTime - startTime),  " second"
    
    
    
    
def make_baseline_dir_dict():    
    #make baseline dir dict
    print "make baseline_dict "
    startTime = time.time()
    quickCheckDic = {}
    if os.path.exists(os.path.join(cur_path,baseline_dir_dict)):
        quickCheckDic  = read_baseline_dict_file()
        
    os.chdir(cur_path)
    exporter =  FileExporter(baseline_dir_dict)

    baseBrower = myDirBrowser(exporter)
    baseBrower.SetOmitDir( omit_dir  )  # only one level dir name. if want more, do in derived class
    baseBrower.SetOmitFile(omit_file)
    baseBrower.SetOmitFileExt(omit_fileExt )
    
    baseBrower.SetQuickCheckDic(quickCheckDic)

    if(baseBrower.SetInitDir(baseline_dir)==0):
        print ("false")
    else:
        #print a.m_strInitDir
        baseBrower.BeginBrowse()
    print baseBrower.quickCheckDicUse
    exporter.close()
    endTime = time.time()
    print "     done. Use time " , str(endTime - startTime),  " second"

def usage():
    print '''Usage: patch_maker_make_dic  [ WORKING | BASELINE | ALL ]
    '''
    
def main():
    #print sys.argv
    if len(sys.argv) != 2:
        usage()
        exit(1)
    if sainity_check() != 0:
        print "\n----\n     Check Failed. Can't make_dic"
        exit(2)
        
    if sys.argv[1].upper() ==  'WORKING':
        make_working_dir_dict()
    elif sys.argv[1].upper() ==  'BASELINE':            
        make_baseline_dir_dict()
    elif sys.argv[1].upper() ==  'ALL':       
        make_working_dir_dict()
        make_baseline_dir_dict()      
    elif sys.argv[1] == '-h':
        usage()  
    else:
        usage()
    
    print "done"     

if __name__ == '__main__':
    main()
    #cur_script_name = sys.argv[0]
    #cur_path = os.path.dirname(sys.argv[0])
    
    #testDirBrowser()
    
 
            
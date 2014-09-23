#!/usr/bin/python 
import os,sys
import re
from util import *


#add current dir to sys path
sys.path.append(os.getcwd())
try:
    from patch_maker_config import *
except Exception as err:  
    print "Error: Can't load [patch_maker_config.py]."
    exit(1)    

def check_version_control_format(version_control_file_path):
    f = open(version_control_file_path,'r')
    line = f.readline().strip()
    print "     VERSION_CONTROL format check:"
    if(line[0:5] != 'Trunk' and line[0:4] != 'Tags'):
        print '''        VERSION_CONTROL.txt format error. Must start with:  Trunk | Tags
            ''' ,
        print 'Current is: ',line
           
        return -1,line
    else:
        print '''         VERSION_CONTROL.txt format good.
        ''',
        print 'Current is: ',line
        return 0,line

def check_release_notes_format(release_notes_file_path,version_line):
    
    if version_line == '':
        return -1
    f = open(release_notes_file_path,'r')
    data = f.read()
    
    print "     release_notes format check:"
    if version_line != 'Trunk':
        
        # try to find string "[ Tags 1.00.00 ]"
        pp = re.compile('\[(\s*)(%s)(\s*)\]'%version_line) #\s match 0 or any space
        p = re.search(pp,data) 
        if p != None:
            print "         Version info: ", version_line , " Found in release_notes.txt"
            return 0
        else:
            print "         Version info: ", version_line , "\n         Can't be found in release_notes.txt. Must has correct version record "
            return -1
    else:
        print "         Current is Trunk. Nothing checked"            
        return 0
    
def sainity_check():
    ret = 0
    cur_path = os.getcwd()
    
    print "Checking..."
    if os.path.exists(os.path.join(cur_path,'patch_maker_config.py')):
        print "Check patch_maker_config.py in ",cur_path, " - Ok"
        ret += 0
    else:
        print "Check patch_maker_config.py in ",cur_path, " - Fail"
        ret += -1
    
    if os.path.exists(baseline_dir):
        print "Check baseline_dir exist: ", baseline_dir, " - Ok"
        ret += 0
    else:
        print "Check baseline_dir exist: ", baseline_dir, " - Fail"
        ret += -1
    
    if os.path.exists(working_dir):
        print "Check working_dir exist: ",working_dir, " - Ok"
        ret += 0
    else:
        print "Check working_dir exist: ",working_dir, " - Fail"
        ret += -1

    version_control_file_path = os.path.join(working_dir,'VERSION_CONTROL.txt')
    version_line = ''
    if os.path.exists(version_control_file_path):
        print "Check VERSION_CONTROL.txt exist: ",version_control_file_path, " - Ok"
        rret , version_line  = check_version_control_format(version_control_file_path)
        ret += 0
        ret += rret 
    else:
        print "Check VERSION_CONTROL.txt exist: ",os.path.join(working_dir,'VERSION_CONTRL.txt'), " - Fail"
        ret += -1
    
    release_notes_file_path = os.path.join(working_dir,'release_notes.txt')
    if os.path.exists(release_notes_file_path):
        print "Check release_notes.txt exist: ",release_notes_file_path, " - Ok"
        rret = check_release_notes_format(release_notes_file_path,version_line)
        ret += 0
        ret += rret
    else:
        print "Check release_notes.txt exist: ",release_notes_file_path, " - Fail"
        ret += -1
    print "Check done"
    return ret
if __name__ == '__main__':
    print sainity_check()            
import sys
import os
import time
import shutil 
import base64
from util import *
from sanity_check import *

import patch_maker_make_dic
import gen_do_patch

#add current dir to sys path
sys.path.append(os.getcwd())
try:
    from patch_maker_config import *
except Exception as err:  
    print "Error: Can't load [patch_maker_config.py]."
    exit(1)

cur_path = os.getcwd()
print "cur_path:",cur_path 

#--do sainity check at first-------    
if sainity_check() != 0:
    print "\n----\n     Check Failed. Can't make_patch"
    exit(2)

#--update baseline dic
print "create or update baseline dic if anything changed....."
patch_maker_make_dic.make_baseline_dir_dict()

#--update working dic
print "create or update working dic if anything changed....."
patch_maker_make_dic.make_working_dir_dict()

#---------        
baseline_dict_file = open(os.path.join(cur_path,baseline_dir_dict),'r')
working_dict_file = open(os.path.join(cur_path,working_dir_dict),'r')

workDir = working_dir
baselineDir  = baseline_dir
patchDir = os.path.join(cur_path,patch_dir)

#VERSION_CONTROL.txt must contain only one line, format as:
#Trunk 
# or
#Tags 1.00.01 
#
#function retrun a string as:
# Trunk
#  or
# Tags\1.00.00
def TrunkTag_Path():
    version_file_path = os.path.join(workDir,'VERSION_CONTROL.txt')
    version_file = open(version_file_path,'r')
    Trunk_Tag = version_file.readline()
    #Trunk_Tag = Trunk_Tag.upper()
    version_file.close()
    p = Trunk_Tag.split()
    if p[0].upper() == 'TRUNK':
        return 'Trunk'
    else:
        p = Trunk_Tag.split()
        return os.path.join('Tags',p[1])
    
lines1 = baseline_dict_file.readlines()
lines2 = working_dict_file.readlines()

baseline_dict = {}
working_dict = {}

for line1 in lines1:
    try:
        filename1 = line1.split(';')[1]
        
    except Exception as err:  
        print filename1 
        
    if(baseline_dict.has_key(filename1 ) == True):  # should not be here. todo: raise exception  
        print filename1
        print "woo1"
    else:
        baseline_dict[filename1] = line1.strip('\n').split(';')
        

print "baseline has ",len(baseline_dict)," items"

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

print "working has ", len(working_dict), " items"


TRUNKTAG_PATH = TrunkTag_Path()
# now pick up items
# new add at first
# if match, will be set to 1. otherwise, will be keep
add_items = []

for item in working_dict:
    if baseline_dict.has_key(item) == True: # same name
        if working_dict[item][0] == 'DIR': # dir only check existency
             working_dict[item].append( 1 )
        else:   # file need check md5 
            if baseline_dict[item][4] == working_dict[item][4]: # check MD5
                working_dict[item].append( 1 )

#print working_dict        

for item in sorted(working_dict.keys()):
    if working_dict[item][-1] == 1 :
        pass
    else:
        #print working_dict[item] # patch's add item
        add_items.append(working_dict[item])
        
print '===================='    
remove_items = []
for item in baseline_dict:
    if working_dict.has_key(item) == True: # same name
        if baseline_dict[item][0] == 'DIR': # dir only check existency
             baseline_dict[item].append( 1 )
        else:   # file need check md5 
            if working_dict[item][4] == baseline_dict[item][4]: # check MD5
                baseline_dict[item].append( 1 )



for item in sorted(baseline_dict.keys()):
    if baseline_dict[item][-1] == 1:
        pass
    else:
        #print baseline_dict[item] # patch's remove item
        remove_items.append(baseline_dict[item])
    

#remove old dir
cleandir = os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME)
if os.path.exists(cleandir):
    shutil.rmtree(cleandir )
    

#collect files 
for item in add_items: 
    #print item     
    if item[0] == 'File':
        fullPath =  os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME,ADD_DIR,item[1])
        #print 'fullPath:',fullPath
        parentDir = os.path.split(fullPath)[0]
        #print 'parentDir:',parentDir
        if os.path.exists(parentDir):
            pass
        else:
            os.makedirs(parentDir)
        shutil.copy(os.path.join(workDir,item[1]),os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME,ADD_DIR,item[1]))
    elif item[0] == 'DIR':
        #print os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME,ADD_DIR,item[1])
        destdir =os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME,ADD_DIR,item[1])
        if os.path.exists(destdir):
            pass
        else:
            os.makedirs(destdir)
    else:
        pass
    
#print '===================='                
for item in remove_items:
    #print item     
    if item[0] == 'File':
        fullPath =  os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME,REMOVE_DIR,item[1])
        #print 'fullPath:',fullPath
        parentDir = os.path.split(fullPath)[0]
        #print 'parentDir:',parentDir
        if os.path.exists(parentDir):
            pass
        else:
            os.makedirs(parentDir)
        shutil.copy(os.path.join(baselineDir,item[1]),os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME,REMOVE_DIR,item[1]))
    elif item[0] == 'DIR':
        #print os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME,REMOVE_DIR,item[1])
        destdir =os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME,REMOVE_DIR,item[1])
        if os.path.exists(destdir):
            pass
        else:
            os.makedirs(destdir)
    else:
        pass

#=====================================
#generate do_patch.py in destpatch dir
do_patch_filename = os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME,'do_patch.py')
doScriptUnderDir = os.path.join(patchDir,TRUNKTAG_PATH,PROJECT_NAME)

baseline_dir_dict_path = os.path.join(cur_path,baseline_dir_dict)
working_dir_dict_path = os.path.join(cur_path,working_dir_dict)

str_script = gen_do_patch.gen_script(add_items,
                                    remove_items,
                                    doScriptUnderDir ,
                                    baseline_dir_dict_path, 
                                    working_dir_dict_path ,
                                    baseline_dir,
                                    working_dir)
                                    
do_patch_file = open(do_patch_filename,'w')
do_patch_file.write(str_script)
do_patch_file.close()

try:
    #report a patch make action
    import mail_reporter
    user = os.getlogin() if (sys.platform != 'win32' ) else 'unknown'
    sub = u'PatchMaker used by %s %s'%(user,time.ctime())
    content = u'''doScriptUnderDir = %s
    baseline_dir_dict_path = %s
    working_dir_dict_path = %s
    baseline_dir = %s
    working_dir = %s\n'''%(doScriptUnderDir ,baseline_dir_dict_path, working_dir_dict_path ,baseline_dir,working_dir)
    
    release_notes_file_path = os.path.join(working_dir,'release_notes.txt')
    try:
        content += '---------------------------\n'
        content += 'release_notes.txt :\n\n'
        
        file = open(release_notes_file_path,'rb')
        info = file.read()
        #content += base64.encodestring(info)
        content += info.decode("gb2312")
        content += '---------------------------\n'
        
    except Exception as e:
        print e
        content += e
        pass
    
    mail_reporter.send_mail(sub ,content )
except Exception as err:  
    print err
    pass
print "make_patch done."
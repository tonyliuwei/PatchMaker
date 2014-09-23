import os
import sys
import time
import shutil 
import string

from util import *
import DirBrowser
#add current dir to sys path
sys.path.append(os.getcwd())
#from patch_maker_config import *




class myDirBrowser(DirBrowser.DirBrowser):
    
    def __init__(self , exporter , strInitDir="",):
        DirBrowser.DirBrowser.__init__(self,strInitDir)
        self.exporter = exporter
        
    def ProcessFile(self, strFilename,strDir):     
        fullName = os.path.join(strDir,strFilename)
        relativeName = os.path.relpath(fullName ,self.m_strInitDir)   
        file_md5 = md5Checksum(fullName)
        strInfo = "File;%s;%s;%s;%s"%(relativeName,str(os.path.getmtime(fullName)),str(os.path.getsize(fullName)),file_md5 )
        self.exporter.export(strInfo)
        #print "FILE:"+fullName + ","+ "timestemp:"+str(os.path.getmtime(fullName))+","+"filesize:"+str(os.path.getsize(fullName))
        pass

    def ProcessDir(self,strCurrentdir,strParentdir):
        if(strParentdir == None): # first level. do nothing
            pass
        else:
            fullDir = os.path.join(strParentdir,strCurrentdir)
            relativeDir = os.path.relpath(fullDir ,self.m_strInitDir)    
            #print "DIR:"+strCurrentdir+","
            #print "DIR:"+fullDir + ","+ "timestemp:"+str(os.path.getmtime(fullDir))
            #print "DIR;%s;%s"%(relativeDir ,str(os.path.getmtime(fullDir)))
            strInfo = "DIR;%s;%s"%(relativeDir ,str(os.path.getmtime(fullDir)))
            self.exporter.export(strInfo)
            pass
            

class ListExporter( Exporter ):
    def __init__(self):
        self._list = []
        
        pass
    def close(self):
        pass        
    def getList(self):
        return self._list 
    def export(self,strInfo):
        self._list.append(strInfo.split(';'))
        pass
 
#todo: dir sort still has problem       
#generate do_patch.py
# InitDir is parent dir contains add/remove
def genAddList(strInitDir):
    addlistExporter = ListExporter()
    addDirBrowser = myDirBrowser(addlistExporter )
    addDir = os.path.join(strInitDir,ADD_DIR)
    #print addDir
    if(addDirBrowser.SetInitDir(addDir)==0):
        print ("false")
        return []
    else:
        addDirBrowser.BeginBrowse()        
        pass
    add_list =  addlistExporter.getList()
    return add_list
    
def genRemoveList(strInitDir):
    removelistExporter = ListExporter()
    removeDirBrowser = myDirBrowser(removelistExporter )
    removeDir = os.path.join(strInitDir,REMOVE_DIR)
    #print removeDir 
    if(removeDirBrowser.SetInitDir(removeDir)==0):
        print ("false")
        return []
    else:
        removeDirBrowser.BeginBrowse()        
        pass
    remove_list = removelistExporter.getList()
    return remove_list 
   

        

def gen_script(add_list,remove_list,strInitDir,baseline_dir_dict = 'unknown',working_dir_dict = 'unknown' , baseline_dir = 'unknown' ,working_dir= 'unknown'):    
    dd = {}
    dd['gen_time'] = time.ctime()
    dd['initDir'] = strInitDir
    dd['baseline_dir_dict'] = baseline_dir_dict
    dd['working_dir_dict'] = working_dir_dict
    dd['baseline_dir'] =  baseline_dir
    dd['working_dir'] = working_dir
    dd['user'] = os.getlogin() if (sys.platform != 'win32' ) else 'unknown'
    dd['ADD_DIR']= "'%s'"% ADD_DIR
    dd['REMOVE_DIR'] = "'%s'"% REMOVE_DIR
    dd['add_items'] = str(sorted(add_list))
    dd['remove_items'] = str(sorted(remove_list,reverse = True))
    
    ss = string.Template('''#!/usr/bin/python
#Autogen by PATCH_MAKER. Don't modify by yourself
# ----------------------------
# generate time: $gen_time by user: $user
# Add/Remove in: $initDir
# baseline_dict: $baseline_dir_dict
# working_dict : $working_dir_dict
# baseline_dir : $baseline_dir
# working_dir  : $working_dir
# ----------------------------
#       

import sys
import os
import time
import hashlib
import shutil



ADD_DIR =$ADD_DIR
REMOVE_DIR =$REMOVE_DIR

# add_items with DIR on top
add_items = $add_items

# remove_items with DIR on bottem. DIR will be removed after file be removed
remove_items = $remove_items

def usage():
    print "Usage: python do_patch.py target_full_path"

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
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        target_path = sys.argv[1]
        if os.path.exists(target_path):
            print "Do patch on dir: %s"%target_path
            # do remove files and dirs according remove_items
            for item in remove_items:
                if item[0] == 'File': # remove file from target 
                    rm_file_name = os.path.join(target_path, item[1])
                    if os.path.exists(rm_file_name) :
                        md5_dest = md5Checksum(rm_file_name)
                        if md5_dest != item[4]:
                            print "Waring: MD5 check wrong"
                        os.remove(rm_file_name)
                    else:
                        print "Warning: File %s doesn't exist but was calmed to remove"%rm_file_name
                elif item[0] == 'DIR': # remove dir from target
                    rm_dir_name = os.path.join(target_path, item[1])
                    if os.path.exists(rm_dir_name) :
                        #shutil.rmtree(rm_dir_name) # may del files which should be keep
                        try: # if a dir is empty and parent is empty
                            os.removedirs(rm_dir_name) # remove a leaf directory and all empty intermediate ones
                        except:
                            pass # just omit it
                            
                    else:
                        #print "Warning: Dir %s doesn't exist but was calmed to remove"%rm_dir_name
                        pass
                else:
                    print "Warning: bad format"
            # do add files and dirs according add_items
            for item in add_items:
                if item[0] == 'File':
                    cp_file_name = os.path.join(target_path,item[1])
                    if os.path.exists(cp_file_name): #should not exist
                        print "Warning: dest file %s should not exist"%cp_file_name
                    else: # do copy to destination
                        shutil.copy(os.path.join(ADD_DIR,item[1]),cp_file_name)
        
                    pass
                elif item[0] == 'DIR':
                    cp_dir_name = os.path.join(target_path,item[1])
                    if os.path.exists(cp_dir_name): #should not exist
                        print "Warning: dest dir %s should not exist"%cp_dir_name
                    else:
                        os.makedirs(cp_dir_name)
                    pass
                else:
                    print "Warning: bad format"
            print "Done"                    
        else:
            print "Error. target_path %s does not exist"%target_path


    ''')
    #print ss.substitute(dd)
    do_script = ss.substitute(dd)
    
    return do_script 
    
    
def usage():
    print '''Usage: python gen_do_patch.py [patch_dir]
    
    will generate a do_patch.py in patch_dir
    orginal do_patch.py will be overwrite
    '''   
     
def gen_do_patch_py(strInitDir,baseline_dir_dict = 'unknown',working_dir_dict = 'unknown' , baseline_dir = 'unknown' ,working_dir= 'unknown' ):

    add_list = genAddList(strInitDir)
    remove_list = genRemoveList(strInitDir)
    
    str_script = gen_script(add_list , remove_list ,
            strInitDir,
            baseline_dir_dict ,
            working_dir_dict , 
            baseline_dir ,
            working_dir )
    return str_script
    
def main():
    cur_path = os.getcwd()
    if len(sys.argv) == 2:        
        initDir = sys.argv[1]
    else:
        initDir = cur_path                
    
    str_script = gen_do_patch_py(initDir)
    dest_file_name = os.path.join(initDir,'do_patch.py')
    print dest_file_name 
    if os.path.exists(dest_file_name) :
        print "do_script.py exist in %s. Do nothing"%initDir
    else:
        f = open(dest_file_name,'w')
        f.write(str_script)
        f.close()
    pass
    
if __name__ == '__main__':
    main()    
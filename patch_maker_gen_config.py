#!/usr/bin/python
import os,sys
import string

cur_dir = os.getcwd()

config_file_name = os.path.join(cur_dir,'patch_maker_config.py')
defult_config = '''#patch_maker_config.py
PROJECT_NAME = ""
baseline_dir = ""
working_dir = ""
'''
if os.path.exists(config_file_name ) :
    print config_file_name  , " exist in current dir. Do nothing"
else:
    f = open(config_file_name ,'w')
    f.write(defult_config )
    f.close()
    
    print "Default PatchMaker config file generated: ",config_file_name 

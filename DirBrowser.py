


import os
import os.path



_debug = 0
_debug_lev1 = 0
_debug_lev2 = 1

class DirBrowser:
    """general class for browse a directory
    """
    def __init__(self,strInitDir="" ):
        if(_debug and _debug_lev1):
            print("init")
        self.m_strInitDir = strInitDir
        self.m_omitDir = {}
        self.m_omitFile = {}
        self.m_omitFileExt = {}

    def SetOmitDir(self,omitDir):
        self.m_omitDir = omitDir
        
    def SetOmitFile(self,omitFile):
        self.m_omitFile = omitFile
    
    def SetOmitFileExt(self,omitFileExt):
        self.m_omitFileExt = omitFileExt
        
    def SetInitDir(self,strInitDir):
        """
        if return 0, means the strInitDir is invalidate
        otherwise return 1
        """
        res = 0

        # test existence, readable writeable
        # of dir
        #
        res = os.access(strInitDir,os.F_OK| \
                                   os.R_OK)#| \
                                   #os.W_OK  )
        #res = os.access(strInitDir,os.F_OK| \
        #                           os.R_OK| \
        #                           os.W_OK  )
       
        if(res == 0):
            return 0
        else:
            self.m_strInitDir = strInitDir
            os.chdir(strInitDir)
            return 1

    
    def BeginBrowse(self,strFileSpec=[]):
        """
        return value
        0   : false
        1   : true
        """
        self.ProcessDir(self.m_strInitDir,None);
    	return self.BrowseDir(self.m_strInitDir, \
                              strFileSpec);
        
    def BrowseDir(self, strDir, strFilespec=[]):
        """
        return
        0   : false
        1   : true
        """
        

            
        self.OnEnterThisDir(strDir)

        # now we enter the dir
        os.chdir(strDir)
        list = []
        list = os.listdir(strDir)
        # now list contain all sub-file and sub-dir
        if(_debug and _debug_lev1):
            print "\n".join(list)
        filelist = []
        subdirlist = []
        for s in list:
            if(os.path.isfile(s)):
                filelist.append(s)
            elif(os.path.isdir(s)):
                subdirlist.append(s)
            else:
                #print("what's hell?") + strDir +": " + s
                pass


        if(_debug and _debug_lev1):
            print ":----file list:----"
            print "\n".join(filelist)
            print ":----dir list:----"
            print "\n".join(subdirlist)

        # process files
        for filename in filelist:
            if(self.m_omitFile.has_key(filename)== True):
                continue # do nothing
            
            ext = os.path.splitext(filename)[1] 
            if self.m_omitFileExt.has_key(ext) == True:
                #print 'bingo omitFileExt'
                #print ext ,' ' ,filename
                continue #d do nothing
                
            if(os.path.islink(strDir+'/'+ filename ) == True): # it is a link
                continue# do nothing
                
            if(self.ProcessFile(filename,strDir) == 0): #
                pass
            else:
                pass # todo: check

        # finish all files
        self.OnFinishAllFilesInThisFolder(strDir)

        # process dirs
        for dirname in subdirlist:
            if (self.m_omitDir.has_key(dirname) == True):
                continue # do nothing
            fullDirName = os.path.join(strDir , dirname)
            if(os.path.islink(fullDirName) == True): # it is a link
                continue # do nothing
            
            self.ProcessDir(dirname, strDir) #strDir is the parent
            
            if(self.BrowseDir(os.path.join(strDir,dirname) , \
                              strFilespec) == 0):
                return 0
        
       	self.OnFinishThisDir(strDir);
        return 1


    def ProcessFile(self, strFilename,strDir):
        """
        return value
            0   : false
            1   : true

        override this function
        """
        if(_debug and _debug_lev2):
            print "process: %s\\%s" % (strDir,strFilename) #full pathname
            print "fileNme: %s" % strFilename #filename only
        
        pass

    def ProcessDir(self,strCurrentdir,strParentdir):
        """
        no return
        override this function
        """
        if(_debug and _debug_lev2):
            print "process dir: %s in %s" % (strCurrentdir,strParentdir)
        pass


    def OnEnterThisDir(self,strCurrentdir):
        """
        override this function
        """
        pass

    def OnFinishAllFilesInThisFolder(self,strCurrentdir):
        """
        override this function
        """
        pass

    def OnFinishThisDir(self,strCurrentdir):
        """
        override this function
        """
        pass
    

def testDirBrowser():
    a = DirBrowser()
    if(a.SetInitDir("D:\\tony\\workspace")==0):
        print ("false")
    else:
        print a.m_strInitDir
        a.BeginBrowse()

if __name__ == '__main__':
    testDirBrowser()
    
